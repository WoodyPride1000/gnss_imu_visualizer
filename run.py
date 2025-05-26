from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sensor import SensorManager
from threading import Thread
import time
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Flaskアプリケーション初期化
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# センサーマネージャの初期化
try:
    sensor_manager = SensorManager()
except Exception as e:
    logger.error(f"Failed to initialize SensorManager: {e}")
    exit(1)

@app.route('/')
def index():
    """GNSS/IMUデータの可視化ページをレンダリング"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Template rendering error: {e}")
        return "Error rendering page", 500

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected.")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected.")

@socketio.on('toggle_sensor_mode')
def handle_toggle(data):
    mode = data.get("mode")
    if mode in ["real", "sim", "auto"]:
        try:
            sensor_manager.force_mode(mode)
            emit('mode_update', {"current_mode": mode})
            logger.info(f"Sensor mode switched to: {mode}")
        except Exception as e:
            emit('error', {'message': f"Failed to switch mode: {str(e)}"})
            logger.error(f"Mode switch error: {e}")
    else:
        emit('error', {'message': f"Invalid mode: {mode}"})
        logger.warning(f"Invalid mode requested: {mode}")

def emit_sensor_data():
    """1秒ごとにセンサーデータをクライアントに送信"""
    next_time = time.time()
    while True:
        try:
            data = sensor_manager.get_data()
            socketio.emit('message', data)
        except ValueError as ve:
            logger.error(f"Data format error: {ve}")
            socketio.emit('error', {'message': 'Invalid sensor data format'})
        except ConnectionError as ce:
            logger.error(f"Sensor connection error: {ce}")
            socketio.emit('error', {'message': 'Sensor connection lost'})
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            socketio.emit('error', {'message': 'Unexpected error occurred'})
        
        next_time += 1.0
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == '__main__':
    sensor_thread = Thread(target=emit_sensor_data, daemon=True)
    sensor_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
