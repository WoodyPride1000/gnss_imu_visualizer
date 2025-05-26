import logging
import math
from datetime import datetime, timezone
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, filename='sensor.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DummySensor:
    """ダミーセンサー（テスト用）"""
    def get_data(self) -> Dict:
        try:
            return {
                'lat': 35.681236,  # 東京駅
                'lon': 139.767125,
                'rtk_fix_type': 4,  # RTK固定
                'error_radius': 0.1,  # 誤差半径（メートル）
                'satellite_count': 12,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"DummySensor error: {e}")
            raise

class SensorManager:
    def __init__(self):
        self.forced_mode: Optional[str] = None
        self.state = {
            'x_est_lat': 35.681236, 'p_est_lat': 1.0,
            'x_est_lon': 139.767125, 'p_est_lon': 1.0
        }
        self.sensor = self._select_sensor()
        self.last_position = None
        self.last_time = None
        self.kalman_filter = KalmanFilter1D(sensor_type="gnss")

    def _select_sensor(self):
        try:
            if self.forced_mode == 'dummy':
                logger.info("Using DummySensor")
                return DummySensor()
            # 実際のセンサー実装を追加（例: RTKLIB, NMEAパーサー）
            logger.info("Using DummySensor (default)")
            return DummySensor()
        except Exception as e:
            logger.error(f"Sensor selection error: {e}")
            raise

    def get_data(self) -> Dict:
        try:
            data = self.sensor.get_data()
            current_time = datetime.now(timezone.utc)

            # カルマンフィルターで緯度・経度を平滑化
            self.state['x_est_lat'], self.state['p_est_lat'] = self.kalman_filter.filter(
                data['lat'], self.state['x_est_lat'], self.state['p_est_lat'], rtk_fix_type=data['rtk_fix_type']
            )
            self.state['x_est_lon'], self.state['p_est_lon'] = self.kalman_filter.filter(
                data['lon'], self.state['x_est_lon'], self.state['p_est_lon'], rtk_fix_type=data['rtk_fix_type']
            )

            # 速度計算
            velocity = 0.0
            if self.last_position and self.last_time:
                dt = (current_time - self.last_time).total_seconds()
                if dt > 0:
                    dlat = self.state['x_est_lat'] - self.last_position['lat']
                    dlon = self.state['x_est_lon'] - self.last_position['lon']
                    distance = ((dlat * 111000) ** 2 + (dlon * 111000 * math.cos(math.radians(self.state['x_est_lat']))) ** 2) ** 0.5
                    velocity = distance / dt

            self.last_position = {'lat': self.state['x_est_lat'], 'lon': self.state['x_est_lon']}
            self.last_time = current_time

            return {
                'lat': self.state['x_est_lat'],
                'lon': self.state['x_est_lon'],
                'velocity': velocity,
                'rtk_fix_type': data['rtk_fix_type'],
                'error_radius': data['error_radius'],
                'satellite_count': data['satellite_count'],
                'timestamp': current_time.isoformat()
            }
        except Exception as e:
            logger.error(f"SensorManager get_data error: {e}")
            raise
