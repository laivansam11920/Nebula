const particlesContainer = document.getElementById('particles');
for (let i = 0; i < 50; i++) {
  const particle = document.createElement('div');
  particle.className = 'particle';
  particle.style.left = Math.random() * 100 + '%';
  particle.style.animationDelay = Math.random() * 15 + 's';
  particle.style.animationDuration = Math.random() * 10 + 10 + 's';
  particlesContainer.appendChild(particle);
}

let progress = 0;
let isServerAwake = false;
const progressBar = document.getElementById('progressBar');
const percentageText = document.getElementById('percentage');

const API_URL =
  window.location.hostname === 'localhost' ||
  window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000'
    : 'https://vault-storage.me/';

async function wakeUpServer() {
  try {
    console.log('Đang gọi server...');
    const response = await fetch(`${API_URL}/ping/khoi-dong`);
    if (response.ok) {
      console.log('Server đã dậy!');
      isServerAwake = true;
    }
  } catch (error) {
    if (!isServerAwake) setTimeout(wakeUpServer, 2000);
  }
}

function updateProgress() {
  if (progress < 100) {
    if (progress < 90) {
      progress += Math.random() * 3;
    } else if (!isServerAwake) {
      progress += 0.05;
      if (progress >= 99) progress = 99;
    } else {
      progress += 10;
    }

    if (progress > 100) progress = 100;

    progressBar.style.width = progress + '%';
    percentageText.textContent = Math.floor(progress) + '%';

    const delay = progress < 30 ? 100 : progress < 70 ? 150 : 200;
    setTimeout(updateProgress, delay);
  } else {
    setTimeout(() => {
      window.location.href = 'https://vault-storage.me/auth/login';
    }, 800);
  }
}
wakeUpServer();
updateProgress();
