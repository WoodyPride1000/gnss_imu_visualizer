# sensor.py
import random
import time
from datetime import datetime
from kalman import kalman_filter

# 実センサーモジュールがあればここに組み込む（例: serial, smbus 等）
try:
    import real_sensor_module  # 仮名、実際のセンサライブラリに置き換え
    SENSOR_AVAILABLE = True
except ImportError:
    SENSOR_AVAILABLE = False

class SensorBase:
    def get_data(self):
        raise NotImplementedError()

class RealSensor(SensorBase):
    def __init__(self):
        self.x_est_lat, self.p_est_lat = 0.0, 1.0
        self.x_est_lon, self.p_est_lon = 0.0, 1.0

    def read_gnss(self):
        # 実際のGNSSデータ取得処理に置き換える
        return 35.681236 + random.uniform(-0.0001, 0.0001), 139.767125 + random.uniform(-0.0001, 0.0001)

    def read_heading(self):
        # 実際のIMUによる方位角取得処理に置き換える
        return (random.uniform(0, 360) + 90) % 360  # +90度補正

    def read_rtk_status(self):
        # 例: u-blox の Fix type 1=none, 4=RTK Fixed
        return random.choice([1, 4])

    def get_data(self):
        raw_lat, raw_lon = self.read_gnss()
        heading = self.read_heading()
        rtk_fix_type = self.read_rtk_status()
        error_radius = random.uniform(0.2, 1.5) if rtk_fix_type == 4 else random.uniform(1.5, 5.0)

        self.x_est_lat, self.p_est_lat = kalman_filter(raw_lat, self.x_est_lat, self.p_est_lat)
        self.x_est_lon, self.p_est_lon = kalman_filter(raw_lon, self.x_est_lon, self.p_est_lon)

        return {
            "lat": self.x_est_lat,
            "lon": self.x_est_lon,
            "heading": heading,
            "rtk_fix_type": rtk_fix_type,
            "error_radius": error_radius,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

class SensorSimulator(SensorBase):
    def __init__(self):
        self.x_est_lat, self.p_est_lat = 35.681236, 1.0
        self.x_est_lon, self.p_est_lon = 139.767125, 1.0

    def get_data(self):
        raw_lat = 35.681236 + random.uniform(-0.0002, 0.0002)
        raw_lon = 139.767125 + random.uniform(-0.0002, 0.0002)
        heading = (random.uniform(0, 360) + 90) % 360
        rtk_fix_type = random.choice([1, 4])
        error_radius = random.uniform(0.2, 1.5) if rtk_fix_type == 4 else random.uniform(1.5, 5.0)

        self.x_est_lat, self.p_est_lat = kalman_filter(raw_lat, self.x_est_lat, self.p_est_lat)
        self.x_est_lon, self.p_est_lon = kalman_filter(raw_lon, self.x_est_lon, self.p_est_lon)

        return {
            "lat": self.x_est_lat,
            "lon": self.x_est_lon,
            "heading": heading,
            "rtk_fix_type": rtk_fix_type,
            "error_radius": error_radius,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

class SensorManager:
    def __init__(self):
        self.forced_mode = None  # "real" または "sim"
        self.sensor = self._select_sensor()

    def _select_sensor(self):
        if self.forced_mode == "real":
            return RealSensor()
        elif self.forced_mode == "sim":
            return SensorSimulator()
        elif SENSOR_AVAILABLE:
            return RealSensor()
        else:
            return SensorSimulator()

    def force_mode(self, mode):
        self.forced_mode = mode
        self.sensor = self._select_sensor()

    def get_data(self):
        return self.sensor.get_data()
