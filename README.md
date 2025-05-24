# GNSS-IMU 可視化システム

## 概要

このプロジェクトは、GNSS（GPS）およびIMUセンサを用いて、リアルタイムで位置と方位を可視化するWebベースのシステムです。RTK-GNSSの精密な位置情報やIMUの方位データをKalman Filterで融合し、Leaflet.jsベースの地図とグラフで表示します。

---

## 特徴

- 📡 **GNSS + IMUセンサ統合（Kalman Filter）**
- 🧭 **リアルタイム方位推定と地図表示**
- 📈 **RTK誤差履歴・履歴軌跡のグラフ表示**
- 🧪 **実センサ/シミュレーションの自動/手動切替**
- 📱 **スマートフォン・タブレット対応のレスポンシブUI**
- 🛰 **衛星補足数やHDOPの視覚化**
- ⚠️ **異常データの検出・警告表示**

---

## 構成

 `run.py`: Flaskサーバー本体
- `sensor.py`: センサ取得＆シミュレーション管理
- `kalman.py`: Kalman Filter ロジック
- `imu_reader.py`: MPU6050センサー用ドライバ
- `templates/index.html`: UIページ（地図とグラフ）
- `public/map.js`: 地図処理（Leaflet）
- `public/chart.js`: グラフ表示（Chart.js）
- `INSTALL.md`: インストール手順
- `LICENSE`: MITライセンス
- `docs/manual.pdf`: 取扱説明書（PDF）
- `README.md`: このファイル

---

## インストール手順（詳細は INSTALL.md）
必要パッケージのインストール




```bash

sudo apt-get install i2c-tools
sudo pip install mpu6050-raspberrypi


git clone https://github.com/WoodyPride1970/gnss_imu_visualizer.git
cd gnss_imu_visualizer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

---

