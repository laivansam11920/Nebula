import { showToast } from 'https://purge.jsdelivr.net/gh//gemini-dot/learnpythonserver-sm@main/frontend/javascript/popup/popup.js';

(function () {
  const socket = io(
    'https://vault-server-laivansam-gnfdcsgthfhraahe.eastasia-01.azurewebsites.net',
    {
      transports: ['polling', 'websocket'], // Cho phép cả hai
      withCredentials: true,
    }
  );

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
    const response = await fetch(
      'https://vault-server-laivansam-gnfdcsgthfhraahe.eastasia-01.azurewebsites.net/ping/khoi-dong'
    );
    if (response.status === 503) {
      window.location.href = 'https://vault-storage.me/503';
    }
  } catch (error) {
    console.log('Server đang khởi động hoặc gặp sự cố kết nối.');
  }
}

secretMaintenanceCheck();

document.addEventListener('DOMContentLoaded', function () {
  const signupForm = document.getElementById('main-signup-form');

  if (signupForm) {
    signupForm.addEventListener('submit', function (event) {
      // CHẶN reset trang ngay lập tức
      event.preventDefault();
      handleSignup(event);
    });
  }
});

function handleSignup(event) {
  const firstname = document.getElementById('firstname').value;
  const lastname = document.getElementById('lastname').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm-password').value;
  const terms = document.getElementById('terms').checked;

  if (!firstname || !lastname || !email || !password || !confirmPassword) {
    showToast('error', 'Vui lòng điền đầy đủ thông tin');
    return;
  }

  if (password !== confirmPassword) {
    showToast('error', 'Mật khẩu xác nhận không khớp');
    return;
  }

  if (!terms) {
    showToast('error', 'Vui lòng đồng ý với điều khoản dịch vụ');
    return;
  }

  const fullname = firstname + ' ' + lastname;
  const goi_du_lieu = {
    username: fullname,
    gmail: email,
    password: password,
  };

  showToast('info', 'Đang gửi yêu cầu...');
  console.log('Đang gửi dữ liệu:', goi_du_lieu);

  const API_URL =
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1'
      ? 'http://localhost:5000' //server test ở nhà:)
      : 'https://vault-server-laivansam-gnfdcsgthfhraahe.eastasia-01.azurewebsites.net';

  fetch(`${API_URL}/auth/create-a-pass`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(goi_du_lieu),
  })
    .then((response) => {
      return response.json().then((data) => {
        if (response.ok) {
          showToast('success', `Đăng ký thành công! Chào mừng ${fullname}`);
        } else {
          showToast('error', 'Lỗi: ' + (data.message || 'Có lỗi xảy ra'));
        }
      });
    })
    .catch((error) => {
      console.log('Lỗi kết nối', error);
      showToast('error', `Lỗi kết nối ${error}`);
    });
} //
