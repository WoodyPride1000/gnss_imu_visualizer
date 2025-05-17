# kalman.py
# 単純な線形カルマンフィルタの実装

def kalman_filter(z_meas, x_est_prev, p_est_prev, A=1, H=1, Q=0.01, R=1.0):
    """
    線形カルマンフィルタによる1次元状態推定

    Parameters:
    - z_meas: 観測値（測定値）
    - x_est_prev: 直前の状態推定値
    - p_est_prev: 直前の推定誤差分散
    - A: 状態遷移モデル
    - H: 観測モデル
    - Q: プロセスノイズ分散
    - R: 観測ノイズ分散

    Returns:
    - x_est: 更新後の状態推定値
    - p_est: 更新後の推定誤差分散
    """
    # 予測ステップ
    x_pred = A * x_est_prev
    p_pred = A * p_est_prev * A + Q

    # カルマンゲインの計算
    K = p_pred * H / (H * p_pred * H + R)

    # 更新ステップ
    x_est = x_pred + K * (z_meas - H * x_pred)
    p_est = (1 - K * H) * p_pred

    return x_est, p_est
