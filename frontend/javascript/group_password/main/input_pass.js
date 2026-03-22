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
      window.location.href = 'https://vault-storage.me/503'; // Chuyển hướng sang trang bảo trì
    }
  } catch (error) {
    console.log('Server đang khởi động hoặc gặp sự cố kết nối.');
  }
}

secretMaintenanceCheck();

function isMobileDevice() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}
// Thêm const vào trước các biến để khai báo nè og
const userpass = document.getElementById('password');
const useremail = document.getElementById('email');
const formDangNhap = document.getElementById('dang-nhap'); // Đổi tên cho đỡ nhầm với nút bấm

if (formDangNhap) {
  formDangNhap.addEventListener('submit', function (event) {
    // Chặn hành động reload mặc định của form
    event.preventDefault();

    showToast('info', 'Đang gửi xác thực...');

    const lay_gia_tri_pass = userpass.value;
    const lay_gia_tri_user = useremail.value;

    const goi_du_lieu = {
      gmail: lay_gia_tri_user,
      password: lay_gia_tri_pass,
    };

    console.log('Đang gửi dữ liệu:', goi_du_lieu);

    const API_URL =
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000' //server test ở nhà:)
        : 'https://vault-server-laivansam-gnfdcsgthfhraahe.eastasia-01.azurewebsites.net'; //

    fetch(`${API_URL}/auth/input-pass`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(goi_du_lieu),
    })
      .then((response) => {
        if (response.status === 200) {
          return response.json().then((data) => {
            showToast(
              'success',
              'Đăng nhập thành công! Chào mừng bạn quay trở lại.'
            );
            localStorage.setItem('user_email', lay_gia_tri_user);
            setTimeout(() => {
              if (isMobileDevice()) {
                window.location.href = `https://vault-storage.me/frontend/view/upload/dashboard/dashboard-mobile.html?useraccount=${lay_gia_tri_user}`;
              } else {
                window.location.href = `https://vault-storage.me/dashboard?useraccount=${lay_gia_tri_user}`;
              }
            }, 2000);
          });
        } else if (response.status === 401) {
          return response.json().then((data) => {
            showToast(
              'error',
              'Thất bại: ' + (data.message || 'Sai tài khoản hoặc mật khẩu!')
            );
          });
        } else {
          showToast('error', `Lỗi hệ thống: Mã lỗi ${response.status}`);
        }
      })
      .catch((error) => {
        console.error('Lỗi kết nối mạng rồi bạn ơi:', error);
        showToast('error', `Lỗi kết nối mạng rồi bạn ơi: ${error}`);
      });
  });
}
