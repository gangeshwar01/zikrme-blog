// Enhanced hero slider with navigation controls and better transitions
(function(){
  const root = document.querySelector('.hero-slider');
  if(!root) return;
  
  const slides = Array.from(root.querySelectorAll('.slide'));
  const totalSlides = slides.length;
  
  if(totalSlides === 0) return;
  
  let currentIndex = 0;
  let autoplayInterval;
  const autoplayDelay = 5000; // 5 seconds
  
  // Create navigation dots
  function createNavigation() {
    if(totalSlides <= 1) return;
    
    const navContainer = document.createElement('div');
    navContainer.className = 'slider-nav';
    navContainer.style.cssText = `
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 8px;
      z-index: 10;
    `;
    
    slides.forEach((_, index) => {
      const dot = document.createElement('button');
      dot.className = 'nav-dot';
      dot.style.cssText = `
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 2px solid rgba(255,255,255,0.5);
        background: transparent;
        cursor: pointer;
        transition: all 0.3s ease;
      `;
      
      dot.addEventListener('click', () => goToSlide(index));
      navContainer.appendChild(dot);
    });
    
    root.appendChild(navContainer);
    updateNavigation();
  }
  
  // Create prev/next buttons
  function createControls() {
    if(totalSlides <= 1) return;
    
    const prevBtn = document.createElement('button');
    prevBtn.className = 'slider-control prev';
    prevBtn.innerHTML = '‹';
    prevBtn.style.cssText = `
      position: absolute;
      left: 20px;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(0,0,0,0.5);
      color: white;
      border: none;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      font-size: 24px;
      cursor: pointer;
      z-index: 10;
      transition: all 0.3s ease;
    `;
    
    const nextBtn = document.createElement('button');
    nextBtn.className = 'slider-control next';
    nextBtn.innerHTML = '›';
    nextBtn.style.cssText = `
      position: absolute;
      right: 20px;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(0,0,0,0.5);
      color: white;
      border: none;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      font-size: 24px;
      cursor: pointer;
      z-index: 10;
      transition: all 0.3s ease;
    `;
    
    prevBtn.addEventListener('click', () => goToSlide(currentIndex - 1));
    nextBtn.addEventListener('click', () => goToSlide(currentIndex + 1));
    
    root.appendChild(prevBtn);
    root.appendChild(nextBtn);
    
    // Hover effects
    [prevBtn, nextBtn].forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        btn.style.background = 'rgba(0,0,0,0.8)';
        btn.style.transform = 'translateY(-50%) scale(1.1)';
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.background = 'rgba(0,0,0,0.5)';
        btn.style.transform = 'translateY(-50%) scale(1)';
      });
    });
  }
  
  // Go to specific slide
  function goToSlide(index) {
    // Handle circular navigation
    if(index < 0) index = totalSlides - 1;
    if(index >= totalSlides) index = 0;
    
    // Remove active class from current slide
    slides[currentIndex].classList.remove('active');
    
    // Update current index
    currentIndex = index;
    
    // Add active class to new slide
    slides[currentIndex].classList.add('active');
    
    // Update navigation
    updateNavigation();
    
    // Restart autoplay
    restartAutoplay();
  }
  
  // Update navigation dots
  function updateNavigation() {
    const dots = root.querySelectorAll('.nav-dot');
    dots.forEach((dot, index) => {
      if(index === currentIndex) {
        dot.style.background = 'white';
        dot.style.borderColor = 'white';
      } else {
        dot.style.background = 'transparent';
        dot.style.borderColor = 'rgba(255,255,255,0.5)';
      }
    });
  }
  
  // Start autoplay
  function startAutoplay() {
    if(autoplayInterval) clearInterval(autoplayInterval);
    autoplayInterval = setInterval(() => {
      goToSlide(currentIndex + 1);
    }, autoplayDelay);
  }
  
  // Restart autoplay
  function restartAutoplay() {
    startAutoplay();
  }
  
  // Pause autoplay on hover
  function setupHoverPause() {
    root.addEventListener('mouseenter', () => {
      if(autoplayInterval) clearInterval(autoplayInterval);
    });
    
    root.addEventListener('mouseleave', () => {
      startAutoplay();
    });
  }
  
  // Initialize slider
  function init() {
    // Show first slide
    goToSlide(0);
    
    // Create navigation elements
    createNavigation();
    createControls();
    
    // Setup hover pause
    setupHoverPause();
    
    // Start autoplay if enabled
    if(root.dataset.autoplay === 'true') {
      startAutoplay();
    }
    
    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
      if(e.key === 'ArrowLeft') {
        goToSlide(currentIndex - 1);
      } else if(e.key === 'ArrowRight') {
        goToSlide(currentIndex + 1);
      }
    });
  }
  
  // Start initialization
  init();
})();

// Mobile nav toggle with outside click to close
(function(){
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('#site-nav');
  if(!toggle || !nav) return;
  
  // Toggle menu on button click
  toggle.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent event bubbling
    nav.classList.toggle('open');
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    // Check if the click is outside the navigation and toggle button
    if (!nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove('open');
    }
  });
  
  // Close menu when clicking on navigation links (optional UX improvement)
  const navLinks = nav.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
    });
  });
  
  // Close menu on escape key press
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      nav.classList.remove('open');
    }
  });
  
  // Close menu when scrolling
  let scrollTimeout;
  window.addEventListener('scroll', () => {
    if (nav.classList.contains('open')) {
      nav.classList.remove('open');
    }
  }, { passive: true });
})();

// Mobile YouTube video fallback and error handling
(function(){
  function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }
  
  function isChromeMobile() {
    return /Android.*Chrome/i.test(navigator.userAgent);
  }
  
  function createYouTubeFallback(videoId, container) {
    const fallbackDiv = document.createElement('div');
    fallbackDiv.className = 'youtube-fallback-container';
    fallbackDiv.style.cssText = `
      position: relative;
      width: 100%;
      aspect-ratio: 16/9;
      background: #000;
      border-radius: 8px;
      overflow: hidden;
    `;
    
    const fallbackLink = document.createElement('a');
    fallbackLink.href = `https://www.youtube.com/watch?v=${videoId}`;
    fallbackLink.target = '_blank';
    fallbackLink.rel = 'noopener noreferrer';
    fallbackLink.style.cssText = `
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #ff0000, #cc0000);
      color: white;
      text-decoration: none;
      padding: 20px;
      text-align: center;
      gap: 15px;
    `;
    
    fallbackLink.innerHTML = `
      <i class="ri-youtube-line" style="font-size: 48px; margin-bottom: 10px;"></i>
      <h3 style="margin: 0; font-size: 18px; font-weight: bold;">Watch on YouTube</h3>
      <p style="margin: 0; font-size: 14px; opacity: 0.9;">Tap to open in YouTube app</p>
      <div style="margin-top: 10px; padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 12px;">
        Better mobile experience
      </div>
    `;
    
    fallbackDiv.appendChild(fallbackLink);
    return fallbackDiv;
  }
  
  function handleYouTubeError(iframe) {
    if (!isMobile()) return;
    
    const originalSrc = iframe.src;
    const videoId = originalSrc.match(/embed\/([^?]+)/)?.[1];
    
    if (!videoId) return;
    
    // For Chrome mobile, replace immediately
    if (isChromeMobile()) {
      const fallback = createYouTubeFallback(videoId, iframe.parentNode);
      iframe.parentNode.replaceChild(fallback, iframe);
      return;
    }
    
    // For other mobile browsers, wait and check
    let checkCount = 0;
    const checkInterval = setInterval(() => {
      checkCount++;
      
      // Check if iframe is still loading or has error
      if (iframe.offsetHeight === 0 || checkCount >= 6) {
        clearInterval(checkInterval);
        const fallback = createYouTubeFallback(videoId, iframe.parentNode);
        iframe.parentNode.replaceChild(fallback, iframe);
      }
    }, 500);
  }
  
  // Apply to all YouTube iframes
  document.addEventListener('DOMContentLoaded', () => {
    const youtubeIframes = document.querySelectorAll('iframe[src*="youtube.com/embed"]');
    youtubeIframes.forEach(handleYouTubeError);
  });
})();

// Share button handling on post detail
(function(){
  const btn = document.querySelector('.share-btn');
  if(!btn) return;
  btn.addEventListener('click', async () => {
    const shareData = {
      title: btn.dataset.title || document.title,
      url: btn.dataset.url || window.location.href
    };
    try {
      if(navigator.share){
        await navigator.share(shareData);
      }else{
        await navigator.clipboard.writeText(shareData.url);
        btn.textContent = 'Link copied!';
        setTimeout(()=>{ btn.innerHTML = '<i class="ri-share-forward-line"></i> Share'; }, 1500);
        alert('Link copied to clipboard');
      }
    } catch (e) {
      console.error('Share failed', e);
    }
  });
})();

// Draggable floating mini video for destination detail and home page
(function initMiniVideo(){
  function setup(){
    const mini = document.querySelector('.floating-mini-video');
    if(!mini) return;

    // Ensure it overlays page layout
    if(mini.parentElement !== document.body){
      document.body.appendChild(mini);
    }

    const video = mini.querySelector('video');
    const iframe = mini.querySelector('iframe');
    const closeBtn = mini.querySelector('.close-mini-video');
    
    if(video){
      video.muted = true;
      video.play().catch(()=>{});
    }
    
    if(iframe){
      // YouTube iframe will handle autoplay based on URL parameters
    }

  if(closeBtn){
    closeBtn.addEventListener('click', () => mini.remove());
  }

    mini.style.position = 'fixed';
    mini.style.right = '16px';
    // place just below the hero by default (top offset) or bottom-right if no hero
    const heroEl = document.querySelector('.page-hero');
    const heroRect = heroEl ? heroEl.getBoundingClientRect() : null;
    const defaultTop = heroRect ? (window.scrollY + heroRect.bottom + 16) : undefined;
    if(defaultTop !== undefined && defaultTop < window.scrollY + window.innerHeight - 200){
      mini.style.top = defaultTop + 'px';
      mini.style.bottom = 'auto';
    } else {
      mini.style.bottom = '16px';
      mini.style.top = 'auto';
    }
    mini.style.width = '360px';
    mini.style.aspectRatio = '16/9';
    mini.style.zIndex = '1000';
    mini.style.boxShadow = '0 10px 25px rgba(0,0,0,0.25)';
    mini.style.borderRadius = '12px';
    mini.style.overflow = 'hidden';
    mini.style.background = '#000';

  if(video){
    video.style.width = '100%';
    video.style.height = '100%';
    video.style.objectFit = 'cover';
  }

  if(closeBtn){
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '6px';
    closeBtn.style.right = '8px';
    closeBtn.style.width = '28px';
    closeBtn.style.height = '28px';
    closeBtn.style.borderRadius = '999px';
    closeBtn.style.border = 'none';
    closeBtn.style.background = 'rgba(0,0,0,0.5)';
    closeBtn.style.color = '#fff';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.fontSize = '18px';
    closeBtn.style.lineHeight = '28px';
  }

  let isDragging = false;
  let startX = 0, startY = 0, startLeft = 0, startTop = 0;

  function onPointerDown(e){
    isDragging = true;
    const rect = mini.getBoundingClientRect();
    startLeft = rect.left;
    startTop = rect.top;
    startX = (e.touches ? e.touches[0].clientX : e.clientX);
    startY = (e.touches ? e.touches[0].clientY : e.clientY);
    document.addEventListener('mousemove', onPointerMove);
    document.addEventListener('mouseup', onPointerUp);
    document.addEventListener('touchmove', onPointerMove, {passive:false});
    document.addEventListener('touchend', onPointerUp);
  }

  function onPointerMove(e){
    if(!isDragging) return;
    e.preventDefault();
    const currentX = (e.touches ? e.touches[0].clientX : e.clientX);
    const currentY = (e.touches ? e.touches[0].clientY : e.clientY);
    const dx = currentX - startX;
    const dy = currentY - startY;
    let left = startLeft + dx;
    let top = startTop + dy;

    const rect = mini.getBoundingClientRect();
    const maxLeft = window.innerWidth - rect.width;
    const maxTop = window.innerHeight - rect.height;
    left = Math.min(Math.max(0, left), maxLeft);
    top = Math.min(Math.max(0, top), maxTop);

    mini.style.left = left + 'px';
    mini.style.top = top + 'px';
    mini.style.right = 'auto';
    mini.style.bottom = 'auto';
  }

  function onPointerUp(){
    isDragging = false;
    document.removeEventListener('mousemove', onPointerMove);
    document.removeEventListener('mouseup', onPointerUp);
    document.removeEventListener('touchmove', onPointerMove);
    document.removeEventListener('touchend', onPointerUp);
  }

    mini.addEventListener('mousedown', onPointerDown);
    mini.addEventListener('touchstart', onPointerDown, {passive:true});
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', setup);
    window.addEventListener('load', setup, {once:true});
  } else {
    setup();
  }
})();

