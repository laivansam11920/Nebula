function showLoadingState() {
  const container = document.getElementById('fileContainer'); // Hoặc id nơi og chứa file
  if (!container) return;
  
  // Dọn sạch container
  container.innerHTML = '';
  
  // Tạo ra 12 cái khung xương giả để giữ chỗ
  let skeletonHTML = '';
  for (let i = 0; i < 12; i++) {
    skeletonHTML += `<div class="skeleton-card"></div>`;
  }
  
  container.innerHTML = skeletonHTML;
}