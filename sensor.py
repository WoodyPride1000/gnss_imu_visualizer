import random
import time
from datetime import datetime
from kalman import kalman_filter
import serial
import pynmea2

# 実センサーモジュール（GNSS用）
try:
    import serial
    import pynmea2
    SENSOR_AVAILABLE = True
except ImportError:
    SENSOR_AVAILABLE = False

class SensorBase:
    def get_data(self):
        raise NotImplementedError()

class RealSensor(SensorBase):
    def __init__(self):
        from imu_reader import IMUReader
        self.imu = IMUReader()
        self.serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1) if SENSOR_AVAILABLE else None
        self.x_est_lat, self.p_est_lat = 35.681236, 1.0
        self.x_est_lon, self.p_est_lon = 139.767125, 1.0

    def read_data(self):
        # GNSSデータ取得
        try:
            if self.serial and SENSOR_AVAILABLE:
                line = self.serial.readline().decode('ascii', errors='ignore')
                if line.startswith('$GNGGA'):
                    msg = pynmea2.parse(line)
                    raw_lat, raw_lon = msg.latitude, msg.longitude
                    rtk_fix_type = msg.gps_qual
                    satellite_count = msg.num_sats
                    error_radius = 0.2 if rtk_fix_type == 4 else 1.5
                else:
                    raise ValueError("No valid GNGGA data")
            else:
                raw_lat = 35.681236 + random.uniform(-0.0002, 0.0002)
                raw_lon = 139.767125 + random.uniform(-0.0002, 0.0002)
                rtk_fix_type = random.choice([1, 4])
                satellite_count = random.randint(4, 12)
                error_radius = random.uniform(0.2, 1.5) if rtk_fix_type == 4 else random.uniform(1.5, 5.0)
        except Exception as e:
            print(f"GNSS error: {e}")
            raw_lat = 35.681236 + random.uniform(-0.0002, 0.0002)
            raw_lon = 139.767125 + random.uniform(-0.0002, 0.0002)
            rtk_fix_type = random.choice([1, 4])
            satellite_count = random.randint(4, 12)
            error_radius = random.uniform(0.2, 1.5) if rtk_fix_type == 4 else random.uniform(1.5, 5.0)

        # IMUヘディング取得
        heading = self.imu.read_heading() if self.imu.is_connected() else random.uniform(0, 360)

        # カルマンフィルター適用
        self.x_est_lat, self.p_est_lat = kalman_filter(raw_lat, self.x_est_lat, self.p_est_lat)
        self.x_est_lon, self.p_est_lon = kalman_filter(raw_lon, self.x_est_lon, self.p_est_lon)

        return {
            "lat": self.x_est_lat,
            "lon": self.x_est_lon,
            "heading": (heading + 90) % 360,
            "rtk_fix_type": rtk_fix_type,
            "error_radius": error_radius,
            "satellite_count": satellite_count,
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
        satellite_count = random.randint(4, 12)
        error_radius = random.uniform(0.2, 1.5) if rtk_fix_type == 4 else random.uniform(1.5, 5.0)

        self.x_est_lat, self.p_est_lat = kalman_filter(raw_lat, self.x_est_lat, self.p_est_lat)
        self.x_est_lon, self.p_est_lon = kalman_filter(raw_lon, self.x_est_lon, self.p_est_lon)

        return {
            "lat": self.x_est_lat,
            "lon": self.x_est_lon,
            "heading": heading,
            "rtk_fix_type": rtk_fix_type,
            "error_radius": error_radius,
            "satellite_count": satellite_count,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

class SensorManager:
    def __init__(self):
        self.forced_mode = None  # "real", "sim", "auto"
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
