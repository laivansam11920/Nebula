function toggleDark() {
  const t = document.getElementById('darkToggle');
  const on = t.classList.toggle('on');
  const set = (k, dark, light) =>
    document.documentElement.style.setProperty(k, on ? dark : light);
  set('--bg', '#111111', '#f5f5f3');
  set('--surface', '#1a1a1a', '#ffffff');
  set('--border', '#2a2a2a', '#e0e0de');
  set('--border-dark', '#3a3a3a', '#c0c0be');
  set('--ink', '#30302d', '#0a0a0a');
  set('--ink-2', '#ffffffc5', '#333332');
  set('--ink-3', '#ffffff', '#666664');
  set('--ink-4', '#ffffff', '#999997');
  set('--ink-5', '#161616', '#1d1d1d');
  set('--ink-6', '#242424', '#ffffff');
  set('--ink-7', '#ffffff', '#000000');
  set('--ink-8', '#ffffff', '#000000');
  set('--ink-9', '#ffffff', '#000000')
  toast(on ? '🌙 Giao diện tối đã bật' : '☀️ Giao diện sáng đã bật');
}
// nhiều thế