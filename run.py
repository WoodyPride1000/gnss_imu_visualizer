from flask import Flask, render_template
from flask_socketio import SocketIO
import logging
import time
from datetime import datetime, timezone
from threading import Lock
from typing import Dict

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)
lock = Lock()

sensor_manager = SensorManager()
imu_reader = IMUReader()

@app.route('/')
def index():
    return render_template('index.html')

def emit_sensor_data():
    while True:
        try:
            with lock:
                sensor_data = sensor_manager.get_data()
                imu_data = imu_reader.get_data()
                data = {
                    'lat': sensor_data['lat'],
                    'lon': sensor_data['lon'],
                    'heading': imu_data['heading'],
                    'velocity': sensor_data['velocity'],
                    'rtk_fix_type': sensor_data['rtk_fix_type'],
                    'error_radius': sensor_data['error_radius'],
                    'satellite_count': sensor_data['satellite_count'],
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                socketio.emit('sensor_data', data)
            time.sleep(1)
        except Exception as e:
            logger.error(f"Emit error: {e}")
            socketio.emit('error', {'message': str(e)})
            time.sleep(1)

if __name__ == '__main__':
    socketio.start_background_task(emit_sensor_data)
    socketio.run(app, host='0.0.0.0, port=5000, debug=False)
