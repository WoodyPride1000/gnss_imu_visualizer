# run.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sensor import SensorManager
from threading import Thread
import time

# Flask アプリケーション初期化
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# センサーマネージャの初期化（自動 or 強制）
sensor_manager = SensorManager()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected.")

@socketio.on('toggle_sensor_mode')
def handle_toggle(data):
    mode = data.get("mode")
    if mode in ["real", "sim"]:
        sensor_manager.force_mode(mode)
        emit('mode_update', {"current_mode": mode})
        print(f"Sensor mode forcibly switched to: {mode}")

def emit_sensor_data():
    while True:
        data = sensor_manager.get_data()
        try:
            socketio.emit('message', data)
        except Exception as e:
            print(f"Emit error: {e}")
        time.sleep(1)

if __name__ == '__main__':
    sensor_thread = Thread(target=emit_sensor_data, daemon=True)
    sensor_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
