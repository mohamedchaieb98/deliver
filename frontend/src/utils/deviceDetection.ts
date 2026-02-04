// Simple device detection utility
export const isMobile = (): boolean => {
  if (typeof window === 'undefined') return false;
  
  // Check screen width
  const screenWidth = window.innerWidth <= 768;
  
  // Check user agent
  const userAgent = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
  
  // Check touch capability
  const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  
  // Return true if any condition suggests mobile
  return screenWidth || userAgent || hasTouch;
};

export const getDeviceType = (): 'mobile' | 'desktop' => {
  return isMobile() ? 'mobile' : 'desktop';
};