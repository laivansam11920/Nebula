/**
 * Storage Manager
 * Lấy dữ liệu dung lượng từ Backend, cập nhật giao diện và cảnh báo.
 */
const storageInfoEl = document.querySelector('.storage-info');
const StorageManager = {
  // Mức phần trăm dung lượng sẽ kích hoạt cảnh báo
  WARNING_THRESHOLD_PERCENT: 90,

  /**
   * Định dạng byte thành dạng có thể đọc được (KB, MB, GB)
   */
  formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  },

  /**
   * Cập nhật tất cả các thanh tiến trình hiển thị dung lượng trên giao diện
   * @param {Object} storageData Object lưu trữ trả về từ API Backend
   */
  updateUI(storageData) {
    // Trích xuất dữ liệu từ Backend
    const currentBytes = storageData.used_bytes;
    const maxBytes = storageData.max_bytes;
    let percent = storageData.percent_used;

    // Đảm bảo không vượt quá 100% trên thanh tiến trình
    if (percent > 100) percent = 100;
    const percentRounded = Math.round(percent);

    const formattedCurrent = this.formatBytes(currentBytes);
    // Nếu maxMB >= 1024 thì hiển thị dạng GB cho đẹp, ngược lại hiển thị MB
    const formattedMax =
      storageData.max_mb >= 1024
        ? `${(storageData.max_mb / 1024).toFixed(1)} GB`
        : `${storageData.max_mb} MB`;

    // 1. Cập nhật Sidebar (index.html)
    const storagePctEl = document.querySelector('.storage-pct');
    const storFillEl = document.getElementById('storFill');
    const storageInfoEl = document.querySelector('.storage-info');

    if (storagePctEl) storagePctEl.innerText = `${percentRounded}%`;
    if (storFillEl) storFillEl.style.width = `${percent}%`;
    if (storageInfoEl) {
      storageInfoEl.innerHTML = `Đã dùng <strong>${formattedCurrent}</strong> / ${formattedMax}`;
    }

    // 2. Cập nhật Right Click Menu (right_click.js)
    const ctxStorageValueEl = document.querySelector(
      '.context-menu-storage-value'
    );
    const ctxStorageFillEl = document.getElementById('ctxStorageFill');
    const ctxStorageTextEl = document.querySelector(
      '.context-menu-storage-text'
    );

    if (ctxStorageValueEl) ctxStorageValueEl.innerText = `${percentRounded}%`;
    if (ctxStorageFillEl) ctxStorageFillEl.style.width = `${percent}%`;
    if (ctxStorageTextEl) {
      ctxStorageTextEl.innerHTML = `<strong>${formattedCurrent}</strong> / ${formattedMax}`;
    }

    // 3. Cập nhật Settings Modal (setting_model.js)
    const settingsStorageContainer = document.querySelector(
      '#settings-storage .settings-item > div:nth-child(2)'
    );
    if (settingsStorageContainer) {
      const textSpanInfo = settingsStorageContainer.querySelector(
        'div:first-child span:first-child'
      );
      const textSpanPct = settingsStorageContainer.querySelector(
        'div:first-child span:last-child'
      );
      const barFill = settingsStorageContainer.querySelector(
        'div:last-child > div'
      );

      if (textSpanInfo)
        textSpanInfo.innerText = `${formattedCurrent} / ${formattedMax}`;
      if (textSpanPct) textSpanPct.innerText = `${percentRounded}%`;
      if (barFill) barFill.style.width = `${percent}%`;
    }

    // 4. Kiểm tra cảnh báo nếu sắp hết dung lượng
    if (percent >= this.WARNING_THRESHOLD_PERCENT) {
      this.showWarningNotification(percentRounded, formattedMax);
    }
  },

  /**
   * Hiển thị cảnh báo cho người dùng
   */
  showWarningNotification(percent, maxCapacity) {
    // Có thể thay alert bằng hàm Toast custom của bạn (ví dụ: toast(...))
    toast(
      `Cảnh báo: Bạn đã sử dụng hết ${percent}% không gian lưu trữ (Tối đa ${maxCapacity})! Vui lòng dọn dẹp file không cần thiết hoặc nâng cấp dung lượng.`
    );
  },

  /**
   * Gọi API Server để lấy thông tin dung lượng
   */
  async fetchAndRefreshStorage() {
    try {
      const apiUrl = 'https://vault-storage.me/upload_sv/check_storage_user';

      const response = await fetch(apiUrl, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data && data.storage) {
        this.updateUI(data.storage);
        storageInfoEl.innerHTML = `Đã dùng <strong>${this.formatBytes(data.storage.used_bytes)}</strong> / ${this.formatBytes(
          data.storage.max_bytes
        )}`;
      }
    } catch (error) {
      console.error(
        'Lỗi khi lấy thông tin dung lượng lưu trữ từ Server:',
        error
      );
    }
  },
};

document.addEventListener('DOMContentLoaded', () => {
  StorageManager.fetchAndRefreshStorage();
});

window.refreshStorageUI = () => StorageManager.fetchAndRefreshStorage();
