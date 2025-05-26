import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, filename='kalman.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class KalmanFilter1D:
    def __init__(self, sensor_type: str = "gnss", rtk_fix_type: int = None):
        try:
            self.A = 1.0
            self.H = 1.0
            if sensor_type == "gnss":
                self.Q = 0.01
                self.R = 0.2 if rtk_fix_type == 4 else 1.5
            elif sensor_type == "imu":
                self.Q = 0.05
                self.R = 1.0
            else:
                raise ValueError(f"Unsupported sensor type: {sensor_type}")
            logger.info(f"Initialized KalmanFilter1D for {sensor_type}, Q={self.Q}, R={self.R}")
        except Exception as e:
            logger.error(f"KalmanFilter1D initialization error: {e}")
            raise

    def filter(self, z_meas: float, x_est_prev: float, p_est_prev: float, u: float = 0.0, rtk_fix_type: int = None) -> Tuple[float]:
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

            if rtk_fix_type is not None:
                self.R = 0.2 if rtk_fix_type == 4 else 1.5

            x_pred = self.A * x_est_prev + u
            p_pred = self.A * p_est_prev * self.A + self.Q

            if (self.H * p_pred * self.H + self.R) == 0:
                raise ValueError("Denominator in Kalman gain calculation is zero")
            K = p_pred * self.H / (self.H * p_pred * self.H + self.R)

            x_est = x_pred + K * (z_meas - self.H * x_pred)
            p_est = (1 - K * self.H) * p_pred

            return x_est, p_est
        except Exception as e:
            logger.error(f"Kalman filter error: {e}")
            raise
