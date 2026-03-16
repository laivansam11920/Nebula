/**
 * animations.js — Animation utilities for the login page.
 * Provides reusable helpers: skeleton shimmer, smooth element transitions,
 * stagger reveals, and typed-text effect.
 */

// ─── Skeleton Loader ────────────────────────────────────────────────────────

/**
 * Show a skeleton shimmer overlay inside `el`.
 * The overlay is removed when `hideSkeletonLoader(el)` is called.
 * @param {HTMLElement} el
 */
export function showSkeletonLoader(el) {
  if (!el || el.querySelector('.skeleton-overlay')) return;
  const overlay = document.createElement('div');
  overlay.className = 'skeleton-overlay';
  overlay.setAttribute('aria-hidden', 'true');
  overlay.innerHTML = `
    <div class="skeleton-line skeleton-line--title"></div>
    <div class="skeleton-line skeleton-line--subtitle"></div>
    <div class="skeleton-line skeleton-line--input"></div>
    <div class="skeleton-line skeleton-line--input"></div>
    <div class="skeleton-line skeleton-line--btn"></div>
  `;
  el.style.position = 'relative';
  el.appendChild(overlay);
}

/**
 * Hide and remove the skeleton overlay from `el`.
 * @param {HTMLElement} el
 */
export function hideSkeletonLoader(el) {
  if (!el) return;
  const overlay = el.querySelector('.skeleton-overlay');
  if (!overlay) return;
  overlay.classList.add('skeleton-overlay--fade-out');
  overlay.addEventListener('animationend', () => overlay.remove(), { once: true });
}

// ─── Smooth Transitions ──────────────────────────────────────────────────────

/**
 * Fade-in `el` from `translateY(offset)` to its natural position.
 * @param {HTMLElement} el
 * @param {object} opts
 * @param {number} [opts.duration=480] ms
 * @param {number} [opts.offset=24]  px
 * @param {string} [opts.easing='cubic-bezier(0.16,1,0.3,1)']
 */
export function fadeInUp(el, { duration = 480, offset = 24, easing = 'cubic-bezier(0.16,1,0.3,1)' } = {}) {
  if (!el) return;
  el.animate(
    [
      { opacity: 0, transform: `translateY(${offset}px)` },
      { opacity: 1, transform: 'translateY(0)' },
    ],
    { duration, easing, fill: 'both' }
  );
}

/**
 * Smoothly reveal a set of elements with a staggered delay.
 * @param {NodeList|HTMLElement[]} elements
 * @param {number} [staggerMs=60]
 */
export function staggerReveal(elements, staggerMs = 60) {
  [...elements].forEach((el, i) => {
    setTimeout(() => fadeInUp(el, { duration: 420, offset: 16 }), i * staggerMs);
  });
}

/**
 * Crossfade two elements: fade-out `outEl`, then fade-in `inEl`.
 * `outEl` is hidden (display:none) once the fade completes.
 * @param {HTMLElement} outEl
 * @param {HTMLElement} inEl
 * @param {number} [duration=350]
 */
export function crossFade(outEl, inEl, duration = 350) {
  const easing = 'cubic-bezier(0.4,0,0.2,1)';

  const outAnim = outEl.animate(
    [{ opacity: 1, transform: 'translateX(0)' }, { opacity: 0, transform: 'translateX(-20px)' }],
    { duration, easing, fill: 'forwards' }
  );

  outAnim.onfinish = () => {
    outEl.style.display = 'none';
    outEl.getAnimations().forEach((a) => a.cancel());
    inEl.style.display = '';
    inEl.animate(
      [{ opacity: 0, transform: 'translateX(20px)' }, { opacity: 1, transform: 'translateX(0)' }],
      { duration, easing, fill: 'forwards' }
    );
  };
}

// ─── Button Spinner ───────────────────────────────────────────────────────────

/**
 * Replace button content with a spinner, disable it, and store original HTML.
 * @param {HTMLButtonElement} btn
 */
export function setButtonLoading(btn) {
  if (!btn || btn.dataset.loading === 'true') return;
  btn.dataset.loading = 'true';
  btn.dataset.originalHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `
    <span class="btn-spinner" aria-hidden="true"></span>
    <span class="visually-hidden">Đang xử lý…</span>
  `;
}

/**
 * Restore a button from its loading state.
 * @param {HTMLButtonElement} btn
 */
export function clearButtonLoading(btn) {
  if (!btn || btn.dataset.loading !== 'true') return;
  btn.disabled = false;
  btn.innerHTML = btn.dataset.originalHtml || '';
  delete btn.dataset.loading;
  delete btn.dataset.originalHtml;
}

// ─── Ripple Effect ────────────────────────────────────────────────────────────

/**
 * Attach a material-style ripple to a button on click.
 * @param {HTMLButtonElement} btn
 */
export function attachRipple(btn) {
  btn.addEventListener('pointerdown', (e) => {
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 2;
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    ripple.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px`;
    btn.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
  });
}

// ─── Micro-interaction: shake ─────────────────────────────────────────────────

/**
 * Shake `el` briefly to signal an error.
 * @param {HTMLElement} el
 */
export function shakeElement(el) {
  if (!el) return;
  el.animate(
    [
      { transform: 'translateX(0)' },
      { transform: 'translateX(-8px)' },
      { transform: 'translateX(8px)' },
      { transform: 'translateX(-6px)' },
      { transform: 'translateX(6px)' },
      { transform: 'translateX(0)' },
    ],
    { duration: 400, easing: 'ease-in-out' }
  );
}
