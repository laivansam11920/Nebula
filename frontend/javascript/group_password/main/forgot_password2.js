import { showToast } from 'https://cdn.jsdelivr.net/gh//gemini-dot/learnpythonserver-sm@main/frontend/javascript/popup/popup.js';

(function () {
  const socket = io('https://vault-storage.me/', {
    transports: ['polling', 'websocket'], // Cho phép cả hai
    withCredentials: true,
  });

  socket.on('global_notification', (data) => {
    console.log('📡 Đã nhận thông báo hệ thống:', data.message);

    if (typeof toast === 'function') {
      showToast('info', `THÔNG BÁO: ${data.message}`);
    } else {
      showToast('info', 'Thông báo hệ thống: ' + data.message);
    }
  });
  socket.on('connect_error', (err) => {
    console.error('❌ Lỗi kết nối Socket:', err.message);
  });

  socket.on('connect', () => {
    console.log('✅ Đã kết nối thành công với trạm phát sóng Python!');
  });
})();

async function secretMaintenanceCheck() {
  try {
    const response = await fetch('https://vault-storage.me/ping/khoi-dong');
    if (response.status === 503) {
      window.location.href = 'https://vault-storage.me/503';
    }
  } catch (error) {
    console.log('Server đang khởi động hoặc gặp sự cố kết nối.');
  }
}

secretMaintenanceCheck();

function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    gmail: params.get('gmail'),
    token: params.get('token'),
  };
}

async function verifyToken() {
  const { gmail, token } = getQueryParams();

  if (!gmail && !token) {
    return;
  }

  if (!gmail || !token) {
    showToast('error', 'Liên kết không hợp lệ.');
    return;
  }
  showToast('info', 'Đang xác thực liên kết...');

  const API_URL =
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1'
      ? 'http://localhost:5000' //server test ở nhà:)
      : 'https://vault-storage.me/';

  try {
    const response = await fetch(
      `${API_URL}/auth/tim-mat-khau2?gmail=${gmail}&token=${token}`,
      {
        method: 'GET',
      }
    );

    const data = await response.json();

    if (response.ok && data.success) {
      console.log('Xác thực token thành công! Giờ cho phép đổi pass.');
      window.location.href =
        'https://vault-storage.me/auth/reset_site?gmail=' +
        encodeURIComponent(gmail) +
        '&token=' +
        encodeURIComponent(token);
    } else {
      showToast(
        'error',
        'Lỗi rồi: ' + (data.message || 'Token hết hạn hoặc không đúng!')
      );
    }
  } catch (error) {
    console.error('Lỗi:', error);
    showToast('error', 'Không kết nối được server!');
  }
} //
window.onload = verifyToken;
