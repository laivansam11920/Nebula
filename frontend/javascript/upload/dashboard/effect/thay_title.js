function transformNameForLogo(fullName) {
  if (!fullName || fullName === 'Anonymous') return 'MY';
  const nameParts = fullName.trim().split(/\s+/);
  let lastName = nameParts[nameParts.length - 1];

  lastName = lastName
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D');
  return lastName.toUpperCase();
}
async function syncLogoWithName() {
  try {
    const response = await fetch(
      'https://vault-storage.me/profile/get_profile',
      {
        method: 'GET',
        credentials: 'include',
      }
    );

    const data = await response.json();

    if (data.trang_thai && data.username) {
      const finalName = transformNameForLogo(data.username);

      const logoEl = document.querySelector('.logo');
      if (logoEl) {
        logoEl.innerHTML = `${finalName} <span>files</span>`;
      }
    }
  } catch (error) {
    console.error('Lỗi khi đồng bộ tên Logo:', error);
  }
}

syncLogoWithName();
