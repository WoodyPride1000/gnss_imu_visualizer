📦 INSTALL.md – GNSS/IMU Visualizer インストール手順

✅ 必要条件
Python 3.8 以上
pip（Pythonパッケージマネージャ）
Node.js（地図やグラフ表示に必要なライブラリがある場合）
Git（プロジェクトのクローンと更新）
Raspberry Pi (推奨) または Linux/Windows PC
センサー接続（任意）：
GNSSモジュール（u-blox など）
IMUモジュール（MPU-6050 など）
📁 1. プロジェクトのクローン
git clone https://github.com/WoodyPride1970/gnss_imu_visualizer.git
cd gnss_imu_visualizer
🛠 2. 仮想環境の作成と依存パッケージのインストール
python -m venv venv
source venv/bin/activate     # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
🧪 3. 動作確認
python run.py
ブラウザで http://localhost:5000 を開いて、地図とグラフが表示されることを確認します。

⚙️ 4. systemd による自動起動設定（Raspberry Pi向け）
以下の systemd サービスファイルを作成します：
# /etc/systemd/system/gnss-imu.service

[Unit]
Description=GNSS IMU Visualizer Service
After=network.target

[Service]
ExecStart=/home/pi/gnss_imu_visualizer/venv/bin/python /home/pi/gnss_imu_visualizer/run.py
WorkingDirectory=/home/pi/gnss_imu_visualizer
Restart=always
User=pi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
有効化して起動：
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable gnss-imu
sudo systemctl start gnss-imu
ステータス確認：
sudo systemctl status gnss-imu
📡 5. センサ自動切替機能について
GNSS / IMU が接続されている場合、自動でリアルセンサが有効になります。
センサがない場合は自動的にシミュレーションに切り替わります。
UI 上に強制的に切り替えるトグルボタンも実装されています（map.js/index.html 参照）。
✅ 動作確認済み環境
Raspberry Pi 4 (Raspberry Pi OS)
Windows 10 + Python 3.10
macOS Ventura + Python 3.9
GNSS: u-blox Neo-M8P, M9N
IMU: MPU-6050 (I2C接続)
