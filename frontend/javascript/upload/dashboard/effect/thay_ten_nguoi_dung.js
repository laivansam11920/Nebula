function getAvatarName(fullName) {
  if (!fullName) return 'Ano';
  const words = fullName.trim().split(/\s+/);
  const firstName = words.pop();
  return firstName.charAt(0).toUpperCase();
}

function renderProfile(username) {
  const char = getAvatarName(username);

  const nameTarget = document.querySelector('.am-name');
  if (nameTarget) nameTarget.textContent = username;

  const bigAvatar = document.querySelector('.am-avatar-big');
  if (bigAvatar) bigAvatar.innerText = char;

  const btnAvatar = document.getElementById('avatarBtn');
  if (btnAvatar) btnAvatar.innerText = char;
}

async function updateAdminName() {
  const cachedName = localStorage.getItem('user_name');
  if (cachedName) renderProfile(cachedName);

  try {
    const response = await fetch(
      'https://vault-storage.me/profile/get_profile',
      {
        method: 'GET',
        credentials: 'include',
      }
    );

    const data = await response.json();
    const mainAvatar = document.getElementById('avatarBtn');
    if (data.trang_thai && data.username) {
      if (!mainAvatar) {
        renderProfile(data.username);
        console.log('[LOG] Profile updated & cached!');
      }
      const nameTarget = document.querySelector('.am-name');
      if (nameTarget) nameTarget.textContent = data.username;
      document.title = `VAULT — ${data.username}'s Drive`;
      console.log('[LOG] Đã thay đổi tile thành' + data.username);
      localStorage.setItem('user_name', data.username);
    }
  } catch (err) {
    console.error('Lỗi fetch tên:', err);
  }
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', updateAdminName);
} else {
  updateAdminName();
}
