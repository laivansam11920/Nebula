function toggleLogoutModal(show) {
  console.log('[DEBUG] Hàm toggle được gọi với giá trị:', show); // Xem trong F12 Console
  const modal = document.getElementById('logoutModal');

  if (!modal) {
    console.error('Không tìm thấy cái bảng có id là logoutModal rồi og ơi!');
    return;
  }

  if (show === true) {
    modal.style.setProperty('display', 'flex', 'important');
  } else {
    modal.style.setProperty('display', 'none', 'important');
  }
}

async function confirmLogout() {
  console.log('Đã xác nhận đăng xuất!');
  try {
    const response = await fetch('https://vault-storage.me/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Server phản hồi nè og:', data);
      localStorage.clear();
      sessionStorage.clear();
      toast('Đã đăng xuất thành công! :)');
      window.location.href = 'https://vault-storage.me';
    } else {
      console.error('Lỗi server, mã lỗi:', response.status);
      window.location.reload();
    }
  } catch (error) {
    console.error('Không kết nối được tới server:', error);
    window.location.reload();
  }
}
