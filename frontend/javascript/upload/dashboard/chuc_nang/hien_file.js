const khu_vuc_file = document.querySelector('.file-container');

// Bắt sự kiện khi chuột di chuyển vào khu vực chứa file
khu_vuc_file.addEventListener('mouseover', (e) => {
    const file_hien_tai = e.target.closest('.file-item');
    if (!file_hien_tai) return; // Nếu không trúng file nào thì bỏ qua

    // Nếu file chưa có menu chức năng thì dùng JS tạo ra
    if (!file_hien_tai.querySelector('.file-actions')) {
        const menu_chuc_nang = document.createElement('div');
        menu_chuc_nang.className = 'file-actions';
        // Thêm các nút bấm của ông vào đây
        menu_chuc_nang.innerHTML = `<button>Sửa</button> <button>Xóa</button>`;
        file_hien_tai.appendChild(menu_chuc_nang);
    }
});

// Xóa menu đi khi chuột rời khỏi file để dọn "rác"
khu_vuc_file.addEventListener('mouseout', (e) => {
     const file_hien_tai = e.target.closest('.file-item');
     if (file_hien_tai) {
         const menu_chuc_nang = file_hien_tai.querySelector('.file-actions');
         if (menu_chuc_nang) menu_chuc_nang.remove();
     }
});