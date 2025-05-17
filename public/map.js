// public/map.js

const map = L.map('map').setView([35.681236, 139.767125], 17);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © OpenStreetMap contributors'
}).addTo(map);

let marker = null;
let accuracyCircle = null;

// モード表示用ラベル
const statusEl = document.getElementById('status');
const headingEl = document.getElementById('heading');
const errorEl = document.getElementById('error');
const timestampEl = document.getElementById('timestamp');

// 切り替えボタン
const toggleBtn = document.getElementById('toggle-sensor');
let currentMode = 'auto'; // 'auto', 'real', 'sim'

toggleBtn.addEventListener('click', () => {
    if (currentMode === 'auto') {
        currentMode = 'real';
    } else if (currentMode === 'real') {
        currentMode = 'sim';
    } else {
        currentMode = 'auto';
    }
    socket.emit('force_mode', currentMode);
    toggleBtn.innerText = `Mode: ${currentMode.toUpperCase()}`;
});

const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('message', (data) => {
    const { lat, lon, heading, rtk_fix_type, error_radius, timestamp } = data;

    // マーカー描画
    if (!marker) {
        marker = L.marker([lat, lon], {
            rotationAngle: heading,
            rotationOrigin: 'center center'
        }).addTo(map);
    } else {
        marker.setLatLng([lat, lon]);
        marker.setRotationAngle(heading);
    }

    // 誤差円描画
    if (!accuracyCircle) {
        accuracyCircle = L.circle([lat, lon], {
            radius: error_radius,
            color: rtk_fix_type === 4 ? 'green' : 'red',
            fillOpacity: 0.2
        }).addTo(map);
    } else {
        accuracyCircle.setLatLng([lat, lon]);
        accuracyCircle.setRadius(error_radius);
        accuracyCircle.setStyle({
            color: rtk_fix_type === 4 ? 'green' : 'red'
        });
    }

    // ステータス表示
    statusEl.innerText = `RTK Mode: ${rtk_fix_type === 4 ? 'FIXED' : 'FLOAT/NONE'}`;
    headingEl.innerText = `Heading: ${heading.toFixed(1)}°`;
    errorEl.innerText = `Error Radius: ${error_radius.toFixed(2)} m`;
    timestampEl.innerText = `Timestamp: ${timestamp}`;
});
