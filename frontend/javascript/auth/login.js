/**
 * login.js — Login page interaction logic.
 *
 * Handles:
 *  • 2-step form flow: step-1 (email) → step-2 (password)
 *  • API authentication via POST /auth/input-pass
 *  • Loading spinner on submit button
 *  • Toast notifications (success / error / info)
 *  • Dark-mode toggle (persisted in localStorage)
 *  • Socket.io global notifications
 *  • Maintenance / 503 check
 *  • Google OAuth redirect
 *  • Remember-me (prefill email from localStorage)
 */

import {
  fadeInUp,
  staggerReveal,
  crossFade,
  setButtonLoading,
  clearButtonLoading,
  attachRipple,
  shakeElement,
} from './animations.js';

import { showToast } from '../popup/popup.js';

// ─── Constants ──────────────────────────────────────────────────────────────

const API_URL =
  window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000'
    : 'https://vault-server-laivansam-gnfdcsgthfhraahe.eastasia-01.azurewebsites.net';

const DASHBOARD_URL = 'https://www.vault-storage.me/frontend/view/upload/dashboard/index.html';
const DASHBOARD_MOBILE_URL =
  'https://www.vault-storage.me/frontend/view/upload/dashboard/dashboard-mobile.html';
const MAINTENANCE_URL = 'https://www.vault-storage.me/frontend/view/error/503.html';
const SIGNUP_URL =
  'https://www.vault-storage.me/frontend/view/group_password/create_a_password.html';
const FORGOT_URL =
  'https://www.vault-storage.me/frontend/view/group_password/forgot_password.html';

// ─── DOM References ──────────────────────────────────────────────────────────

const loginCard = document.getElementById('login-card');
const step1 = document.getElementById('step-1');
const step2 = document.getElementById('step-2');

const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

const btnNext = document.getElementById('btn-next');
const btnBack = document.getElementById('btn-back');
const btnSubmit = document.getElementById('btn-submit');
const togglePasswordBtn = document.getElementById('toggle-password');

const themeToggle = document.getElementById('theme-toggle');
const googleBtn = document.getElementById('google-login-btn');
const facebookBtn = document.getElementById('facebook-login-btn');
const forgotLink = document.getElementById('forgot-link');
const signupLink = document.getElementById('signup-link');

const emailError = document.getElementById('email-error');
const passwordError = document.getElementById('password-error');

// ─── State ───────────────────────────────────────────────────────────────────

let currentStep = 1; // 1 = email step, 2 = password step

// ─── Utility ─────────────────────────────────────────────────────────────────

function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

function setInputError(inputEl, errorEl, message) {
  if (!inputEl || !errorEl) return;
  inputEl.classList.add('input--error');
  errorEl.textContent = message;
  errorEl.classList.add('visible');
  shakeElement(inputEl.closest('.input-field') || inputEl);
}

function clearInputError(inputEl, errorEl) {
  if (!inputEl || !errorEl) return;
  inputEl.classList.remove('input--error');
  errorEl.textContent = '';
  errorEl.classList.remove('visible');
}

// ─── Theme ───────────────────────────────────────────────────────────────────

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('auth-theme', theme);
  if (themeToggle) {
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Chuyển sang Light mode' : 'Chuyển sang Dark mode');
    themeToggle.title = themeToggle.getAttribute('aria-label');
  }
}

function initTheme() {
  const saved = localStorage.getItem('auth-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? 'dark' : 'light'));
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });
}

// ─── Step Management ─────────────────────────────────────────────────────────

function goToStep(target) {
  if (target === currentStep) return;

  if (target === 2) {
    // Validate email before advancing
    if (!isValidEmail(emailInput.value)) {
      setInputError(emailInput, emailError, 'Vui lòng nhập địa chỉ email hợp lệ.');
      emailInput.focus();
      return;
    }
    clearInputError(emailInput, emailError);
    // Show email summary in step 2
    const emailDisplay = document.getElementById('email-display');
    if (emailDisplay) emailDisplay.textContent = emailInput.value;
    crossFade(step1, step2);
    setTimeout(() => {
      passwordInput && passwordInput.focus();
    }, 400);
  } else {
    crossFade(step2, step1);
    setTimeout(() => {
      emailInput && emailInput.focus();
    }, 400);
  }

  currentStep = target;
  updateStepIndicator(target);
}

function updateStepIndicator(step) {
  document.querySelectorAll('.step-dot').forEach((dot, i) => {
    dot.classList.toggle('step-dot--active', i + 1 === step);
    dot.classList.toggle('step-dot--done', i + 1 < step);
  });
}

// ─── Form Submission ──────────────────────────────────────────────────────────

async function handleSubmit(e) {
  e.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  if (!password) {
    setInputError(passwordInput, passwordError, 'Vui lòng nhập mật khẩu.');
    passwordInput.focus();
    return;
  }
  clearInputError(passwordInput, passwordError);

  setButtonLoading(btnSubmit);
  showToast('info', 'Đang xác thực…');

  try {
    const response = await fetch(`${API_URL}/auth/input-pass`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ gmail: email, password }),
    });

    if (response.status === 200) {
      showToast('success', 'Đăng nhập thành công! Chào mừng bạn quay trở lại 🎉');
      localStorage.setItem('user_email', email);

      const remember = document.getElementById('remember');
      if (remember && remember.checked) {
        localStorage.setItem('remembered_email', email);
      } else {
        localStorage.removeItem('remembered_email');
      }

      setTimeout(() => {
        const dest = isMobile()
          ? `${DASHBOARD_MOBILE_URL}?useraccount=${encodeURIComponent(email)}`
          : `${DASHBOARD_URL}?useraccount=${encodeURIComponent(email)}`;
        window.location.href = dest;
      }, 1800);
    } else if (response.status === 401) {
      const data = await response.json().catch(() => ({}));
      const msg = data.message || 'Sai tài khoản hoặc mật khẩu!';
      showToast('error', `Đăng nhập thất bại: ${msg}`);
      clearButtonLoading(btnSubmit);
      setInputError(passwordInput, passwordError, msg);
      passwordInput.focus();
    } else {
      showToast('error', `Lỗi hệ thống: mã lỗi ${response.status}`);
      clearButtonLoading(btnSubmit);
    }
  } catch (err) {
    console.error('Lỗi kết nối:', err);
    showToast('error', 'Không thể kết nối máy chủ. Vui lòng thử lại.');
    clearButtonLoading(btnSubmit);
  }
}

// ─── Password Toggle ──────────────────────────────────────────────────────────

if (togglePasswordBtn && passwordInput) {
  togglePasswordBtn.addEventListener('click', () => {
    const isHidden = passwordInput.type === 'password';
    passwordInput.type = isHidden ? 'text' : 'password';
    togglePasswordBtn.classList.toggle('is-visible', isHidden);
    togglePasswordBtn.setAttribute('aria-label', isHidden ? 'Ẩn mật khẩu' : 'Hiện mật khẩu');
  });
}

// ─── Event Wiring ─────────────────────────────────────────────────────────────

if (btnNext) {
  btnNext.addEventListener('click', () => goToStep(2));
  attachRipple(btnNext);
}

if (btnBack) {
  btnBack.addEventListener('click', () => goToStep(1));
}

if (btnSubmit) {
  btnSubmit.addEventListener('click', handleSubmit);
  attachRipple(btnSubmit);
}

// Allow Enter key to advance / submit
if (emailInput) {
  emailInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      goToStep(2);
    }
  });
  // Live email validation feedback
  emailInput.addEventListener('input', () => {
    if (emailError && emailError.classList.contains('visible')) {
      if (isValidEmail(emailInput.value)) clearInputError(emailInput, emailError);
    }
  });
}

if (passwordInput) {
  passwordInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleSubmit(e);
  });
  passwordInput.addEventListener('input', () => {
    if (passwordError && passwordError.classList.contains('visible') && passwordInput.value) {
      clearInputError(passwordInput, passwordError);
    }
  });
}

// Navigation links
if (forgotLink) forgotLink.href = FORGOT_URL;
if (signupLink) signupLink.href = SIGNUP_URL;

// Google OAuth
if (googleBtn) {
  googleBtn.addEventListener('click', () => {
    window.location.href = `${API_URL}/auth/google`;
  });
  attachRipple(googleBtn);
}

// Facebook OAuth (placeholder — not yet implemented server-side)
if (facebookBtn) {
  facebookBtn.addEventListener('click', () => {
    showToast('info', 'Đăng nhập bằng Facebook chưa được hỗ trợ. Vui lòng dùng Google hoặc email.');
  });
  attachRipple(facebookBtn);
}

// ─── Remember Me ──────────────────────────────────────────────────────────────

function initRememberMe() {
  const saved = localStorage.getItem('remembered_email');
  if (saved && emailInput) {
    emailInput.value = saved;
    const remember = document.getElementById('remember');
    if (remember) remember.checked = true;
  }
}

// ─── Maintenance Check ────────────────────────────────────────────────────────

async function checkMaintenance() {
  try {
    const res = await fetch(`${API_URL}/ping/khoi-dong`);
    if (res.status === 503) window.location.href = MAINTENANCE_URL;
  } catch (_) {
    // Server starting or network issue — do nothing
  }
}

// ─── Socket.io Global Notifications ──────────────────────────────────────────

function initSocket() {
  if (typeof io === 'undefined') return;
  const socket = io(API_URL, {
    transports: ['polling', 'websocket'],
    withCredentials: true,
  });
  socket.on('global_notification', (data) => {
    showToast('info', `THÔNG BÁO: ${data.message}`);
  });
  socket.on('connect_error', (err) => console.error('Socket error:', err.message));
}

// ─── Page Init ────────────────────────────────────────────────────────────────

function init() {
  initTheme();
  initRememberMe();
  checkMaintenance();
  initSocket();

  // Initial entrance animation
  if (loginCard) fadeInUp(loginCard, { duration: 600, offset: 32 });
  if (step1) staggerReveal(step1.querySelectorAll('.form-group, .btn-primary, .btn-secondary, .divider, .social-row, .footer-links'));

  // Step 2 is hidden on load
  if (step2) step2.style.display = 'none';

  updateStepIndicator(1);
}

init();
