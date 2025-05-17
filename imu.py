
from mpu6050 import mpu6050

class IMUReader:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

    def read_heading(self):
        gyro_data = self.sensor.get_gyro_data()
        return gyro_data['z']  # 簡易的なジャイロZ軸の角速度を返す（参考値）

    def is_connected(self):
        try:
            self.sensor.get_accel_data()
            return True
        except:
            return False
