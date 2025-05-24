class MapController {
  constructor(mapElementId) {
    this.map = L.map(mapElementId).setView([35.681236, 139.767125], 15); // 初期位置: 東京駅
    this.pathPoints = [];
    this.marker = null;
    this.polyline = L.polyline([], { color: 'blue' }).addTo(this.map);

    this._initTileLayer();
  }

  _initTileLayer() {
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);
  }

  updatePosition(lat, lon, headingDeg) {
    const newLatLng = [lat, lon];
    this.pathPoints.push(newLatLng);

    if (this.marker) {
      this.marker.setLatLng(newLatLng);
      this.marker.setRotationAngle(headingDeg); // 追加: ヘディング反映
    } else {
      this.marker = L.marker(newLatLng, {
        icon: this._createHeadingIcon(),
        rotationAngle: headingDeg,
        rotationOrigin: 'center'
      }).addTo(this.map);
    }

    this.polyline.setLatLngs(this.pathPoints);
    this.map.setView(newLatLng);
  }

  _createHeadingIcon() {
    return L.divIcon({
      html: '▲',
      iconSize: [20, 20],
      className: 'heading-icon',
      iconAnchor: [10, 10],
      tooltipAnchor: [0, -10]
    });
  }
}

// ツールチップの国際化
function updateStatus(data) {
  const status = `
    <strong>${i18next.t("latitude")}:</strong> ${data.lat}<br>
    <strong>${i18next.t("longitude")}:</strong> ${data.lon}<br>
    <strong>${i18next.t("heading")}:</strong> ${data.heading.toFixed(1)}°<br>
    <strong>${i18next.t("velocity")}:</strong> ${data.velocity.toFixed(2)} m/s
  `;
  document.getElementById("status").innerHTML = status;
}

// 初期化
const mapController = new MapController("map");
const socket = io();

socket.on("sensor_data", (data) => {
  const { lat, lon, heading, velocity } = data;
  if (!lat || !lon) return;

  mapController.updatePosition(lat, lon, heading);
  updateStatus(data);
});
