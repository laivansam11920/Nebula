// ═══ SHARE MODAL FUNCTIONS ═══

let currentShareFile = null;
let isPublic = false;

/**
 * Mở modal chia sẻ
 * @param {Object} file - {id, name, type, url}
 */
function openShareModal(file) {
  currentShareFile = file;

  // Update file name
  document.getElementById('shareFileName').textContent = file.name;

  // Update share link
  const shareLink = `https://vault.com/share/${file.id}`;
  document.getElementById('shareLinkInput').value = shareLink;

  // Show HTML section only for .html files
  const htmlSection = document.getElementById('htmlAccessSection');
  if (file.name.toLowerCase().endsWith('.html')) {
    htmlSection.style.display = 'block';
    isPublic = false;
    updatePrivacyUI();
  } else {
    htmlSection.style.display = 'none';
  }

  // Show modal
  document.getElementById('shareModalOverlay').classList.add('show');
  document.body.style.overflow = 'hidden';
}

/**
 * Đóng modal
 */
function closeShareModal() {
  document.getElementById('shareModalOverlay').classList.remove('show');
  document.body.style.overflow = '';
  currentShareFile = null;
  isPublic = false;
}

/**
 * Copy link
 */
function copyShareLink() {
  const input = document.getElementById('shareLinkInput');
  input.select();
  document.execCommand('copy');

  const btn = document.querySelector('.share-copy-btn');
  btn.textContent = 'Copied!';
  btn.classList.add('copied');

  setTimeout(() => {
    btn.textContent = 'Copy';
    btn.classList.remove('copied');
  }, 2000);

  if (typeof toast === 'function') {
    toast('✓ Đã copy link');
  }
}

/**
 * Toggle privacy
 */
function togglePrivacy() {
  isPublic = !isPublic;
  updatePrivacyUI();

  // TODO: Call API to update privacy
  console.log(`Privacy: ${isPublic ? 'PUBLIC' : 'PRIVATE'}`);

  if (typeof toast === 'function') {
    toast(isPublic ? '🌐 File đã công khai' : '🔒 File riêng tư');
  }
}

/**
 * Update privacy UI
 */
function updatePrivacyUI() {
  const toggle = document.getElementById('privacyToggle');
  const label = document.getElementById('privacyLabel');
  const labelText = document.getElementById('privacyLabelText');
  const badge = document.getElementById('privacyBadge');

  if (isPublic) {
    toggle.classList.add('public');
    label.classList.remove('private');
    label.classList.add('public');
    labelText.textContent = 'Công khai';
    badge.textContent = 'PUBLIC';
  } else {
    toggle.classList.remove('public');
    label.classList.remove('public');
    label.classList.add('private');
    labelText.textContent = 'Riêng tư';
    badge.textContent = 'PRIVATE';
  }
}

/**
 * Open HTML preview
 */
function openHTMLPreview() {
  if (!currentShareFile) return;
  const url =
    currentShareFile.url || `https://vault.com/preview/${currentShareFile.id}`;
  window.open(url, '_blank');
}

// ─── Social Sharing ─────────────────────────────────────────

function shareToFacebook() {
  const link = document.getElementById('shareLinkInput').value;
  const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(link)}`;
  window.open(url, '_blank', 'width=600,height=400');
}

function shareToTwitter() {
  const link = document.getElementById('shareLinkInput').value;
  const text = `Xem file "${currentShareFile.name}" của tôi:`;
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(link)}`;
  window.open(url, '_blank', 'width=600,height=400');
}

function shareToEmail() {
  const link = document.getElementById('shareLinkInput').value;
  const subject = `Chia sẻ file: ${currentShareFile.name}`;
  const body = `Xin chào,\n\nTôi muốn chia sẻ file "${currentShareFile.name}" với bạn.\n\nTruy cập: ${link}`;
  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

function shareToWhatsApp() {
  const link = document.getElementById('shareLinkInput').value;
  const text = `Xem file "${currentShareFile.name}": ${link}`;
  window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
}

function shareToTelegram() {
  const link = document.getElementById('shareLinkInput').value;
  const text = `Xem file "${currentShareFile.name}"`;
  window.open(
    `https://t.me/share/url?url=${encodeURIComponent(link)}&text=${encodeURIComponent(text)}`,
    '_blank'
  );
}

// ─── Event Listeners ────────────────────────────────────────

// Click outside to close
document
  .getElementById('shareModalOverlay')
  .addEventListener('click', function (e) {
    if (e.target === this) {
      closeShareModal();
    }
  });

// ESC to close
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    const overlay = document.getElementById('shareModalOverlay');
    if (overlay.classList.contains('show')) {
      closeShareModal();
    }
  }
});

console.log('[Share Modal] Loaded');

function shareFile() {
  if (!selectedId) {
    toast('Chọn file trước');
    return;
  }

  const file = sampleFiles.find((f) => f.id === selectedId);

  if (!file) {
    toast('File không tồn tại');
    return;
  }

  const kinh_do_user = localStorage.getItem('lon') ?? null;
  const vi_do_user = localStorage.getItem('lat') ?? null;

  fetch('https://vault-storage.me/upload_sv/log-share', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      id: file.id,
      name: file.name,
      type: file.type,
      location_user: {
        kinh_do: kinh_do_user,
        vi_do: vi_do_user,
      },
      timestamp: new Date().toISOString(),
    }),
  }).catch((err) => console.error('Lỗi ghi log:', err));
  // Open share modal
  openShareModal({
    id: file.id,
    name: file.name,
    type: file.type,
    url: file.url || `https://vault.com/files/${file.id}`,
  });
}
