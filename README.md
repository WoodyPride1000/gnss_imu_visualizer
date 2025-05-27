# GNSS-IMU 可視化システム

## 概要

GNSS-IMU 可視化システムは、GNSS（GPS）と IMU（慣性計測装置）センサーを用いて、リアルタイムで位置、方位、速度を可視化する Web ベースのシステムです。RTK-GNSS による高精度測位と IMU の方位データをカルマンフィルターで融合し、Leaflet.js ベースの地図、Chart.js によるグラフ、座標系変換、多言語対応を提供します。

---

## 特徴

- 📡 **GNSS + IMU センサー統合**：カルマンフィルターによる位置・方位の平滑化。
- 🧭 **リアルタイム可視化**：地図上に位置（マーカー）、軌跡（ポリライン）、方位（回転アイコン）を表示。
- 📈 **履歴グラフ**：エラーラディウス、RTK 状態（FIX/FLOAT/NONE）、衛星数の時系列表示。
- 🌐 **座標系変換**：緯度経度、MGRS、UTM、日本の平面直角座標系（I〜XIX）をサポート。
- 🌍 **多言語対応**：日本語と英語の UI 切り替え。
- 🧪 **センサー切り替え**：実センサー（RTK-GNSS, MPU6050）とシミュレータ（ダミーデータ）の自動/手動切り替え。
- 📱 **レスポンシブ UI**：スマートフォン・タブレット対応。
- 🛰 **センサー品質表示**：衛星数、エラーラディウス、RTK 状態をリアルタイム表示。
- ⚠️ **異常検出**：無効なデータ（例：緯度範囲外）や WebSocket 接続エラーを UI で警告。

---

## 構成

- `app.py`: Flask サーバーと WebSocket アプリケーション。
- `sensor.py`: GNSS センサー制御（実センサー/シミュレータ切り替え）。
- `imu_reader.py`: IMU センサー制御（実センサー/シミュレータ切り替え）。
- `kalman.py`: カルマンフィルターの実装。
- `templates/index.html`: UI ページ（地図、グラフ、座標変換、ステータス表示）。
- `docs/manual.html`: 取扱説明書（HTML 形式）。
- `requirements.txt`: 依存ライブラリ一覧。
- `LICENSE`: MIT ライセンス。
- `README.md`: このファイル。

クライアント側ライブラリ（CDN 経由）：
- Leaflet.js（地図）
- Chart.js（グラフ）
- Socket.IO（リアルタイム通信）
- proj4js, mgrs（座標変換）
- i18next（多言語対応）

---

## 動作環境

- Python 3.8 以上
- ハードウェア：PC または Raspberry Pi（実センサー使用時）
- センサー（オプション）：RTK-GNSS モジュール、MPU6050（IMU）
- ブラウザ：Chrome, Firefox, Safari（最新バージョン推奨）

---

## インストール手順

1. **リポジトリのクローン**：
   ```bash
   git clone https://github.com/WoodyPride1970/gnss_imu_visualizer.git
   cd gnss_imu_visualizer

---
##仮想環境の作成と有効化：


```bash

python -m venv venv
source venv/bin/activate  # Windows の場合は: venv\Scripts\activate


---

##依存ライブラリのインストール
```bash
pip install flask flask-socketio

---
##実センサー使用時（オプション）：
Raspberry Pi で MPU6050 を使用する場合：

```bash
sudo apt-get update
sudo apt-get install i2c-tools
pip install mpu6050-raspberrypi
---
##アプリケーションの起動：

```bash
python app.py

---
##使い方
詳細は docs/manual.html を参照してください。主な手順：
センサー接続：
RTK-GNSS モジュールと MPU6050 を接続（Raspberry Pi など）。

接続がない場合、自動でシミュレータモード（ダミーデータ）に切り替わる。
---
##UI 操作：
地図：現在位置（マーカー）、軌跡（ポリライン）、方位（回転アイコン）を表示。

座標系：緯度経度、MGRS、UTM、平面直角座標系を選択。

言語：日本語または英語を選択。

ステータス：位置、方位、速度、RTK 状態、エラーラディウス、衛星数を確認。

グラフ：エラーラディウス、RTK 状態、衛星数の履歴を表示（最大 60 ポイント）。

シミュレータモード：
sensor.py または imu_reader.py の forced_mode='dummy' を設定。

ダミーデータ（例：東京駅の位置）を使用。

---
注意事項
GNSS は屋外で使用してください。屋内では衛星信号が弱い場合があります。

IMU は使用前にキャリブレーションが必要です（ジャイロドリフト補正）。

平面直角座標系は現在位置に応じた測地系（例：東京なら VI）を選択してください。

WebSocket 接続が不安定な場合、ネットワーク環境を確認してください。

シミュレータモードでは固定データが使用されます。

