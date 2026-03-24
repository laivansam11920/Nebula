(function () {
  const socket = io('https://vault-storage.me/', {
    transports: ['polling', 'websocket'], // Cho phép cả hai
    withCredentials: true,
  });

  socket.on('global_notification', (data) => {
    pass();

    if (typeof toast === 'function') {
      toast(`THÔNG BÁO: ${data.message}`);
    } else {
      toast('Thông báo hệ thống: ' + data.message);
    }
  });
  socket.on('connect_error', (err) => {
    pass();
  });

  socket.on('connect', () => {
    pass();
  });
})();
const pass = () => {};
const urlParams = new URLSearchParams(window.location.search);
const userName = urlParams.get('useraccount');
if (userName) {
  const cleanName = decodeURIComponent(userName);
  toast(`chào mừng ${cleanName}`);
}
async function secretMaintenanceCheck() {
  try {
    const response = await fetch('https://vault-storage.me/ping/khoi-dong');
    if (response.status === 503) {
      window.location.replace('https://vault-storage.me/503');
    }
  } catch (error) {
    pass();
  }
}

secretMaintenanceCheck();

function updateMainAvatar(dataURL) {
  const mainAvatar = document.getElementById('avatarBtn');
  if (mainAvatar) {
    mainAvatar.innerHTML = `<img src="${dataURL}" style="width:100%;height:100%;object-fit:cover;border-radius:50%">`;
  }

  const bigAvatar = document.querySelector('.am-avatar-big');
  if (bigAvatar) {
    bigAvatar.innerHTML = `<img src="${dataURL}" style="width:100%;height:100%;object-fit:cover;border-radius:50%">`;
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const previewElement = document.getElementById('avatarPreview');
  const localAvatar = localStorage.getItem('user_avatar');

  if (localAvatar && previewElement) {
    previewElement.innerHTML = `<img src="${localAvatar}" alt="Avatar">`;
    updateMainAvatar(localAvatar);
  }

  try {
    const response = await fetch(
      'https://vault-storage.me/profile/get_avatar',
      {
        credentials: 'include',
      }
    );
    const data = await response.json();

    if (data.trang_thai === true && data.url !== localAvatar) {
      if (previewElement) {
        previewElement.innerHTML = `<img src="${data.url}" alt="Avatar">`;
      }
      updateMainAvatar(data.url);
      localStorage.setItem('user_avatar', data.url);
    }
  } catch (error) {
    pass();
  }
});

async function checkAccess() {
  try {
    const response = await fetch('https://vault-storage.me/security/upload', {
      method: 'POST',
      credentials: 'include',
    });

    const data = await response.json();

    if (response.status === 200) {
      toast('thành công! Chào mừng bạn quay trở lại.');
    } else {
      window.location.replace('https://vault-storage.me/401');
    }
  } catch (error) {
    window.location.replace('https://vault-storage.me/500');
  }
}
function chayLenhQuet() {
  fetch('https://vault-storage.me/security/scan_malware', {
    method: 'GET',
    credentials: 'include',
  }).catch((err) => pass());
  pass();
}
checkAccess();
chayLenhQuet();

const sampleFiles = []; // Bắt đầu rỗng, sẽ được fill bởi loadFilesFromServer()
const trashFiles = [];
let isProcessing = false;
let files = [...sampleFiles]; // Không dùng nữa, giữ để tương thích
let selectedId = null;
let viewMode = 'grid';
let searchQuery = ''; // chuỗi tìm kiếm hiện tại
let activeFilter = 'all'; // filter từ nav: 'all','img','doc','vid','pdf','zip','today','fav','trash','shared'
// ─── HÀM LỌC TRUNG TÂM ───────────────────────────────────────────
// Luôn lọc từ sampleFiles gốc, kết hợp filter + search cùng lúc
function getFilteredFiles() {
  const today = new Date().toLocaleDateString('vi-VN');
  let result = [...sampleFiles];

  // 1. Lọc theo category nav
  switch (activeFilter) {
    case 'img':
      result = result.filter((f) => f.type === 'img');
      break;
    case 'doc':
      result = result.filter((f) => f.type === 'doc');
      break;
    case 'vid':
      result = result.filter((f) => f.type === 'vid');
      break;
    case 'pdf':
      result = result.filter((f) => f.type === 'pdf');
      break;
    case 'zip':
      result = result.filter((f) => f.type === 'zip');
      break;
    case 'today':
      result = result.filter((f) => f.date === today);
      break;
    case 'fav':
      const currentFavs = getFavorites();
      // Lọc những file có mã định danh nằm trong danh sách yêu thích
      result = result.filter((f) => currentFavs.includes(f.ma_dinh_danh));
      break;
    case 'trash':
      result = [...trashFiles];
      break; // demo: thùng rác trống
    case 'shared':
      result = [];
      break; // demo: chưa chia sẻ
    default:
      break; // 'all' — giữ nguyên
  }

  // 2. Lọc thêm theo search query (tên file + ext)
  if (searchQuery.trim()) {
    const q = searchQuery.trim().toLowerCase();
    result = result.filter(
      (f) => f.name.toLowerCase().includes(q) || f.ext.toLowerCase().includes(q)
    );
  }
  return result;
}

// ─── SIDEBAR / PANEL STATE ────────────────────────────────────────
const app = document.getElementById('app');
const sidebar = document.getElementById('sidebar');
const panel = document.getElementById('panel');

let leftOpen = false;
let rightOpen = false;
let leftCloseTimer, rightCloseTimer;
const CLOSE_DELAY = 580; // ms chờ trước khi đóng, tránh giật khi di nhanh

function openLeft() {
  clearTimeout(leftCloseTimer);
  if (leftOpen) return;
  leftOpen = true;
  sidebar.classList.add('open');
  app.classList.add('left-open');
  const chevron = document.getElementById('sidebarChevron');
  if (chevron) chevron.style.transform = 'rotate(180deg)';
}
function closeLeft() {
  leftCloseTimer = setTimeout(() => {
    leftOpen = false;
    sidebar.classList.remove('open');
    app.classList.remove('left-open');
    const chevron = document.getElementById('sidebarChevron');
    if (chevron) chevron.style.transform = 'rotate(0deg)';
  }, CLOSE_DELAY);
}

function openRight() {
  clearTimeout(rightCloseTimer);
  if (rightOpen) return;
  rightOpen = true;
  panel.classList.add('open');
  app.classList.add('right-open');
}

function closeRight() {
  rightCloseTimer = setTimeout(() => {
    if (isProcessing) return; // Nếu đang bận thì không đóng panel
    rightOpen = false;
    panel.classList.remove('open');
    app.classList.remove('right-open');
  }, CLOSE_DELAY);
}
const FAVORITES_KEY = 'vault_favorites_list';

function getFavorites() {
  const favs = localStorage.getItem(FAVORITES_KEY);
  return favs ? JSON.parse(favs) : [];
}

function updateFavoriteButton(id) {
  const favoritePanelText = document.getElementById('favoritePanelText');
  if (!favoritePanelText) return;

  const favs = getFavorites(); // Lấy mảng ID từ localStorage
  // Tìm thông tin file từ ID để lấy mã định danh (ma_dinh_danh)
  const f = sampleFiles.find((x) => x.id === id);

  if (f && favs.includes(f.ma_dinh_danh)) {
    favoritePanelText.textContent = 'Bỏ yêu thích';
  } else {
    favoritePanelText.textContent = 'Yêu thích';
  }
}

function toggleFavorite() {
  if (!selectedId) {
    toast('Vui lòng chọn một file để yêu thích!');
    return;
  }
  const f = sampleFiles.find((x) => x.id === selectedId);
  if (!f) return;
  let favs = getFavorites();
  const index = favs.indexOf(f.ma_dinh_danh);
  if (index > -1) {
    favs.splice(index, 1);
    toast('☆ Đã xóa khỏi yêu thích');
  } else {
    favs.push(f.ma_dinh_danh);
    toast('⭐ Đã thêm vào yêu thích');
  }
  localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs));
  renderFiles();
  updateFavoriteButton(selectedId);
}

// Hover events — sidebar trái
sidebar.addEventListener('mouseenter', openLeft);
sidebar.addEventListener('mouseleave', closeLeft);

// Hover events — panel phải
panel.addEventListener('mouseenter', openRight);
panel.addEventListener('mouseleave', () => {
  if (!isProcessing) {
    closeRight();
  }
});

// toggleLeft/toggleRight vẫn giữ để các nút bên trong có thể gọi
function toggleLeft() {
  leftOpen ? closeLeft() : openLeft();
  clearTimeout(leftCloseTimer); // nếu click thì không delay
  leftOpen = !sidebar.classList.contains('open');
  // force immediate
  if (!leftOpen) {
    sidebar.classList.remove('open');
    app.classList.remove('left-open');
    const chevron = document.getElementById('sidebarChevron');
    if (chevron) chevron.style.transform = 'rotate(0deg)';
  }
}
function toggleRight() {
  if (rightOpen) {
    clearTimeout(rightCloseTimer);
    rightOpen = false;
    panel.classList.remove('open');
    app.classList.remove('right-open');
  } else {
    openRight();
  }
}

// ─── RENDER FILES ─────────────────────────────────────────────────
function renderFiles() {
  const container = document.getElementById('fileContainer');
  const titleEl = document.querySelector('#filesArea .section-title');
  container.innerHTML = '';

  const filtered = getFilteredFiles();

  // Cập nhật tiêu đề section
  if (searchQuery.trim()) {
    if (titleEl)
      titleEl.textContent = `Kết quả tìm kiếm "${searchQuery.trim()}"`;
  } else {
    const labels = {
      all: 'Tất cả',
      img: 'Hình ảnh',
      doc: 'Tài liệu',
      vid: 'Video',
      pdf: 'PDF',
      zip: 'Lưu trữ',
      today: 'Hôm nay',
      fav: 'Yêu thích',
      trash: 'Thùng rác',
      shared: 'Chia sẻ',
    };
    if (titleEl) titleEl.textContent = labels[activeFilter] || 'Tất cả';
  }

  // Empty state
  // Empty state (Cập nhật giao diện trống đẹp mắt)
  if (filtered.length === 0) {
    container.className = '';

    if (searchQuery.trim()) {
      // 1. Trạng thái: Tìm kiếm không có kết quả
      container.innerHTML = `
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center; gap:12px;padding:80px 24px;text-align:center;">
          <div style="width:72px;height:72px;background:rgba(10,10,10,0.04);border-radius:50%;display:flex;align-items:center;justify-content:center;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--ink-4)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </div>
          <div style="font-size:15px;font-weight:700;color:var(--ink);font-family:'Manrope',sans-serif;margin-top:8px;">
            Không tìm thấy "${searchQuery.trim()}"
          </div>
          <div style="font-size:13px;color:var(--ink-4);">
            Hãy thử dùng từ khóa khác hoặc kiểm tra lại lỗi chính tả.
          </div>
        </div>`;
    } else if (activeFilter === 'trash') {
      // 2. Trạng thái: Thùng rác trống
      container.innerHTML = `
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center; gap:12px;padding:80px 24px;text-align:center;">
          <div style="width:72px;height:72px;background:rgba(192,48,48,0.08);border-radius:50%;display:flex;align-items:center;justify-content:center;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#c03030" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"></path>
            </svg>
          </div>
          <div style="font-size:15px;font-weight:700;color:var(--ink);font-family:'Manrope',sans-serif;margin-top:8px;">
            Thùng rác trống
          </div>
          <div style="font-size:13px;color:var(--ink-4);">
            Những file bạn xóa sẽ nằm ở đây trước khi bị xóa vĩnh viễn.
          </div>
        </div>`;
    } else {
      // 3. Trạng thái: Thư mục chưa có file (Call-to-Action)
      container.innerHTML = `
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center; gap:12px;padding:80px 24px;text-align:center;">
          <!-- Vòng tròn nền đứt nét chứa Icon hộp giấy -->
          <div style="width:88px;height:88px;background:rgba(10,10,10,0.02);border: 2px dashed rgba(10,10,10,0.15); border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:8px;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--ink-3)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <div style="font-size:16px;font-weight:700;color:var(--ink);font-family:'Manrope',sans-serif;">
            Mục này đang trống
          </div>
          <div style="font-size:13px;color:var(--ink-4);max-width:280px;line-height:1.6;">
            Bạn chưa có file nào ở đây. Hãy tải lên tài liệu đầu tiên để bắt đầu lưu trữ nhé!
          </div>
          <!-- Nút bấm nổi bật (Tương tác gọi thẳng input tải file) -->
          <button onclick="window.location.href='https://www.vault-storage.me/frontend/view/upload/web_upload/index.html'"
                  style="margin-top:16px;padding:10px 24px;background:var(--ink);color:#fff;border:none;border-radius:8px;font-weight:600;font-size:13px;font-family:'Manrope',sans-serif;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: all 0.2s;"
                  onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(0,0,0,0.2)';"
                  onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)';">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            Tải file lên ngay
          </button>
        </div>`;
    }

    updateSelCount(0);
    return;
  }
  if (viewMode === 'grid') {
    container.className = 'file-grid';
    filtered.forEach((f, i) => {
      const div = document.createElement('div');
      div.className = 'file-card' + (selectedId === f.id ? ' selected' : '');

      // Kiểm tra nếu là ảnh thì dùng URL, nếu không thì dùng màu thumb mặc định
      const bgStyle =
        f.type === 'img' && f.url
          ? `background-image: url('${f.url}'); background-size: cover; background-position: center;`
          : `background: ${f.thumb}`;

      // Nếu là ảnh thì không hiện Emoji đè lên (hoặc hiện nhỏ lại), tùy og thích
      const content =
        f.type === 'img' && f.url
          ? ''
          : `<span style="font-size:32px">${f.emoji}</span>`;

      div.innerHTML = `
    <div class="file-thumb type-${f.type}" style="${bgStyle}">
      ${content}
    </div>
    <div class="file-name" title="${f.name}">${highlight(f.name, searchQuery)}</div>
    <div class="file-meta">${f.ext} · ${f.size}</div>
  `;
      div.onclick = () => selectFile(f.id);
      container.appendChild(div);
    });
  } else {
    container.className = 'file-list';
    filtered.forEach((f, i) => {
      const div = document.createElement('div');
      div.className = 'file-row' + (selectedId === f.id ? ' selected' : '');
      div.style.animationDelay = i * 0.03 + 's';

      // Tạo logic kiểm tra ảnh giống như bên Grid Mode
      const isImg = f.type === 'img' && f.url;
      const rowBgStyle = isImg
        ? `background-image: url('${f.url}'); background-size: cover; background-position: center;`
        : `background: ${f.thumb}`;
      const rowContent = isImg ? '' : f.emoji;

      div.innerHTML = `
        <div class="row-icon" style="${rowBgStyle}">${rowContent}</div>
        <div class="row-name">${highlight(f.name, searchQuery)}</div>
        <div class="row-type">${f.ext}</div>
        <div class="row-size">${f.size}</div>
        <div class="row-date">${f.date}</div>
      `;
      div.onclick = () => selectFile(f.id);
      container.appendChild(div);
    });
  }

  updateSelCount(filtered.length);
  updateStats(); // Cập nhật stats cards
  updateBadges();
}

// Highlight từ khóa trong tên file
function highlight(text, query) {
  if (!query.trim()) return text;
  const escaped = query.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return text.replace(
    new RegExp(`(${escaped})`, 'gi'),
    '<mark style="background:rgba(10,10,10,0.12);border-radius:2px;padding:0 1px;">$1</mark>'
  );
}

// ─── SELECT FILE ──────────────────────────────────────────────────
function selectFile(id) {
  selectedId = selectedId === id ? null : id;
  renderFiles();

  const f =
    sampleFiles.find((x) => x.id === id) || trashFiles.find((x) => x.id === id);
  const panelEmpty = document.getElementById('panelEmpty');
  const panelContent = document.getElementById('panelContent');
  const panelActions = document.getElementById('panelActions');

  if (!f || selectedId === null) {
    panelEmpty.style.display = 'flex';
    panelContent.style.display = 'none';
    panelActions.style.display = 'none';
    document.getElementById('panelTitle').textContent = 'Chi tiết file';
    document.getElementById('panelSub').textContent = 'Chọn một file để xem';
    return;
  }

  const previewEl = document.getElementById('previewThumb');
  const isImg = f.type === 'img' && f.url;
  if (isImg) {
    previewEl.innerHTML = '';
    previewEl.style.backgroundImage = `url('${f.url}')`;
    previewEl.style.backgroundSize = 'cover';
    previewEl.style.backgroundPosition = 'center';
  } else {
    previewEl.innerHTML = `<span style="font-size:60px">${f.emoji}</span>`;
    previewEl.style.backgroundImage = 'none';
    previewEl.style.background = f.thumb;
  }
  panelEmpty.style.display = 'none';
  panelContent.style.display = 'flex';
  panelActions.style.display = 'flex';

  document.getElementById('panelSub').textContent = f.ext + ' · ' + f.size;
  document.getElementById('detName').textContent = f.name;
  document.getElementById('detType').textContent = f.ext;
  document.getElementById('detSize').textContent = f.size;
  document.getElementById('detDate').textContent = f.date;
  document.getElementById('detRes').textContent = f.res;
  document.getElementById('detPath').textContent = '/vault/uploads/' + f.name;

  if (!rightOpen) openRight();

  const isTrashMode =
    (typeof activeFilter !== 'undefined' && activeFilter === 'trash') ||
    f.deleted;

  const favBtn = document.getElementById('favoritePanelBtn');
  const normalActions = document.getElementById('normalActions');
  const trashActions = document.getElementById('trashActions');
  const dateLabel = document.getElementById('detDateLabel');

  if (isTrashMode) {
    if (favBtn) favBtn.style.display = 'none';
    if (normalActions) normalActions.style.display = 'none';
    if (trashActions) trashActions.style.display = 'block';
    if (dateLabel) dateLabel.textContent = 'Ngày xóa';
  } else {
    if (favBtn) favBtn.style.display = 'block';
    if (normalActions) normalActions.style.display = 'block';
    if (trashActions) trashActions.style.display = 'none';
    if (dateLabel) dateLabel.textContent = 'Ngày tải';
    updateFavoriteButton(f.id);
  }
}

// ─── VIEW MODE ────────────────────────────────────────────────────
function setView(mode) {
  viewMode = mode;
  document
    .getElementById('gridBtn')
    .classList.toggle('active', mode === 'grid');
  document
    .getElementById('listBtn')
    .classList.toggle('active', mode === 'list');

  const area = document.getElementById('filesArea');
  area.style.opacity = '0';
  area.style.transform = 'translateY(6px)';
  setTimeout(() => {
    renderFiles();
    area.style.opacity = '1';
    area.style.transform = 'translateY(0)';
  }, 150);
}

const filesArea = document.getElementById('filesArea');
filesArea.style.transition = 'opacity 0.2s, transform 0.25s';

// ─── NAV / FILTER ─────────────────────────────────────────────────
function setNav(el) {
  // Đổi active state
  document
    .querySelectorAll('.nav-item')
    .forEach((e) => e.classList.remove('active'));
  el.classList.add('active');

  // Lấy filter từ data-filter attribute
  activeFilter = el.dataset.filter || 'all';

  // Reset selection khi đổi filter
  selectedId = null;

  // Re-render với filter mới
  renderFiles();
  updateStats();
  // Reset panel về trạng thái trống
  const panelEmpty = document.getElementById('panelEmpty');
  const panelContent = document.getElementById('panelContent');
  const panelActions = document.getElementById('panelActions');
  if (panelEmpty) panelEmpty.style.display = 'flex';
  if (panelContent) panelContent.style.display = 'none';
  if (panelActions) panelActions.style.display = 'none';
  const titleEl = document.getElementById('panelTitle');
  const subEl = document.getElementById('panelSub');
  if (titleEl) titleEl.textContent = 'Chi tiết file';
  if (subEl) subEl.textContent = 'Chọn một file để xem';
}

// ─── SELECTION COUNT ──────────────────────────────────────────────
function updateSelCount(total) {
  const count = total !== undefined ? total : getFilteredFiles().length;
  const sel = selectedId ? 1 : 0;
  document.getElementById('selCount').textContent = sel
    ? `${sel} file đã chọn`
    : `${count} file`;
  document.getElementById('deleteSelBtn').style.display = sel ? 'flex' : 'none';
}

async function deleteSelected() {
  if (!selectedId) return;

  // 1. Tìm file đang được chọn trong sampleFiles
  const fileIdx = sampleFiles.findIndex((f) => f.id === selectedId);

  if (fileIdx !== -1) {
    const deletedFile = sampleFiles[fileIdx];
    const ma_de_xoa = deletedFile.ma_dinh_danh;
    try {
      const response = await fetch(
        'https://vault-storage.me/profile/deletefile_user',
        {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ma_dinh_danh_file: ma_de_xoa,
          }),
        }
      );
      const data = await response.json();
      if (response.ok) {
        trashFiles.push(deletedFile);
        sampleFiles.splice(fileIdx, 1);
        selectedId = null;
        renderFiles();
        toast(`Đã chuyển "${deletedFile.name}" vào thùng rác`);
      } else {
        toast(`Lỗi: ${data.mes || 'Không thể xóa file'}`);
      }
    } catch (error) {
      toast('Lỗi kết nối server, thử lại sau nhé og!');
    } finally {
      toast('ok');
    }
  }
}
async function restoreFile() {
  if (!selectedId) return;

  const fileIdx = trashFiles.findIndex((f) => f.id === selectedId);

  if (fileIdx !== -1) {
    const fileToRestore = trashFiles[fileIdx];
    const ma_dinh_danh = fileToRestore.ma_dinh_danh;

    try {
      const response = await fetch(
        'https://vault-storage.me/profile/restorefile_user',
        {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ma_dinh_danh_file: ma_dinh_danh }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        sampleFiles.unshift(fileToRestore);
        trashFiles.splice(fileIdx, 1);

        selectedId = null; // Bỏ chọn sau khi khôi phục
        renderFiles();
        toast(`Đã khôi phục "${fileToRestore.name}"`);
      } else {
        toast(`Lỗi: ${data.mes || 'Không thể khôi phục'}`);
      }
    } catch (error) {
      toast('Lỗi kết nối server rồi og ơi!');
    }
  }
}
// ─── XÓA VĨNH VIỄN ────────────────────────────────────────────────
async function permanentDelete() {
  if (!selectedId) return;

  const fileIdx = trashFiles.findIndex((f) => f.id === selectedId);
  if (fileIdx === -1) return;

  const fileToDelete = trashFiles[fileIdx];

  // Hỏi lại cho chắc, tránh bấm nhầm
  if (!confirm(`Ông có chắc muốn xóa vĩnh viễn "${fileToDelete.name}" không?`))
    return;

  try {
    const response = await fetch(
      'https://vault-storage.me/profile/permanent_delete_user',
      {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ma_dinh_danh_file: fileToDelete.ma_dinh_danh }),
      }
    );

    if (response.ok) {
      // Xóa hẳn khỏi mảng rác
      trashFiles.splice(fileIdx, 1);
      selectedId = null;
      renderFiles();
      toast(`Đã xóa vĩnh viễn "${fileToDelete.name}"`);
    } else {
      const data = await response.json();
      toast(`Lỗi: ${data.mes || 'Không thể xóa vĩnh viễn'}`);
    }
  } catch (error) {
    toast('Server có vấn đề, thử lại sau nhé!');
  }
}
// ─── UPLOAD MODAL ─────────────────────────────────────────────────
let queuedFiles = [];

function openModal() {
  document.getElementById('uploadModal').classList.add('open');
}
function closeModal() {
  document.getElementById('uploadModal').classList.remove('open');
  queuedFiles = [];
  document.getElementById('uploadQueue').innerHTML = '';
}
document.getElementById('uploadModal').addEventListener('click', (e) => {
  if (e.target === document.getElementById('uploadModal')) closeModal();
});

function handleFiles(fl) {
  queuedFiles = Array.from(fl);
  const q = document.getElementById('uploadQueue');
  q.innerHTML = '';
  queuedFiles.forEach((f) => {
    const size =
      f.size > 1048576
        ? (f.size / 1048576).toFixed(1) + ' MB'
        : (f.size / 1024).toFixed(0) + ' KB';
    const div = document.createElement('div');
    div.className = 'queue-item';
    div.innerHTML = `
      <span style="font-size:18px">${getEmoji(f.name)}</span>
      <span class="queue-name">${f.name}</span>
      <span class="queue-size">${size}</span>
    `;
    q.appendChild(div);
  });
}

function getEmoji(name) {
  const ext = name.split('.').pop().toLowerCase();
  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext)) return '🖼️';
  if (['pdf'].includes(ext)) return '📄';
  if (['mp4', 'mov', 'avi', 'mkv'].includes(ext)) return '🎬';
  if (['zip', 'tar', 'gz', 'rar'].includes(ext)) return '📦';
  if (['doc', 'docx'].includes(ext)) return '📝';
  if (['xls', 'xlsx', 'csv'].includes(ext)) return '📊';
  if (['ppt', 'pptx'].includes(ext)) return '📋';
  return '📁';
}

function startUpload() {
  if (queuedFiles.length === 0) {
    simulateUpload([
      {
        name: 'demo-file.png',
        size: '2.4 MB',
        ext: 'PNG',
        type: 'img',
        thumb: '#f0ece8',
        emoji: '🖼️',
        res: '1920×1080',
      },
    ]);
    return;
  }
  const items = queuedFiles.map((f, i) => {
    const size =
      f.size > 1048576
        ? (f.size / 1048576).toFixed(1) + ' MB'
        : (f.size / 1024).toFixed(0) + ' KB';
    const ext = f.name.split('.').pop().toUpperCase();
    return {
      id: Date.now() + i,
      name: f.name,
      size,
      ext,
      type: 'doc',
      thumb: '#f0f0ed',
      emoji: getEmoji(f.name),
      res: '—',
      date: new Date().toLocaleDateString('vi-VN'),
    };
  });
  simulateUpload(items);
}

function simulateUpload(items) {
  closeModal();
  items.forEach((item, i) => {
    setTimeout(() => {
      // Thêm vào sampleFiles gốc để filter hoạt động đúng
      sampleFiles.unshift({
        ...item,
        id: Date.now() + i,
        date: new Date().toLocaleDateString('vi-VN'),
      });
      renderFiles();
      toast(`✓ ${item.name} đã tải lên`);
    }, i * 600);
  });
}

// ─── STATS UPDATE ─────────────────────────────────────────────────
function updateStats() {
  const source = activeFilter === 'trash' ? trashFiles : sampleFiles;

  const total = source.length;
  const imgs = source.filter((f) => f.type === 'img').length;
  const docs = source.filter((f) => f.type === 'doc').length;
  const vids = source.filter((f) => f.type === 'vid').length;
  const other = source.filter(
    (f) => !['img', 'doc', 'vid'].includes(f.type)
  ).length;

  document.getElementById('statTotal').textContent = total;
  document.getElementById('statImg').textContent = imgs;
  document.getElementById('statDoc').textContent = docs;
  document.getElementById('statVid').textContent = vids;
  document.getElementById('statOther').textContent = other;
}

// ─── TOAST ────────────────────────────────────────────────────────
function toast(msg) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>${msg}`;
  document.getElementById('toasts').appendChild(t);
  setTimeout(() => {
    t.classList.add('out');
    setTimeout(() => t.remove(), 300);
  }, 2800);
}

// ─── AVATAR MENU ──────────────────────────────────────────────────
const avatarBtn = document.getElementById('avatarBtn');
const avatarMenu = document.getElementById('avatarMenu');

function toggleAvatarMenu() {
  avatarMenu.classList.contains('open') ? closeAvatarMenu() : openAvatarMenu();
}
function openAvatarMenu() {
  avatarMenu.classList.add('open');
  avatarBtn.classList.add('open');
  document.querySelectorAll('.am-item').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateX(8px)';
    setTimeout(
      () => {
        el.style.transition =
          'opacity 0.2s, transform 0.22s cubic-bezier(0.16,1,0.3,1)';
        el.style.opacity = '1';
        el.style.transform = 'translateX(0)';
      },
      60 + i * 28
    );
  });
}
function closeAvatarMenu() {
  avatarMenu.classList.remove('open');
  avatarBtn.classList.remove('open');
}
document.addEventListener('click', (e) => {
  if (!document.querySelector('.avatar-wrap').contains(e.target))
    closeAvatarMenu();
});

async function loadFilesFromServer() {
  // 1. Hiển thị loading
  showLoadingState();

  try {
    // 2. Gọi API (THAY ĐỔI URL NÀY THEO SERVER CỦA BẠN)
    const response = await fetch(
      'https://vault-storage.me/upload_sv/upload_get_file',
      {
        method: 'GET',
        credentials: 'include', // Gửi cookies (session/auth)
        headers: {
          'Content-Type': 'application/json',
          // Nếu dùng JWT: 'Authorization': 'Bearer ' + token
        },
      }
    );
    // 3. Xử lý lỗi HTTP
    if (!response.ok) {
      if (response.status === 401) {
        // Chưa đăng nhập → Chuyển sang trang login
        toast('Phiên đăng nhập hết hạn');
        setTimeout(() => {
          window.location.href = 'https://vault-storage.me/401';
        }, 1500);
        return;
      }

      if (response.status === 500) {
        toast('Lỗi server, vui lòng thử lại sau');
        return;
      }

      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    // 4. Parse JSON
    // 4. Parse JSON
    const data = await response.json();
    // 5. Xóa hết dữ liệu cũ trên RAM để nạp mới
    sampleFiles.length = 0;
    trashFiles.length = 0;
    const actualData = data.files;
    if (
      actualData &&
      actualData.danh_sach_file &&
      Array.isArray(actualData.danh_sach_file)
    ) {
      sampleFiles.push(
        ...actualData.danh_sach_file.map((f, i) => ({
          ma_dinh_danh: f.ma_dinh_danh_file || f.id || f._id,
          id: f.id || f._id || `f_a_${i}`,
          name: f.name || 'Unnamed',
          type: mapFileType(f.type, f.ext),
          ext: (f.ext || '').toUpperCase(),
          size: f.size || '—',
          date: f.date || new Date().toLocaleDateString('vi-VN'),
          url: f.url || '',
          emoji: getEmojiForType(mapFileType(f.type, f.ext)),
          thumb: getThumbColor(mapFileType(f.type, f.ext)),
          path: f.path || '',
        }))
      );
    }

    // Xử lý File rác (Trash)
    if (
      actualData &&
      actualData.danh_sach_file_da_xoa &&
      Array.isArray(actualData.danh_sach_file_da_xoa)
    ) {
      trashFiles.push(
        ...actualData.danh_sach_file_da_xoa.map((f, i) => ({
          ma_dinh_danh: f.ma_dinh_danh_file || f.id || f._id,
          id: f.id || f._id || `f_t_${i}`,
          name: f.name || 'Unnamed',
          type: mapFileType(f.type, f.ext),
          ext: (f.ext || '').toUpperCase(),
          size: f.size || '—',
          date: f.date || new Date().toLocaleDateString('vi-VN'),
          url: f.url || '',
          emoji: getEmojiForType(mapFileType(f.type, f.ext)),
          thumb: getThumbColor(mapFileType(f.type, f.ext)),
          path: f.path || '',
        }))
      );
    }

    // 7. Cập nhật giao diện
    renderFiles();
    updateStats();
    updateBadges();
  } catch (error) {
    showErrorState(error.message);
    toast('Không thể tải danh sách file');
  }
}

// ─── HELPER FUNCTIONS ─────────────────────────────────────────────

/**
 * Hiển thị loading spinner
 */
function showLoadingState() {
  const container = document.getElementById('fileContainer');
  container.innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                gap:16px;padding:80px 24px;text-align:center;">
      <div style="width:40px;height:40px;border:3px solid var(--border);
                  border-top-color:var(--ink);border-radius:50%;
                  animation:spin 0.8s linear infinite;"></div>
      <div style="font-size:14px;color:var(--ink-3);font-weight:500;">
        Đang tải danh sách file...
      </div>
    </div>
    <style>
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
    </style>
  `;
}

/**
 * Hiển thị error state
 */
function showErrorState(message) {
  const container = document.getElementById('fileContainer');
  container.innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                gap:12px;padding:60px 24px;text-align:center;">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#c03030" 
           stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <div style="font-size:14px;font-weight:600;color:#c03030;">Lỗi tải dữ liệu</div>
      <div style="font-size:12px;color:var(--ink-4);max-width:300px;">${message}</div>
      <button onclick="loadFilesFromServer()" style="margin-top:8px;padding:8px 16px;
              background:var(--ink);color:#fff;border:none;border-radius:8px;
              font-size:13px;font-weight:600;cursor:pointer;">
        Thử lại
      </button>
    </div>
  `;
}

/**
 * Map type từ server (có thể là 'image', 'document', ...)
 * sang type dashboard ('img', 'doc', 'vid', 'pdf', 'zip')
 */
function mapFileType(serverType, ext) {
  // Nếu server đã trả đúng format → giữ nguyên
  if (['img', 'doc', 'vid', 'pdf', 'zip'].includes(serverType)) {
    return serverType;
  }

  // Map từ tên dài → tên ngắn
  const typeMap = {
    image: 'img',
    picture: 'img',
    photo: 'img',
    document: 'doc',
    text: 'doc',
    spreadsheet: 'doc',
    presentation: 'doc',
    video: 'vid',
    movie: 'vid',
    archive: 'zip',
    compressed: 'zip',
  };

  if (typeMap[serverType?.toLowerCase()]) {
    return typeMap[serverType.toLowerCase()];
  }

  // Fallback: Đoán theo extension
  return guessTypeFromExt(ext);
}

/**
 * Đoán type từ extension
 */
function guessTypeFromExt(ext) {
  if (!ext) return 'doc';
  ext = ext.toLowerCase().replace('.', '');

  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'].includes(ext))
    return 'img';
  if (['pdf'].includes(ext)) return 'pdf';
  if (['mp4', 'mov', 'avi', 'mkv', 'webm'].includes(ext)) return 'vid';
  if (['zip', 'rar', '7z', 'tar', 'gz'].includes(ext)) return 'zip';
  return 'doc'; // Default
}

/**
 * Extract extension từ filename
 */
function extractExt(filename) {
  if (!filename) return '';
  const parts = filename.split('.');
  return parts.length > 1 ? parts[parts.length - 1] : '';
}

/**
 * Format bytes thành human-readable (3.2 MB)
 */
function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 KB';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 10) / 10 + ' ' + sizes[i];
}

/**
 * Format ISO timestamp thành DD/MM/YYYY
 */
function formatDate(isoString) {
  if (!isoString) return '';
  try {
    const date = new Date(isoString);
    return date.toLocaleDateString('vi-VN');
  } catch {
    return '';
  }
}

/**
 * Lấy emoji theo type
 */
function getEmojiForType(type, ext) {
  const map = {
    img: '🖼️',
    pdf: '📄',
    doc: '📝',
    vid: '🎬',
    zip: '📦',
  };
  return map[type] || '📁';
}

/**
 * Lấy màu thumb theo type
 */
function getThumbColor(type) {
  const map = {
    img: '#f0ece8',
    pdf: '#f0f0ed',
    doc: '#eef0e8',
    vid: '#e8ecf0',
    zip: '#ede8f0',
  };
  return map[type] || '#f5f5f3';
}

// ─── SEARCH ───────────────────────────────────────────────────────
const searchInput = document.getElementById('searchInput');
const searchClear = document.getElementById('searchClear');

searchInput.addEventListener('input', () => {
  searchQuery = searchInput.value;
  // Hiện/ẩn nút clear
  searchClear.style.display = searchQuery.length > 0 ? 'flex' : 'none';
  // Reset selection khi search
  selectedId = null;
  renderFiles();
});

// Phím Escape: xóa search
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') clearSearch();
});

function clearSearch() {
  searchInput.value = '';
  searchQuery = '';
  searchClear.style.display = 'none';
  selectedId = null;
  renderFiles();
  searchInput.focus();
}

function updateBadges() {
  document.getElementById('all_file').textContent = sampleFiles.length;
  const imgCount = sampleFiles.filter((f) => f.type === 'img').length;
  const docCount = sampleFiles.filter((f) => f.type === 'doc').length;
  const vidCount = sampleFiles.filter((f) => f.type === 'vid').length;
  if (document.getElementById('hinh_anh'))
    document.getElementById('hinh_anh').textContent = imgCount;
  if (document.getElementById('tai_lieu'))
    document.getElementById('tai_lieu').textContent = docCount;
  if (document.getElementById('video'))
    document.getElementById('video').textContent = vidCount;
}

loadFilesFromServer();

async function downloadCurrentFile() {
  if (!selectedId) return;
  const fileToDownload = sampleFiles.find((f) => f.id === selectedId);
  if (!fileToDownload || !fileToDownload.url) return;
  if (!selectedId) {
    toast('Vui lòng chọn một file để tải!');
    return;
  }
  if (fileToDownload && fileToDownload.url) {
    toast(`Đang chuẩn bị tải: ${fileToDownload.name}...`);

    try {
      isProcessing = true;
      const kinh_do_user = localStorage.getItem('lon') ?? null;
      const vi_do_user = localStorage.getItem('lat') ?? null;
      fetch('https://vault-storage.me/upload_sv/log-download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          fileId: selectedId,
          fileName: fileToDownload.name,
          location_user: {
            kinh_do: kinh_do_user,
            vi_do: vi_do_user,
          },
          timestamp: new Date().toISOString(),
        }),
      }).catch((err) => console.error('Lỗi ghi log'));

      const response = await fetch(fileToDownload.url);
      if (!response.ok) throw new Error('Không thể kết nối server');
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = fileToDownload.name;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);

      toast(`Đã tải xong: ${fileToDownload.name}`);
    } catch (error) {
      toast('Lỗi khi tải file, thử lại sau nhé og!'); //
    } finally {
      // Đợi 1 chút sau khi tải xong mới mở khóa để tránh panel đóng sầm lại ngay
      setTimeout(() => {
        isProcessing = false;
      }, 500);
    }
  } else {
    toast('Lỗi: Link file không tồn tại!');
  }
}

// BẮT SỰ KIỆN CHO PREVIEW THUMB (CLICK + HIỆU ỨNG GLOW)
document.addEventListener('DOMContentLoaded', () => {
  const previewThumb = document.getElementById('previewThumb');

  if (previewThumb) {
    // 1. TẠO HIỆU ỨNG GLOW THEO CHUỘT
    previewThumb.addEventListener('mousemove', (e) => {
      // Lấy khung tọa độ của thẻ #previewThumb
      const rect = previewThumb.getBoundingClientRect();

      // Tính toán tọa độ X, Y của chuột so với góc trên trái của ảnh
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      // Đẩy tọa độ này ra CSS thông qua Custom Properties
      previewThumb.style.setProperty('--mouse-x', `${x}px`);
      previewThumb.style.setProperty('--mouse-y', `${y}px`);
    });

    // 2. SỰ KIỆN CLICK ĐỂ MỞ ẢNH
    previewThumb.addEventListener('click', function () {
      if (!selectedId) return;

      const currentFile =
        sampleFiles.find((f) => f.id === selectedId) ||
        trashFiles.find((f) => f.id === selectedId);
      if (!currentFile) return;

      if (currentFile.type !== 'img' || !currentFile.url) {
        return;
      }

      const allImages = sampleFiles.filter((f) => f.type === 'img' && f.url);

      if (typeof openImagePreview === 'function') {
        openImagePreview(
          {
            id: currentFile.id,
            url: currentFile.url,
            name: currentFile.name,
            type: currentFile.ext,
            size: currentFile.size,
            date: currentFile.date,
          },
          allImages
        );
      } else {
        pass();
      }
    });
  }
});
