async function startGateway() {
  const progressBar = document.getElementById('progress');
  const statusText = document.getElementById('status');
  const SERVER_ENDPOINT = 'https://vault-storage.me/ping/khoi-dong';

  let currentWidth = 0;
  let isConnected = false;

  // 1. Bộ đếm thời gian cho thanh load chạy đến 99%
  const loadingInterval = setInterval(() => {
    if (!isConnected) {
      if (currentWidth < 80) {
        currentWidth += Math.random() * 2; // Chạy nhanh lúc đầu
      } else if (currentWidth < 99) {
        currentWidth += (99 - currentWidth) * 0.1; // Càng gần 99 càng chậm
      }
      progressBar.style.width = currentWidth + '%';
      statusText.innerText = `CONNECTING... ${Math.floor(currentWidth)}%`;
    }
  }, 200);

  // 2. Vòng lặp kiểm tra Server (Ping)
  while (!isConnected) {
    try {
      const response = await fetch(SERVER_ENDPOINT);
      if (response.ok) {
        const data = await response.text();
        if (data === 'Pong!') {
          isConnected = true;
          clearInterval(loadingInterval); // Dừng bộ đếm 99%

          // 3. Vọt lên 100% khi có tín hiệu
          progressBar.style.width = '100%';
          statusText.innerText = 'SUCCESS! REDIRECTING...';
          statusText.style.color = '#000';

          setTimeout(() => {
            document.body.classList.add('fade-exit');
            window.location.href = 'https://vault-storage.meauth/login'; // Hoặc trang og muốn
          }, 1000);
        }
      }
    } catch (error) {
      await new Promise((res) => setTimeout(res, 2000)); // Thử lại sau 2s
    }
  }
}

window.addEventListener('load', startGateway);
