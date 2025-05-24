from mpu6050 import mpu6050
from kalman import kalman_filter
import time

class IMUReader:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)
        self.angle = 0.0
        self.last_time = time.time()
        self.x_est_heading, self.p_est_heading = 0.0, 1.0

    def read_heading(self):
        try:
            gyro_data = self.sensor.get_gyro_data()
            dt = time.time() - self.last_time
            self.angle += gyro_data['z'] * dt
            self.last_time = time.time()
            self.x_est_heading, self.p_est_heading = kalman_filter(self.angle, self.x_est_heading, self.p_est_heading)
            return self.x_est_heading
        except Exception as e:
            print(f"IMU read error: {e}")
            return self.x_est_heading

    def is_connected(self):
        try:
            self.sensor.get_accel_data()
            return True
        except:
            return False
