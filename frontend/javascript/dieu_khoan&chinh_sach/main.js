let currentTab = 'terms';

// Hàm đọc file text
async function loadTextFile(filename) {
  try {
    const response = await fetch(filename);
    if (!response.ok) {
      throw new Error('Không thể tải file');
    }
    const text = await response.text();
    return text;
  } catch (error) {
    console.error('Lỗi khi đọc file:', error);
    return `<div class="error-message">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <h3>Không thể tải nội dung</h3>
                    <p>Vui lòng đảm bảo file "${filename}" tồn tại trong cùng thư mục.</p>
                </div>`;
  }
}

// Hàm chuyển đổi text thành HTML có định dạng
function formatTextToHTML(text) {
  // Tách thành các đoạn
  const paragraphs = text.split('\n\n');
  let html = '';

  paragraphs.forEach((para) => {
    para = para.trim();
    if (!para) return;

    // Kiểm tra nếu là tiêu đề (viết hoa hoặc có số đầu dòng)
    if (
      para.match(
        /^[A-ZĐÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ\s]+$/
      ) ||
      para.match(/^\d+\.|^[IVX]+\./)
    ) {
      html += `<h2>${para}</h2>`;
    }
    // Kiểm tra nếu là danh sách
    else if (para.match(/^[-•]\s/)) {
      html += `<ul><li>${para.replace(/^[-•]\s/, '')}</li></ul>`;
    }
    // Đoạn văn bình thường
    else {
      html += `<p>${para}</p>`;
    }
  });

  return html;
}

// Load nội dung khi trang được tải
async function loadContent() {
  // Load điều khoản dịch vụ
  const termsText = await loadTextFile('terms_of_service.txt');
  document.getElementById('terms-content').innerHTML =
    formatTextToHTML(termsText);

  // Load chính sách bảo mật
  const privacyText = await loadTextFile('privacy_policy.txt');
  document.getElementById('privacy-content').innerHTML =
    formatTextToHTML(privacyText);
}

// Chuyển đổi tab
function switchTab(tab) {
  currentTab = tab;

  // Cập nhật nút tab
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach((t) => t.classList.remove('active'));
  event.target.closest('.tab-btn').classList.add('active');

  // Cập nhật nội dung
  const contents = document.querySelectorAll('.tab-content');
  contents.forEach((c) => c.classList.remove('active'));

  if (tab === 'terms') {
    document.getElementById('terms-content').classList.add('active');
  } else {
    document.getElementById('privacy-content').classList.add('active');
  }
}

// Quay lại trang trước
function goBack() {
  window.location.href = '../group_password/create_a_password.html';
}

// In trang
function loggerContent() {
  window.logger();
}

// Load nội dung khi trang được tải
window.addEventListener('DOMContentLoaded', loadContent);
