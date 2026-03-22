document.getElementById('google-login-btn').addEventListener('click', () => {
  window.location.href = 'https://vault-storage.me/auth/login_google';
});
const pass = () => {};
window.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const sid = params.get('sid');
  const gmail = params.get('gmail');

  if (sid && gmail) {
    window.history.replaceState({}, document.title, window.location.pathname);
    await handleVerifyUID(sid, gmail);
  }

  async function handleVerifyUID(uidVal, emailVal) {
    try {
      const response = await fetch(
        'https://vault-storage.me/auth/google/verify_uid',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            uid: uidVal,
            gmail: emailVal,
          }),
        }
      );

      const data = await response.json();

      if (response.status === 200 && data.trang_thai) {
        alert(data.mes);
        window.location.href = 'https://vault-storage.medashboard';
      } else {
        alert('Lỗi: ' + data.mes);
        window.location.href = 'https://vault-storage.meauth/login';
      }
    } catch (error) {
      pass();
    }
  }
});
