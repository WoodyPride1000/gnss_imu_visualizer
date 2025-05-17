
def kalman_filter(z_meas, x_est_prev, p_est_prev, A=1, H=1, Q=0.01, R=1.0):
    x_pred = A * x_est_prev
    p_pred = A * p_est_prev * A + Q
    K = p_pred * H / (H * p_pred * H + R)
    x_est = x_pred + K * (z_meas - H * x_pred)
    p_est = (1 - K * H) * p_pred
    return x_est, p_est
