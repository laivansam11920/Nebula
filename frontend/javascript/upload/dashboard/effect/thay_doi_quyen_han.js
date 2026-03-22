async function fetchUserPower() {
  const API_URL = 'https://vault-storage.me/profile/get_power';

  try {
    const response = await fetch(API_URL, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Lỗi hệ thống: ${response.status}`);
    }

    const data = await response.json();
    const userPower = data.power || 'BASIC';
    const badge = document.querySelector('.am-badge-pro');

    if (badge) {
      const svgIcon = badge.querySelector('svg').outerHTML;
      badge.innerHTML = `${svgIcon} ${userPower.toUpperCase()}`;

      console.log('[UPDATE] Đã nâng cấp quyền hạn lên:', userPower);

      switch (userPower) {
        case 'admin-root':
          badge.style.cssText = `
            background: linear-gradient(#FFD700 0%, #FFA500 100%) !important;
            color: #1a1a1a !important;
            border: 0.1px solid #FFED4E !important;
            box-shadow: 
              0 0 8px rgba(255, 215, 0, 0.5),
              0 2px 6px rgba(0, 0, 0, 0.2),
              inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            font-weight: 800 !important;
            font-size: 10px !important;
            
            letter-spacing: 0.01em !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
            border-radius: 20px !important;
            animation: goldGlow 3s ease-in-out infinite !important;
          `;
          break;

        case 'PREMIUM':
          badge.style.cssText = `
            background: linear-gradient(#E8E8E8 0%, #C0C0C0 50%, #A8A8A8 100%) !important;
            color: #2a2a2a !important;
            border: 0.5px solid #F5F5F5 !important;
            box-shadow: 
              0 0 8px rgba(192, 192, 192, 0.4),
              0 2px 6px rgba(0, 0, 0, 0.15),
              inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
            font-weight: 800 !important;
            font-size: 10px !important;
            letter-spacing: 0.1em !important;
            text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1) !important;
            padding: 4px 12px !important;
            border-radius: 20px !important;
          `;
          break;
        default:
          badge.style.cssText =
            'color: #ffffff !important; opacity: 1 !important;';
      }
      const planElement = document.getElementById('goi');

      if (planElement) {
        const formattedPower =
          userPower.charAt(0).toUpperCase() + userPower.slice(1);
        planElement.innerHTML = `10 GB — ${formattedPower} plan`;
        console.log('[UPDATE] Đã nâng cấp gói lên: ' + newPlanName);
      }
    }
  } catch (error) {
    console.error('Nhưng! Có lỗi khi fetch quyền hạn:', error);
  }
}
document.addEventListener('DOMContentLoaded', fetchUserPower);
