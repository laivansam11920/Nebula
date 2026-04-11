# FileVault Admin Dashboard — Tài liệu kỹ thuật

> Hướng dẫn đầy đủ: chỉnh sửa giao diện, cấu hình thông số, và tích hợp API server thực.

---

## Mục lục

1. [Tổng quan kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Cấu trúc file HTML](#2-cấu-trúc-file-html)
3. [Biểu đồ Upload Activity (Chart.js)](#3-biểu-đồ-upload-activity)
4. [Thẻ thống kê (Stat Cards)](#4-thẻ-thống-kê-stat-cards)
5. [Phân loại lưu trữ (Storage Breakdown)](#5-phân-loại-lưu-trữ)
6. [Bảng file gần đây (Recent Files)](#6-bảng-file-gần-đây)
7. [Nhật ký hoạt động (Activity Feed)](#7-nhật-ký-hoạt-động)
8. [Trạng thái hệ thống (System Status)](#8-trạng-thái-hệ-thống)
9. [Sidebar & Navigation](#9-sidebar--navigation)
10. [Profile Dropdown](#10-profile-dropdown)
11. [Kết nối API Server thực](#11-kết-nối-api-server-thực)
12. [Polling & Auto-refresh](#12-polling--auto-refresh)
13. [Xử lý lỗi & Loading state](#13-xử-lý-lỗi--loading-state)

---

## 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                   TRÌNH DUYỆT (Client)                  │
│                                                         │
│  ┌──────────┐   ┌────────────────────────────────────┐  │
│  │ Sidebar  │   │           Main Content             │  │
│  │ (nav)    │   │  ┌──────────┐  ┌────────────────┐  │  │
│  │          │   │  │ Topbar   │  │ Profile Popup  │  │  │
│  │ Icon →   │   │  └──────────┘  └────────────────┘  │  │
│  │ Expanded │   │  ┌──────────────────────────────┐  │  │
│  │          │   │  │    Dashboard Content         │  │  │
│  │          │   │  │  Stats / Charts / Tables     │  │  │
│  └──────────┘   │  └──────────────────────────────┘  │  │
└─────────────────────────────────────────────────────────┘
          │                    │
          ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND SERVER                        │
│                                                         │
│   GET /api/dashboard/stats      ← Stat cards            │
│   GET /api/dashboard/uploads    ← Biểu đồ               │
│   GET /api/files/recent         ← Bảng file             │
│   GET /api/activity             ← Activity feed         │
│   GET /api/system/health        ← System status         │
│   GET /api/storage/breakdown    ← Storage chart         │
└─────────────────────────────────────────────────────────┘
```

Dashboard hiện tại dùng **dữ liệu tĩnh (mock)**. Phần [11. Kết nối API](#11-kết-nối-api-server-thực) hướng dẫn cách thay thế bằng API thực.

---

## 2. Cấu trúc file HTML

```
admin-dashboard.html
├── <style>           ← Toàn bộ CSS (CSS variables, layout, components)
├── <nav#sidebar>     ← Thanh bên trái
├── <div#main>
│   ├── <header#topbar>          ← Thanh trên (search, avatar)
│   └── <div#content>           ← Nội dung chính
│       ├── .stats-grid          ← 4 thẻ thống kê
│       ├── .charts-row          ← Biểu đồ + phân loại lưu trữ
│       ├── .bottom-row          ← Bảng file + activity feed
│       └── .system-row          ← CPU / RAM / Uptime
├── <div#profile-dropdown>       ← Popup thông tin admin
└── <script>          ← Chart.js + logic JS
```

---

## 3. Biểu đồ Upload Activity

### Vị trí trong code

```html
<!-- HTML: canvas element -->
<canvas id="uploadChart"></canvas>
```

```javascript
// JS: Tìm đoạn này trong <script>
new Chart(ctx, { ... });
```

### Điều chỉnh dữ liệu

**Thay đổi số ngày hiển thị** (hiện tại: 30 ngày):

```javascript
// Tìm dòng:
for (let i = 29; i >= 0; i--) {

// Đổi thành 7 ngày:
for (let i = 6; i >= 0; i--) {

// Đổi thành 90 ngày:
for (let i = 89; i >= 0; i--) {
```

**Thay đổi màu sắc đường biểu đồ:**

```javascript
datasets: [
  {
    label: 'Upload',
    borderColor: 'rgba(255,255,255,0.9)', // ← Màu đường Upload (trắng)
    backgroundColor: 'rgba(255,255,255,0.04)', // ← Màu nền bên dưới đường
    borderWidth: 1.5, // ← Độ dày đường (px)
  },
  {
    label: 'Download',
    borderColor: 'rgba(100,100,100,0.8)', // ← Màu đường Download (xám)
    borderDash: [4, 4], // ← Nét đứt: [dài nét, khoảng trống]
    // borderDash: []  ← Xóa dòng này để thành đường liền
  },
];
```

**Thay đổi kiểu biểu đồ:**

```javascript
// Tìm dòng:
type: 'line',

// Các tùy chọn:
type: 'bar',    // Cột đứng
type: 'line',   // Đường (hiện tại)
```

**Thay đổi độ cong của đường:**

```javascript
tension: 0.4,   // 0 = thẳng góc, 0.4 = cong mềm, 1 = cong mạnh
```

**Thay đổi màu tooltip (hộp thông tin khi hover):**

```javascript
tooltip: {
  backgroundColor: '#1a1a1a',  // ← Nền tooltip
  borderColor: '#333',         // ← Viền tooltip
  titleColor: '#a0a0a0',       // ← Màu chữ tiêu đề
  bodyColor: '#fff',           // ← Màu chữ nội dung
  padding: 10,                 // ← Padding bên trong (px)
}
```

**Thay đổi trục X / Y:**

```javascript
scales: {
  x: {
    ticks: {
      maxTicksLimit: 8,   // ← Số nhãn tối đa trên trục X
      color: '#505050',   // ← Màu chữ trục X
    }
  },
  y: {
    ticks: {
      maxTicksLimit: 5,   // ← Số nhãn tối đa trên trục Y
    }
  }
}
```

### Kết nối dữ liệu từ API

```javascript
// HIỆN TẠI (dữ liệu giả):
for (let i = 29; i >= 0; i--) {
  uploadData.push(Math.floor(Math.random() * 300 + 80));  // ← số ngẫu nhiên
  downloadData.push(Math.floor(Math.random() * 200 + 40));
}

// ──────────────────────────────────────────────
// THAY BẰNG: gọi API thực
async function loadChart() {
  const res = await fetch('/api/dashboard/uploads?days=30');
  const data = await res.json();
  // Kỳ vọng server trả về:
  // { labels: ["01/01","02/01",...], uploads: [120,95,...], downloads: [60,45,...] }

  new Chart(ctx, {
    data: {
      labels: data.labels,
      datasets: [
        { label: 'Upload', data: data.uploads, ... },
        { label: 'Download', data: data.downloads, ... }
      ]
    }
  });
}
loadChart();
```

---

## 4. Thẻ thống kê (Stat Cards)

### Vị trí trong code

```html
<div class="stats-grid">
  <div class="stat-card">...</div>
  <!-- Tổng file -->
  <div class="stat-card">...</div>
  <!-- Dung lượng -->
  <div class="stat-card">...</div>
  <!-- Người dùng -->
  <div class="stat-card">...</div>
  <!-- Lượt tải -->
</div>
```

### Giải thích từng phần trong 1 thẻ

```html
<div class="stat-card">
  <div class="stat-header">
    <div class="stat-icon">📁</div>
    <!-- Icon (emoji hoặc SVG) -->
    <span class="stat-change up">↑ 12.4%</span>
    <!-- % thay đổi -->
    <!-- class="up" = màu xanh, class="down" = màu đỏ -->
  </div>
  <div class="stat-val">48,291</div>
  <!-- Số chính (to, đậm) -->
  <div class="stat-label">Tổng số file</div>
  <!-- Nhãn mô tả -->
  <div class="stat-sub">
    <span class="stat-sub-dot" style="background:var(--green)"></span>
    +586 file trong 7 ngày qua
    <!-- Mô tả phụ -->
  </div>
</div>
```

### Thêm / bớt thẻ

```html
<!-- Thêm thẻ mới vào .stats-grid -->
<div class="stat-card">
  <div class="stat-header">
    <div class="stat-icon">⚡</div>
    <span class="stat-change up">↑ 2.1%</span>
  </div>
  <div class="stat-val">99.98%</div>
  <div class="stat-label">Uptime tháng này</div>
  <div class="stat-sub">
    <span class="stat-sub-dot" style="background:var(--green)"></span>
    Downtime: 8 phút
  </div>
</div>
```

**Lưu ý:** Hiện tại grid là `grid-template-columns: repeat(4, 1fr)`. Nếu thêm thẻ thứ 5, đổi thành:

```css
/* Tìm trong <style>: */
.stats-grid {
  grid-template-columns: repeat(
    5,
    1fr
  ); /* hoặc repeat(auto-fill, minmax(200px, 1fr)) */
}
```

### Kết nối API

```javascript
async function loadStats() {
  const res = await fetch('/api/dashboard/stats');
  const s = await res.json();
  // Kỳ vọng: { totalFiles: 48291, fileChange: 12.4, storage: "2.38 TB", ... }

  document.querySelector(
    '.stats-grid .stat-card:nth-child(1) .stat-val'
  ).textContent = s.totalFiles.toLocaleString('vi-VN');

  document.querySelector(
    '.stats-grid .stat-card:nth-child(2) .stat-val'
  ).textContent = s.storageUsed;
  // ... tương tự cho card 3, 4
}
```

---

## 5. Phân loại lưu trữ

### Vị trí trong code

```html
<div class="storage-list">
  <div class="storage-item">...</div>
  <!-- PDF -->
  <div class="storage-item">...</div>
  <!-- Video -->
  ...
</div>
```

### Cấu trúc 1 dòng

```html
<div class="storage-item">
  <div class="storage-item-head">
    <div class="storage-name">
      <div class="storage-ext">PDF</div>
      <!-- Label loại file (tối đa 3-4 ký tự) -->
      PDF Documents
      <!-- Tên hiển thị -->
    </div>
    <div class="storage-meta">486 GB · 34%</div>
    <!-- Dung lượng · Phần trăm -->
  </div>
  <div class="progress-bar">
    <div class="progress-fill" style="width:34%"></div>
    <!-- width = phần trăm -->
  </div>
</div>
```

### Kết nối API

```javascript
async function loadStorage() {
  const res = await fetch('/api/storage/breakdown');
  const items = await res.json();
  // Kỳ vọng: [{ ext:"PDF", label:"PDF Documents", size:"486 GB", percent:34 }, ...]

  const list = document.querySelector('.storage-list');
  list.innerHTML = items
    .map(
      (item) => `
    <div class="storage-item">
      <div class="storage-item-head">
        <div class="storage-name">
          <div class="storage-ext">${item.ext}</div>
          ${item.label}
        </div>
        <div class="storage-meta">${item.size} · ${item.percent}%</div>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" style="width:${item.percent}%"></div>
      </div>
    </div>
  `
    )
    .join('');
}
```

---

## 6. Bảng file gần đây

### Cấu trúc 1 dòng trong bảng

```html
<tr>
  <td>
    <div class="file-cell">
      <div class="file-thumb">PDF</div>
      <!-- Loại file -->
      <div>
        <div class="file-name">bao-cao.pdf</div>
        <!-- Tên file -->
        <div class="file-id">#FV-00291</div>
        <!-- ID hệ thống -->
      </div>
    </div>
  </td>
  <td>4.2 MB</td>
  <!-- Kích thước -->
  <td>nguyenvana</td>
  <!-- Username -->
  <td>
    <span class="status-pill active">Active</span>
    <!-- class options: active | pending | blocked -->
  </td>
</tr>
```

### Kết nối API

```javascript
async function loadRecentFiles() {
  const res = await fetch('/api/files/recent?limit=10');
  const files = await res.json();
  // Kỳ vọng: [{ id:"FV-291", name:"bao-cao.pdf", ext:"PDF", size:"4.2 MB",
  //             user:"nguyenvana", status:"active" }]

  const tbody = document.querySelector('tbody');
  tbody.innerHTML = files
    .map(
      (f) => `
    <tr>
      <td>
        <div class="file-cell">
          <div class="file-thumb">${f.ext}</div>
          <div>
            <div class="file-name">${f.name}</div>
            <div class="file-id">#${f.id}</div>
          </div>
        </div>
      </td>
      <td>${f.size}</td>
      <td>${f.user}</td>
      <td><span class="status-pill ${f.status}">${capitalize(f.status)}</span></td>
    </tr>
  `
    )
    .join('');
}

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
```

---

## 7. Nhật ký hoạt động

### Cấu trúc 1 mục

```html
<div class="activity-item">
  <div class="activity-dot-wrap">
    <div class="activity-dot green"></div>
    <!-- màu: green | red | yellow | blue | (trống) -->
    <div class="activity-line"></div>
    <!-- đường nối xuống (xóa ở item cuối) -->
  </div>
  <div class="activity-info">
    <div class="activity-text">
      <strong>nguyenvana</strong> đã upload
      <!-- <strong> = in đậm -->
    </div>
    <div class="activity-time">2 phút trước · 192.168.1.42</div>
  </div>
</div>
```

### Màu dot theo loại sự kiện

| Class dot | Màu        | Dùng cho                     |
| --------- | ---------- | ---------------------------- |
| `green`   | Xanh lá    | Upload thành công, backup OK |
| `red`     | Đỏ         | File bị chặn, lỗi hệ thống   |
| `yellow`  | Vàng       | Cảnh báo, yêu cầu chờ duyệt  |
| `blue`    | Xanh dương | Đăng ký user mới, thông tin  |
| _(trống)_ | Xám        | Hoạt động thông thường       |

### Kết nối API

```javascript
async function loadActivity() {
  const res = await fetch('/api/activity?limit=10');
  const logs = await res.json();
  // Kỳ vọng: [{ color:"green", text:"<strong>user</strong> đã upload...",
  //             time:"2 phút trước", ip:"192.168.1.42" }]

  const container = document.querySelector('.activity-list');
  container.innerHTML = logs
    .map(
      (log, i) => `
    <div class="activity-item">
      <div class="activity-dot-wrap">
        <div class="activity-dot ${log.color}"></div>
        ${i < logs.length - 1 ? '<div class="activity-line"></div>' : ''}
      </div>
      <div class="activity-info">
        <div class="activity-text">${log.text}</div>
        <div class="activity-time">${log.time}${log.ip ? ' · ' + log.ip : ''}</div>
      </div>
    </div>
  `
    )
    .join('');
}
```

---

## 8. Trạng thái hệ thống

### Cấu trúc 1 thẻ hệ thống

```html
<div class="sys-card">
  <div class="sys-head">
    <div class="sys-name">CPU Usage</div>
    <span class="stat-change up" style="...">Normal</span>
    <!-- badge trạng thái -->
  </div>
  <div class="sys-val">34%</div>
  <!-- Giá trị chính -->
  <div class="sys-desc">8-core · 3.6 GHz · Load avg: 2.7</div>
  <!-- Mô tả -->
  <div class="sys-bar">
    <div class="sys-bar-fill" style="width:34%"></div>
    <!-- width = % -->
    <!-- Thêm class "warn" (vàng) nếu > 70%, "danger" (đỏ) nếu > 90% -->
  </div>
</div>
```

### Logic màu thanh tiến trình

```javascript
function getBarClass(percent) {
  if (percent >= 90) return 'danger';
  if (percent >= 70) return 'warn';
  return ''; // trắng (bình thường)
}
```

### Kết nối API

```javascript
async function loadSystemHealth() {
  const res = await fetch('/api/system/health');
  const sys = await res.json();
  // Kỳ vọng: { cpu: { percent: 34, desc: "8-core · 3.6 GHz" },
  //            ram: { percent: 67, used: "21.4 GB", total: "32 GB" },
  //            uptime: { percent: 99.98, days: 47, hours: 14 } }

  // Cập nhật CPU
  document.querySelector('.sys-card:nth-child(1) .sys-val').textContent =
    sys.cpu.percent + '%';
  document.querySelector('.sys-card:nth-child(1) .sys-bar-fill').style.width =
    sys.cpu.percent + '%';
  document.querySelector('.sys-card:nth-child(1) .sys-bar-fill').className =
    'sys-bar-fill ' + getBarClass(sys.cpu.percent);
  // Tương tự cho RAM và Uptime...
}
```

---

## 9. Sidebar & Navigation

### Cách hoạt động

```
Trạng thái mặc định:    width: 64px   → chỉ thấy icon
Khi hover (#sidebar):   width: 260px  → icon + label + badge

CSS điều khiển:
#sidebar { width: var(--sidebar-w); transition: width 0.35s; }
#sidebar:hover { width: var(--sidebar-expanded); }

Nội dung ẩn/hiện:
.nav-label { opacity: 0; transition: opacity 0.35s; }
#sidebar:hover .nav-label { opacity: 1; }
```

### Thêm mục navigation mới

```html
<!-- Thêm vào trong <div class="sidebar-section"> -->
<div class="nav-item">
  <div class="nav-icon">⊕</div>
  <!-- Icon (emoji, hoặc SVG 16x16) -->
  <span class="nav-label">Tên mục</span>
  <!-- Nhãn hiện khi hover -->
  <span class="nav-badge">99</span>
  <!-- Badge (tùy chọn, xóa nếu không cần) -->
</div>
```

### Đổi màu accent sidebar (hiện tại trắng)

```css
/* Tìm trong CSS: */
.nav-item.active::before {
  background: var(--white); /* Đổi thành màu khác, vd: #60a5fa */
}
```

### Thêm section mới

```html
<div class="sidebar-section">
  <div class="section-label">Tên section</div>
  <div class="nav-item">...</div>
</div>
```

---

## 10. Profile Dropdown

### Kích hoạt

```javascript
// Mở dropdown khi click avatar topbar
document.getElementById('avatarBtn').onclick = toggleDropdown;

// Mở dropdown khi click avatar sidebar
document
  .getElementById('sidebarAvatarBtn')
  .addEventListener('click', toggleDropdown);

// Đóng khi click ngoài vùng dropdown
document.getElementById('overlay').onclick = closeDropdown;
```

### Thay đổi thông tin admin

```html
<!-- 1. Avatar chữ (2 ký tự đầu tên) -->
<div class="avatar-btn" id="avatarBtn">TN</div>
<!-- Topbar -->
<div class="avatar">TN</div>
<!-- Sidebar -->
<div class="profile-avatar">TN</div>
<!-- Trong dropdown -->

<!-- 2. Tên và email -->
<div class="profile-name">Trần Ngọc</div>
<div class="profile-email">admin@filevault.vn</div>
<div class="profile-badge">SUPER ADMIN</div>

<!-- 3. Thống kê nhanh trong dropdown -->
<div class="pstat-val">142</div>
<!-- số actions -->
<div class="pstat-val">47d</div>
<!-- số ngày online -->
<div class="pstat-val">99%</div>
<!-- SLA -->
```

### Kết nối API admin info

```javascript
async function loadAdminProfile() {
  const res = await fetch('/api/auth/me');
  const admin = await res.json();
  // Kỳ vọng: { name: "Trần Ngọc", email: "admin@...", role: "SUPER ADMIN",
  //            initials: "TN", stats: { actions: 142, uptimeDays: 47, sla: 99 } }

  // Cập nhật tất cả avatar initials
  document
    .querySelectorAll('.avatar-btn, .avatar, .profile-avatar')
    .forEach((el) => {
      if (!el.querySelector('*')) el.textContent = admin.initials;
    });
  document.querySelector('.profile-name').textContent = admin.name;
  document.querySelector('.profile-email').textContent = admin.email;
  document.querySelector('.profile-badge').textContent = admin.role;
}
```

---

## 11. Kết nối API Server thực

### Bước 1: Tạo hàm `fetchAPI` dùng chung

Thêm vào đầu `<script>`:

```javascript
const API_BASE = 'https://your-server.com'; // ← đổi thành domain server của bạn
const TOKEN_KEY = 'fv_admin_token';

async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  const res = await fetch(API_BASE + endpoint, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: token ? `Bearer ${token}` : '',
      ...options.headers,
    },
  });

  if (res.status === 401) {
    window.location.href = '/login'; // Hết phiên đăng nhập
    return null;
  }

  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}
```

### Bước 2: Hàm tải toàn bộ dashboard

```javascript
async function loadDashboard() {
  try {
    showLoading(true);

    // Gọi song song tất cả API (nhanh hơn gọi tuần tự)
    const [stats, uploads, storage, files, activity, system] =
      await Promise.all([
        fetchAPI('/api/dashboard/stats'),
        fetchAPI('/api/dashboard/uploads?days=30'),
        fetchAPI('/api/storage/breakdown'),
        fetchAPI('/api/files/recent?limit=10'),
        fetchAPI('/api/activity?limit=8'),
        fetchAPI('/api/system/health'),
      ]);

    renderStats(stats);
    renderChart(uploads);
    renderStorage(storage);
    renderRecentFiles(files);
    renderActivity(activity);
    renderSystemHealth(system);
  } catch (err) {
    console.error('Dashboard load failed:', err);
    showError('Không thể tải dữ liệu. Kiểm tra kết nối server.');
  } finally {
    showLoading(false);
  }
}

// Gọi khi trang load xong
document.addEventListener('DOMContentLoaded', loadDashboard);
```

### Bước 3: Cấu trúc JSON server cần trả về

**`GET /api/dashboard/stats`**

```json
{
  "totalFiles": 48291,
  "fileChangePercent": 12.4,
  "fileChangeTrend": "up",
  "storageUsed": "2.38 TB",
  "storageTotal": "4 TB",
  "storagePercent": 59.5,
  "activeUsers": 842,
  "onlineNow": 64,
  "downloads": 18472,
  "downloadChangePercent": -3.1
}
```

**`GET /api/dashboard/uploads?days=30`**

```json
{
  "labels": ["08/02", "09/02", "10/02"],
  "uploads": [120, 95, 148],
  "downloads": [60, 45, 78]
}
```

**`GET /api/storage/breakdown`**

```json
[
  { "ext": "PDF", "label": "PDF Documents", "size": "486 GB", "percent": 34 },
  { "ext": "MP4", "label": "Videos", "size": "642 GB", "percent": 45 },
  { "ext": "IMG", "label": "Images", "size": "286 GB", "percent": 20 }
]
```

**`GET /api/files/recent?limit=10`**

```json
[
  {
    "id": "FV-00291",
    "name": "bao-cao-q3-2024.pdf",
    "ext": "PDF",
    "size": "4.2 MB",
    "user": "nguyenvana",
    "status": "active",
    "uploadedAt": "2024-11-08T10:30:00Z"
  }
]
```

**`GET /api/activity?limit=8`**

```json
[
  {
    "color": "green",
    "text": "<strong>nguyenvana</strong> đã upload thành công <strong>bao-cao.pdf</strong>",
    "time": "2 phút trước",
    "ip": "192.168.1.42",
    "type": "upload"
  }
]
```

**`GET /api/system/health`**

```json
{
  "cpu": {
    "percent": 34,
    "desc": "8-core · 3.6 GHz · Load avg: 2.7",
    "status": "normal"
  },
  "ram": {
    "percent": 67,
    "used": "21.4 GB",
    "total": "32 GB",
    "status": "moderate"
  },
  "uptime": {
    "percent": 99.98,
    "desc": "47 ngày · 14 giờ · 22 phút",
    "status": "online"
  }
}
```

---

## 12. Polling & Auto-refresh

Tự động làm mới dữ liệu mà không cần F5:

```javascript
// Làm mới toàn bộ mỗi 60 giây
setInterval(loadDashboard, 60_000);

// Hoặc làm mới từng phần riêng:
setInterval(loadSystemHealth, 10_000); // System: 10 giây
setInterval(loadActivity, 30_000); // Activity: 30 giây
setInterval(loadStats, 60_000); // Stats: 1 phút
setInterval(loadChart, 300_000); // Chart: 5 phút
```

**Dùng WebSocket cho activity feed realtime:**

```javascript
const ws = new WebSocket('wss://your-server.com/ws/activity');

ws.onmessage = (event) => {
  const log = JSON.parse(event.data);
  // Chèn mục mới lên đầu danh sách
  const container = document.querySelector('.activity-list');
  const newItem = createActivityItem(log);
  container.insertBefore(newItem, container.firstChild);
  // Xóa mục cuối nếu quá 8 mục
  if (container.children.length > 8) container.lastChild.remove();
};

ws.onclose = () => {
  setTimeout(() => reconnectWS(), 5000); // Tự kết nối lại sau 5 giây
};
```

---

## 13. Xử lý lỗi & Loading state

### Thêm loading skeleton

```javascript
function showLoading(isLoading) {
  document.querySelectorAll('.stat-card, .card, .sys-card').forEach((el) => {
    el.style.opacity = isLoading ? '0.4' : '1';
    el.style.pointerEvents = isLoading ? 'none' : '';
  });
}
```

### Thêm thông báo lỗi

```javascript
function showError(message) {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed; bottom: 24px; right: 24px; z-index: 9999;
    background: #1a1a1a; border: 1px solid #f87171; color: #f87171;
    padding: 12px 20px; border-radius: 10px;
    font-family: 'DM Mono', monospace; font-size: 13px;
    animation: fadeUp 0.3s ease;
  `;
  toast.textContent = '⚠ ' + message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 5000);
}
```

### Fallback khi API lỗi

```javascript
async function loadStats() {
  try {
    const data = await fetchAPI('/api/dashboard/stats');
    renderStats(data);
  } catch {
    // Giữ nguyên giá trị mock, chỉ thêm dấu hiệu lỗi
    document.querySelectorAll('.stat-val').forEach((el) => {
      el.style.color = 'var(--text-3)';
    });
  }
}
```

---

## CSS Variables — Bảng màu toàn cục

Tất cả màu sắc được định nghĩa trong `:root`. Chỉ cần đổi ở đây để thay đổi toàn bộ giao diện:

```css
:root {
  --bg: #0a0a0a; /* Nền chính (tối nhất) */
  --bg-2: #111111; /* Nền card, sidebar */
  --bg-3: #1a1a1a; /* Nền hover, input */
  --bg-4: #222222; /* Nền progress bar */
  --border: #2a2a2a; /* Viền mặc định */
  --border-light: #333333; /* Viền khi hover */
  --text: #f0f0f0; /* Chữ chính */
  --text-2: #a0a0a0; /* Chữ phụ */
  --text-3: #606060; /* Chữ nhạt (label, placeholder) */
  --white: #ffffff; /* Trắng tuyệt đối */
  --green: #4ade80; /* Màu thành công */
  --red: #f87171; /* Màu lỗi/nguy hiểm */
  --yellow: #fbbf24; /* Màu cảnh báo */
  --blue: #60a5fa; /* Màu thông tin */
  --sidebar-w: 64px; /* Chiều rộng sidebar thu gọn */
  --sidebar-expanded: 260px; /* Chiều rộng sidebar mở rộng */
}
```

> **Tip:** Để chuyển sang theme sáng, chỉ cần đảo các giá trị `--bg*` và `--text*`.

---

_FileVault Admin Dashboard · Phiên bản 1.0 · Cập nhật tháng 3/2024_
