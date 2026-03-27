(function () {
  'use strict';

  // ─── CONFIGURATION ─────────────────────────────────────────────
  const CONFIG = {
    API_URL: 'https://vault-storage.me/api/support/chat',
    WS_URL: 'wss://vault-storage.me/ws/support',
    BOT_NAME: 'VAULT Support',
    BOT_AVATAR:
      'https://res.cloudinary.com/dshgtuy8f/image/upload/v1771402917/main_logo_2_bkgj5f.png',
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    TYPING_DELAY: 800, // ms
  };

  // ─── INJECT CSS ────────────────────────────────────────────────
  const chatCSS = `
    /* Chat Button (Floating) */
    .chat-support-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #0a0a0a 0%, #333 100%);
      color: #fff;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
      z-index: 9998;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .chat-support-btn:hover {
      transform: scale(1.1);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    }

    .chat-support-btn.has-unread::after {
      content: '';
      position: absolute;
      top: 8px;
      right: 8px;
      width: 12px;
      height: 12px;
      background: #ff3b30;
      border: 2px solid #fff;
      border-radius: 50%;
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.2); opacity: 0.8; }
    }

    .chat-support-btn svg {
      width: 28px;
      height: 28px;
    }

    /* Chat Widget Container */
    .chat-widget-container {
      position: fixed;
      bottom: 100px;
      right: 24px;
      width: 400px;
      height: 600px;
      max-height: calc(100vh - 140px);
      background: var(--surface, #ffffff);
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
      display: flex;
      flex-direction: column;
      opacity: 0;
      transform: scale(0.9) translateY(20px);
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 9999;
      overflow: hidden;
    }

    .chat-widget-container.open {
      opacity: 1;
      transform: scale(1) translateY(0);
      pointer-events: all;
    }

    /* Chat Header */
    .chat-header {
      background: linear-gradient(135deg, #0a0a0a 0%, #333 100%);
      color: #fff;
      padding: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-radius: 20px 20px 0 0;
    }

    .chat-header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .chat-bot-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.15);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }

    .chat-bot-info {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .chat-bot-name {
      font-size: 15px;
      font-weight: 700;
      line-height: 1;
    }

    .chat-bot-status {
      font-size: 12px;
      opacity: 0.8;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .chat-bot-status-dot {
      width: 6px;
      height: 6px;
      background: #34c759;
      border-radius: 50%;
      animation: blink 2s ease-in-out infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }

    .chat-header-actions {
      display: flex;
      gap: 8px;
    }

    .chat-header-btn {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #fff;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }

    .chat-header-btn:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    .chat-header-btn svg {
      width: 16px;
      height: 16px;
    }

    /* Quick Actions */
    .chat-quick-actions {
      padding: 16px;
      background: var(--bg, #f5f5f3);
      border-bottom: 1px solid var(--border, #e0e0de);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .chat-quick-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--ink-4, #999);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .chat-quick-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .chat-quick-btn {
      padding: 6px 12px;
      background: var(--surface, #fff);
      border: 1px solid var(--border, #e0e0de);
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
      color: var(--ink-2, #333);
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .chat-quick-btn:hover {
      background: var(--ink, #0a0a0a);
      color: #fff;
      border-color: var(--ink, #0a0a0a);
    }

    /* Chat Messages */
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .chat-messages::-webkit-scrollbar {
      width: 6px;
    }

    .chat-messages::-webkit-scrollbar-thumb {
      background: var(--border-dark, #c0c0be);
      border-radius: 99px;
    }

    .chat-message {
      display: flex;
      gap: 10px;
      animation: messageIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes messageIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .chat-message.user {
      flex-direction: row-reverse;
    }

    .chat-message-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--bg, #f5f5f3);
      border: 1px solid var(--border, #e0e0de);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
    }

    .chat-message.user .chat-message-avatar {
      background: var(--ink, #0a0a0a);
      color: #fff;
      border: none;
    }

    .chat-message-content {
      max-width: 70%;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .chat-message-bubble {
      padding: 12px 16px;
      border-radius: 16px;
      font-size: 14px;
      line-height: 1.5;
      word-wrap: break-word;
    }

    .chat-message.bot .chat-message-bubble {
      background: var(--bg, #f5f5f3);
      color: var(--ink, #0a0a0a);
      border-radius: 16px 16px 16px 4px;
    }

    .chat-message.user .chat-message-bubble {
      background: var(--ink, #0a0a0a);
      color: #fff;
      border-radius: 16px 16px 4px 16px;
    }

    .chat-message-time {
      font-size: 11px;
      color: var(--ink-4, #999);
      padding: 0 4px;
    }

    .chat-message.user .chat-message-time {
      text-align: right;
    }

    /* Typing Indicator */
    .chat-typing {
      display: flex;
      gap: 10px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s;
    }

    .chat-typing.show {
      opacity: 1;
    }

    .chat-typing-bubble {
      padding: 12px 16px;
      background: var(--bg, #f5f5f3);
      border-radius: 16px 16px 16px 4px;
      display: flex;
      gap: 4px;
    }

    .chat-typing-dot {
      width: 8px;
      height: 8px;
      background: var(--ink-4, #999);
      border-radius: 50%;
      animation: typingDot 1.4s ease-in-out infinite;
    }

    .chat-typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .chat-typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typingDot {
      0%, 60%, 100% { transform: translateY(0); }
      30% { transform: translateY(-8px); }
    }

    /* Chat Input */
    .chat-input-container {
      padding: 16px;
      background: var(--surface, #fff);
      border-top: 1px solid var(--border, #e0e0de);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .chat-input-attachments {
      display: none;
      flex-wrap: wrap;
      gap: 8px;
    }

    .chat-input-attachments.has-files {
      display: flex;
    }

    .chat-attachment-item {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      background: var(--bg, #f5f5f3);
      border: 1px solid var(--border, #e0e0de);
      border-radius: 8px;
      font-size: 12px;
    }

    .chat-attachment-item svg {
      width: 14px;
      height: 14px;
      color: var(--ink-3, #666);
    }

    .chat-attachment-remove {
      background: none;
      border: none;
      padding: 0;
      cursor: pointer;
      color: var(--ink-4, #999);
      display: flex;
    }

    .chat-attachment-remove:hover {
      color: var(--ink, #0a0a0a);
    }

    .chat-input-wrapper {
      display: flex;
      gap: 8px;
      align-items: flex-end;
    }

    .chat-input {
      flex: 1;
      padding: 12px 16px;
      background: var(--bg, #f5f5f3);
      border: 1px solid var(--border, #e0e0de);
      border-radius: 12px;
      font-size: 14px;
      font-family: inherit;
      color: var(--ink, #0a0a0a);
      resize: none;
      max-height: 120px;
      transition: all 0.2s;
    }

    .chat-input:focus {
      outline: none;
      border-color: var(--ink, #0a0a0a);
      box-shadow: 0 0 0 3px rgba(10, 10, 10, 0.08);
    }

    .chat-input::placeholder {
      color: var(--ink-4, #999);
    }

    .chat-input-actions {
      display: flex;
      gap: 6px;
    }

    .chat-input-btn {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: var(--bg, #f5f5f3);
      border: 1px solid var(--border, #e0e0de);
      color: var(--ink-3, #666);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
      flex-shrink: 0;
    }

    .chat-input-btn:hover {
      background: var(--surface, #fff);
      border-color: var(--ink-3, #666);
      color: var(--ink, #0a0a0a);
    }

    .chat-input-btn.send {
      background: var(--ink, #0a0a0a);
      color: #fff;
      border: none;
    }

    .chat-input-btn.send:hover {
      background: #333;
      transform: scale(1.05);
    }

    .chat-input-btn.send:disabled {
      background: var(--border-dark, #c0c0be);
      cursor: not-allowed;
      transform: scale(1);
    }

    .chat-input-btn svg {
      width: 18px;
      height: 18px;
    }

    /* Welcome Message */
    .chat-welcome {
      text-align: center;
      padding: 40px 20px;
      color: var(--ink-3, #666);
    }

    .chat-welcome-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    .chat-welcome-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--ink, #0a0a0a);
      margin-bottom: 8px;
    }

    .chat-welcome-text {
      font-size: 14px;
      line-height: 1.6;
    }

    /* Responsive */
    @media (max-width: 480px) {
      .chat-widget-container {
        width: calc(100vw - 32px);
        height: calc(100vh - 120px);
        bottom: 90px;
        right: 16px;
      }

      .chat-support-btn {
        bottom: 16px;
        right: 16px;
      }
    }
  `;

  // Inject CSS
  const styleEl = document.createElement('style');
  styleEl.textContent = chatCSS;
  document.head.appendChild(styleEl);

  // ─── CREATE CHAT WIDGET HTML ───────────────────────────────────
  const chatHTML = `
    <!-- Floating Chat Button -->
    <button class="chat-support-btn" id="chatSupportBtn" onclick="toggleChatWidget()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </button>

    <!-- Chat Widget Container -->
    <div class="chat-widget-container" id="chatWidget">
      <!-- Header -->
      <div class="chat-header">
        <div class="chat-header-left">
          <div class="chat-bot-avatar">
            ${
              CONFIG.BOT_AVATAR.startsWith('http')
                ? `<img src="${CONFIG.BOT_AVATAR}" style="width:100%;height:100%;border-radius:50%;object-fit:cover">`
                : CONFIG.BOT_AVATAR
            }
            </div>
          <div class="chat-bot-info">
            <div class="chat-bot-name">${CONFIG.BOT_NAME}</div>
            <div class="chat-bot-status">
              <span class="chat-bot-status-dot"></span>
              Đang online
            </div>
          </div>
        </div>
        <div class="chat-header-actions">
          <button class="chat-header-btn" onclick="minimizeChatWidget()" title="Thu nhỏ">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </button>
          <button class="chat-header-btn" onclick="closeChatWidget()" title="Đóng">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="chat-quick-actions">
        <div class="chat-quick-label">Câu hỏi thường gặp</div>
        <div class="chat-quick-buttons">
          <button class="chat-quick-btn" onclick="sendQuickMessage('Làm sao để upload file?')">
            📤 Upload file
          </button>
          <button class="chat-quick-btn" onclick="sendQuickMessage('Tôi quên mật khẩu')">
            🔑 Quên mật khẩu
          </button>
          <button class="chat-quick-btn" onclick="sendQuickMessage('Nâng cấp gói lưu trữ')">
            ⬆️ Nâng cấp
          </button>
          <button class="chat-quick-btn" onclick="sendQuickMessage('Chia sẻ file với người khác')">
            🔗 Chia sẻ
          </button>
          <button class="chat-quick-btn" onclick="sendQuickMessage('Báo lỗi hệ thống')">
            🐛 Báo lỗi
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div class="chat-messages" id="chatMessages">
        <!-- Welcome Message -->
        <div class="chat-welcome">
          <div class="chat-welcome-icon">👋</div>
          <div class="chat-welcome-title">Xin chào!</div>
          <div class="chat-welcome-text">
            Chúng tôi có thể giúp gì cho bạn?<br>
            Chọn câu hỏi phía trên hoặc nhập tin nhắn bên dưới.
          </div>
        </div>

        <!-- Typing Indicator -->
        <div class="chat-typing" id="chatTyping">
          <div class="chat-message-avatar">
    ${
      CONFIG.BOT_AVATAR.startsWith('http')
        ? `<img src="${CONFIG.BOT_AVATAR}" style="width:100%;height:100%;border-radius:50%;object-fit:cover">`
        : CONFIG.BOT_AVATAR
    }
  </div>
          <div class="chat-typing-bubble">
            <span class="chat-typing-dot"></span>
            <span class="chat-typing-dot"></span>
            <span class="chat-typing-dot"></span>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container">
        <div class="chat-input-attachments" id="chatAttachments"></div>
        <div class="chat-input-wrapper">
          <textarea 
            class="chat-input" 
            id="chatInput" 
            placeholder="Nhập tin nhắn..."
            rows="1"
            onkeydown="handleChatKeydown(event)"
          ></textarea>
          <div class="chat-input-actions">
            <input type="file" id="chatFileInput" style="display:none" multiple onchange="handleFileSelect(event)">
            <button class="chat-input-btn" onclick="document.getElementById('chatFileInput').click()" title="Đính kèm file">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
              </svg>
            </button>
            <button class="chat-input-btn send" id="chatSendBtn" onclick="sendMessage()" disabled title="Gửi">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  // Inject HTML
  const container = document.createElement('div');
  container.innerHTML = chatHTML;
  document.body.appendChild(container.firstElementChild); // Button
  document.body.appendChild(container.firstElementChild); // Widget

  // ─── STATE ─────────────────────────────────────────────────────
  let chatOpen = false;
  let chatMessages = [];
  let attachedFiles = [];
  let ws = null;
  let unreadCount = 0;

  // ─── TOGGLE CHAT WIDGET ────────────────────────────────────────
  window.toggleChatWidget = function () {
    const widget = document.getElementById('chatWidget');
    const btn = document.getElementById('chatSupportBtn');

    chatOpen = !chatOpen;

    if (chatOpen) {
      widget.classList.add('open');
      document.getElementById('chatInput').focus();

      // Mark as read
      unreadCount = 0;
      btn.classList.remove('has-unread');

      // Connect WebSocket
      connectWebSocket();

      // Send welcome if first time
      if (chatMessages.length === 0) {
        setTimeout(() => {
          addBotMessage(
            'Xin chào! Tôi là trợ lý ảo của VAULT. Tôi có thể giúp gì cho bạn?'
          );
        }, 500);
      }
    } else {
      widget.classList.remove('open');
    }
  };

  window.minimizeChatWidget = function () {
    const widget = document.getElementById('chatWidget');
    widget.classList.remove('open');
    chatOpen = false;
  };

  window.closeChatWidget = function () {
    minimizeChatWidget();
    disconnectWebSocket();
  };

  // ─── WEBSOCKET ─────────────────────────────────────────────────
  function connectWebSocket() {
    try {
      ws = new WebSocket(CONFIG.WS_URL);

      ws.onopen = () => {
        console.log('[Chat] WebSocket connected');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };

      ws.onerror = (error) => {
        console.error('[Chat] WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('[Chat] WebSocket disconnected');
        // Retry after 3s
        setTimeout(() => {
          if (chatOpen) connectWebSocket();
        }, 3000);
      };
    } catch (error) {
      console.error('[Chat] WebSocket connection failed:', error);
    }
  }

  function disconnectWebSocket() {
    if (ws) {
      ws.close();
      ws = null;
    }
  }

  function handleWebSocketMessage(data) {
    if (data.type === 'message') {
      addBotMessage(data.content);
    } else if (data.type === 'typing') {
      showTypingIndicator();
    } else if (data.type === 'stop_typing') {
      hideTypingIndicator();
    }
  }

  // ─── SEND MESSAGE ──────────────────────────────────────────────
  window.sendMessage = async function () {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    // 1. Lấy danh sách tên file để gửi cho Gemini biết
    const fileNames = attachedFiles.map((f) => f.name);

    if (!message && fileNames.length === 0) return;

    if (message) addUserMessage(message);

    // Hiển thị các file đã đính kèm lên khung chat cho vui mắt
    attachedFiles.forEach((file) => {
      addUserMessage(`📎 ${file.name}`);
    });

    // Reset input
    const currentFiles = [...attachedFiles]; // Giữ bản sao để gửi API
    input.value = '';
    input.style.height = 'auto';
    attachedFiles = [];
    updateAttachmentsUI();
    updateSendButton();

    showTypingIndicator();

    try {
      const response = await fetch(CONFIG.API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Bắt buộc phải có
        },
        body: JSON.stringify({
          message: message,
          files: fileNames, // Gửi mảng tên file qua đây
          timestamp: new Date().toISOString(),
        }),
      });

      const data = await response.json();
      hideTypingIndicator();

      // Backend trả về { success: true, message: "..." }
      if (data.success && data.message) {
        addBotMessage(data.message);
      } else {
        addBotMessage('Có lỗi xảy ra từ phía server rồi og ơi! :)');
      }
    } catch (error) {
      hideTypingIndicator();
      console.error('Lỗi kết nối:', error);
      // Fallback nếu server sập
      setTimeout(() => {
        addBotMessage(generateBotResponse(message));
      }, 1000);
    }
  };

  // ─── QUICK MESSAGES ────────────────────────────────────────────
  window.sendQuickMessage = function (message) {
    document.getElementById('chatInput').value = message;
    sendMessage();
  };

  // ─── ADD MESSAGES ──────────────────────────────────────────────
  function addUserMessage(text) {
    const msg = {
      id: Date.now(),
      type: 'user',
      text: text,
      time: new Date().toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit',
      }),
    };

    chatMessages.push(msg);
    renderMessage(msg);
  }

  function addBotMessage(text) {
    const msg = {
      id: Date.now(),
      type: 'bot',
      text: text,
      time: new Date().toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit',
      }),
    };

    chatMessages.push(msg);
    renderMessage(msg);

    // Mark unread if chat closed
    if (!chatOpen) {
      unreadCount++;
      document.getElementById('chatSupportBtn').classList.add('has-unread');
    }
  }

  function renderMessage(msg) {
    const messagesContainer = document.getElementById('chatMessages');
    const welcome = messagesContainer.querySelector('.chat-welcome');

    // Remove welcome message
    if (welcome && chatMessages.length > 0) {
      welcome.remove();
    }

    const messageEl = document.createElement('div');
    messageEl.className = `chat-message ${msg.type}`;

    const avatar =
      msg.type === 'bot'
        ? CONFIG.BOT_AVATAR.startsWith('http')
          ? `<img src="${CONFIG.BOT_AVATAR}" style="width:100%;height:100%;border-radius:50%;object-fit:cover">`
          : CONFIG.BOT_AVATAR
        : getUserInitial();

    messageEl.innerHTML = `
      <div class="chat-message-avatar">${avatar}</div>
      <div class="chat-message-content">
        <div class="chat-message-bubble">${escapeHtml(msg.text)}</div>
        <div class="chat-message-time">${msg.time}</div>
      </div>
    `;

    // Insert before typing indicator
    const typingEl = document.getElementById('chatTyping');
    messagesContainer.insertBefore(messageEl, typingEl);

    // Scroll to bottom
    scrollToBottom();
  }

  // ─── TYPING INDICATOR ──────────────────────────────────────────
  function showTypingIndicator() {
    document.getElementById('chatTyping').classList.add('show');
    scrollToBottom();
  }

  function hideTypingIndicator() {
    document.getElementById('chatTyping').classList.remove('show');
  }

  // ─── FILE HANDLING ─────────────────────────────────────────────
  window.handleFileSelect = function (event) {
    const files = Array.from(event.target.files);

    files.forEach((file) => {
      // Check size
      if (file.size > CONFIG.MAX_FILE_SIZE) {
        if (typeof toast === 'function') {
          toast(`File "${file.name}" quá lớn (max 10MB)`);
        } else {
          alert(`File "${file.name}" quá lớn (max 10MB)`);
        }
        return;
      }

      attachedFiles.push(file);
    });

    updateAttachmentsUI();
    updateSendButton();

    // Clear input
    event.target.value = '';
  };

  function updateAttachmentsUI() {
    const container = document.getElementById('chatAttachments');

    if (attachedFiles.length === 0) {
      container.classList.remove('has-files');
      container.innerHTML = '';
      return;
    }

    container.classList.add('has-files');
    container.innerHTML = attachedFiles
      .map(
        (file, index) => `
      <div class="chat-attachment-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
          <polyline points="13 2 13 9 20 9"/>
        </svg>
        <span>${file.name}</span>
        <button class="chat-attachment-remove" onclick="removeAttachment(${index})">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
    `
      )
      .join('');
  }

  window.removeAttachment = function (index) {
    attachedFiles.splice(index, 1);
    updateAttachmentsUI();
    updateSendButton();
  };

  // ─── INPUT HANDLING ────────────────────────────────────────────
  const chatInput = document.getElementById('chatInput');

  chatInput.addEventListener('input', function () {
    // Auto-resize
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';

    // Update send button
    updateSendButton();
  });

  window.handleChatKeydown = function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  function updateSendButton() {
    const input = document.getElementById('chatInput');
    const btn = document.getElementById('chatSendBtn');
    const hasContent = input.value.trim() || attachedFiles.length > 0;

    btn.disabled = !hasContent;
  }

  // ─── UTILITIES ─────────────────────────────────────────────────
  function scrollToBottom() {
    const container = document.getElementById('chatMessages');
    setTimeout(() => {
      container.scrollTop = container.scrollHeight;
    }, 100);
  }

  function getUserInitial() {
    const name = localStorage.getItem('user_name') || 'U';
    return name.charAt(0).toUpperCase();
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // ─── BOT RESPONSE GENERATOR ────────────────────────────────────
  function generateBotResponse(userMessage) {
    const msg = userMessage.toLowerCase();

    // Predefined responses
    const responses = {
      upload:
        'Để upload file, bạn click vào nút "Upload" ở góc trên bên phải, hoặc kéo thả file vào dashboard. Hỗ trợ mọi định dạng file, tối đa 2GB/file (gói PRO).',
      'quên mật khẩu':
        'Bạn có thể reset mật khẩu bằng cách:\n1. Click "Quên mật khẩu" ở trang đăng nhập\n2. Nhập email đã đăng ký\n3. Kiểm tra email và làm theo hướng dẫn\n\nNếu không nhận được email, kiểm tra mục Spam nhé!',
      'nâng cấp':
        'VAULT có 3 gói:\n\n🆓 FREE: 2GB, 100MB/file\n⭐ PRO: 50GB, 2GB/file - 99k/tháng\n💎 PREMIUM: 500GB, 10GB/file - 249k/tháng\n\nClick "Nâng cấp" trong Settings để xem chi tiết!',
      'chia sẻ':
        'Để chia sẻ file:\n1. Click vào file muốn chia sẻ\n2. Click nút "Chia sẻ" ở panel bên phải\n3. Chọn quyền truy cập (View/Edit)\n4. Copy link và gửi cho người khác\n\nLink có thể đặt mật khẩu (gói PREMIUM).',
      lỗi: 'Rất tiếc về sự cố này! Vui lòng cung cấp:\n1. Mô tả lỗi\n2. Thời gian xảy ra\n3. Screenshot (nếu có)\n\nTeam support sẽ xử lý trong 24h. Email: support@vault.com',
      'xin chào': 'Xin chào! 👋 Tôi có thể giúp gì cho bạn?',
      'cảm ơn': 'Không có gì! Nếu cần hỗ trợ thêm, cứ nhắn nhé 😊',
      default:
        'Tôi đã ghi nhận câu hỏi của bạn. Một chuyên viên sẽ phản hồi sớm nhất. Hoặc bạn có thể:\n\n📧 Email: support@vault.com\n📞 Hotline: 1900-xxxx\n⏰ 8h - 22h hàng ngày',
    };

    // Match keywords
    for (const [keyword, response] of Object.entries(responses)) {
      if (msg.includes(keyword)) {
        return response;
      }
    }

    return responses.default;
  }

  // ─── INIT ──────────────────────────────────────────────────────
  console.log('[Chat Widget] Loaded - Click button to open');

  // Auto-open if URL param exists
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('support') === 'open') {
    setTimeout(() => toggleChatWidget(), 500);
  }
})();
