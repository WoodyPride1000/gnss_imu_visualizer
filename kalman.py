"""
Simple 1D Kalman Filter implementation for position and heading estimation.
"""

def kalman_filter(z_meas, x_est_prev, p_est_prev, A=1.0, H=1.0, Q=0.01, R=1.0):
    """
    Parameters:
        z_meas     : float - New measurement
        x_est_prev : float - Previous estimated state
        p_est_prev : float - Previous error covariance
        A          : float - State transition coefficient
        H          : float - Observation model coefficient
        Q          : float - Process noise covariance
        R          : float - Measurement noise covariance
    
    Returns:
        x_est : float - Updated state estimate
        p_est : float - Updated error covariance
    """
    if not isinstance(z_meas, (int, float)) or z_meas is None:
        raise ValueError("Measurement must be a valid number")

    # Predict
    x_pred = A * x_est_prev
    p_pred = A * p_est_prev * A + Q

    # Kalman Gain
    K = p_pred * H / (H * p_pred * H + R)

    # Update
    x_est = x_pred + K * (z_meas - H * x_pred)
    p_est = (1 - K * H) * p_pred

    return x_est, p_est
