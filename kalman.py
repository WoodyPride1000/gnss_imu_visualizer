import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, filename='kalman.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class KalmanFilter1D:
    def __init__(self, sensor_type: str = "gnss", rtk_fix_type: int = None):
        """
        Initialize 1D Kalman Filter with sensor-specific parameters.

        Parameters:
            sensor_type (str): Type of sensor ("gnss" or "imu").
            rtk_fix_type (int): GNSS RTK fix type (e.g., 4 for RTK fix).
        """
        try:
            self.A = 1.0  # 状態遷移係数（静的モデル）
            self.H = 1.0  # 観測モデル係数
            if sensor_type == "gnss":
                self.Q = 0.01  # プロセスノイズ
                self.R = 0.2 if rtk_fix_type == 4 else 1.5  # 観測ノイズ
            elif sensor_type == "imu":
                self.Q = 0.05  # IMUはドリフトを考慮
                self.R = 1.0   # ジャイロの観測ノイズ
            else:
                raise ValueError(f"Unsupported sensor type: {sensor_type}")
            logger.info(f"Initialized KalmanFilter1D for {sensor_type}, Q={self.Q}, R={self.R}")
        except Exception as e:
            logger.error(f"KalmanFilter1D initialization error: {e}")
            raise

    def filter(self, z_meas: float, x_est_prev: float, p_est_prev: float, u: float = 0.0, rtk_fix_type: int = None) -> Tuple[float, float]:
        """
        1D Kalman Filter for position or heading estimation.

        Parameters:
            z_meas (float): New measurement (e.g., GNSS position or IMU angle).
            x_est_prev (float): Previous estimated state.
            p_est_prev (float): Previous error covariance.
            u (float): Control input (e.g., gyro angular velocity for IMU).
            rtk_fix_type (int): GNSS RTK fix type for dynamic R adjustment.

        Returns:
            tuple: (x_est, p_est) - Updated state estimate and error covariance.
        """
        try:
            if not isinstance(z_meas, (int, float)) or z_meas is None:
                raise ValueError("Measurement must be a valid number")
            if not all(isinstance(x, (int, float)) for x in [x_est_prev, p_est_prev, u]):
                raise ValueError("Parameters must be numbers")
            if p_est_prev < 0:
                raise ValueError("Previous error covariance must be non-negative")
            if abs(z_meas) > 1e6:
                logger.warning(f"Large measurement value: {z_meas}")
                raise ValueError(f"Measurement value {z_meas} is out of reasonable range")

            # RTKフィックスに応じた観測ノイズの動的調整
            if rtk_fix_type is not None:
                self.R = 0.2 if rtk_fix_type == 4 else 1.5

            # 予測
            x_pred = self.A * x_est_prev + u
            p_pred = self.A * p_est_prev * self.A + self.Q

            # カルマンゲイン
            if (self.H * p_pred * self.H + self.R) == 0:
                raise ValueError("Denominator in Kalman gain calculation is zero")
            K = p_pred * self.H / (self.H * p_pred * self.H + self.R)

            # 更新
            x_est = x_pred + K * (z_meas - self.H * x_pred)
            p_est = (1 - K * self.H) * p_pred

            return x_est, p_est
        except Exception as e:
            logger.error(f"Kalman filter error: {e}")
            raise
