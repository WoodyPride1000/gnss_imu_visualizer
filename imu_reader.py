import logging
import math
import time
from datetime import datetime, timezone
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, filename='imu.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DummyIMU:
    """ダミーIMU（テスト用）"""
    def get_data(self) -> Dict:
        try:
            return {
                'gyro_z': 0.0,
                'heading': 0.0,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"DummyIMU error: {e}")
            raise

class IMUReader:
    def __init__(self, forced_mode: Optional[str] = None):
        self.forced_mode = forced_mode
        self.imu = self._select_imu()
        self.state = {'x_est_heading': 0.0, 'p_est_heading': 1.0}
        self.last_time = None
        self.kalman_filter = KalmanFilter1D(sensor_type="imu")

    def _select_imu(self):
        try:
            if self.forced_mode == 'dummy':
                logger.info("Using DummyIMU")
                return DummyIMU()
            logger.info("Using DummyIMU (default)")
            return DummyIMU()
        except Exception as e:
            logger.error(f"IMU selection error: {e}")
            raise

    def get_data(self) -> Dict:
        try:
            data = self.imu.get_data()
            current_time = datetime.now(timezone.utc)
            dt = (current_time - self.last_time).total_seconds() if self.last_time else 0.0
            self.last_time = current_time

            # カルマンフィルター適用
            self.state['x_est_heading'], self.state['p_est_heading'] = self.kalman_filter.filter(
                data['heading'], self.state['x_est_heading'], self.state['p_est_heading'], u=data['gyro_z'] * dt
            )

            # ヘディング正規化
            heading = self.state['x_est_heading'] % 360
            if heading < 0:
                heading += 360

            return {
                'heading': heading,
                'timestamp': current_time.isoformat()
            }
        except Exception as e:
            logger.error(f"IMUReader get_data error: {e}")
            raise
