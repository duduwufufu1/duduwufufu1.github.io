/* ========================================
   GSAP Animations — duduwufufu1's Blog
   Docs: https://gsap.com/docs/
   ======================================== */

// Wait for DOM and GSAP to load
(function () {
  'use strict';

  function initAnimations() {
    // Guard: GSAP loaded?
    if (typeof gsap === 'undefined') {
      // Retry after a short delay if GSAP hasn't loaded yet
      if (typeof gsap === 'undefined') return;
    }

    // ---- Register ScrollTrigger (if available) ----
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);
    }

    // ---- Master Timeline for Page Load ----
    const master = gsap.timeline({
      defaults: { ease: 'power3.out' },
    });

    // 1. Avatar: scale + fade in
    master.fromTo(
      '.avatar img',
      { scale: 0.6, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.8, ease: 'back.out(1.7)' },
    );

    // 2. Nickname: slide up + fade
    master.fromTo(
      '.nickname',
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.6 },
      '-=0.4',
    );

    // 3. Description: slide up + fade
    master.fromTo(
      '.description',
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5 },
      '-=0.3',
    );

    // 4. Social links: stagger in
    master.fromTo(
      '.links .link-item',
      { y: 15, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.4, stagger: 0.08 },
      '-=0.2',
    );

    // ---- Navbar: Sticky & Blur on Scroll ----
    const navbar = document.querySelector('.navbar');
    if (navbar && typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.create({
        start: 'top -80px',
        onUpdate: (self) => {
          const isScrolled = self.progress > 0;
          navbar.style.boxShadow = isScrolled
            ? '0 1px 8px rgba(0,0,0,0.08)'
            : 'none';
          navbar.style.backdropFilter = isScrolled ? 'blur(8px)' : 'none';
        },
      });
    }

    // ---- Social Link Hover Animation ----
    document.querySelectorAll('.links .link-item').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        gsap.to(el, {
          y: -4,
          scale: 1.15,
          duration: 0.3,
          ease: 'back.out(2)',
          overwrite: 'auto',
        });
      });
      el.addEventListener('mouseleave', function () {
        gsap.to(el, {
          y: 0,
          scale: 1,
          duration: 0.3,
          ease: 'power2.out',
          overwrite: 'auto',
        });
      });
    });

    // ---- Avatar Hover ----
    const avatarImg = document.querySelector('.avatar img');
    if (avatarImg) {
      avatarImg.addEventListener('mouseenter', function () {
        gsap.to(avatarImg, {
          scale: 1.08,
          boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
          duration: 0.4,
          ease: 'back.out(1.7)',
          overwrite: 'auto',
        });
      });
      avatarImg.addEventListener('mouseleave', function () {
        gsap.to(avatarImg, {
          scale: 1,
          boxShadow: 'none',
          duration: 0.3,
          ease: 'power2.out',
          overwrite: 'auto',
        });
      });
    }

    // ---- Dark Mode Toggle Animation ----
    const toggleLabel = document.querySelector('.toggleBtn');
    const toggleCheckbox = document.getElementById('switch_default');
    if (toggleLabel && toggleCheckbox) {
      toggleLabel.addEventListener('click', function () {
        // Animate the toggle dot
        gsap.to(toggleLabel.querySelector('::after'), {
          duration: 0.2,
          ease: 'power2.inOut',
        });
        // Animate body background transition
        gsap.to('body', {
          backgroundColor: toggleCheckbox.checked
            ? getComputedStyle(document.documentElement)
                .getPropertyValue('--color-bg-dark')
                .trim()
            : getComputedStyle(document.documentElement)
                .getPropertyValue('--color-bg')
                .trim(),
          duration: 0.3,
          ease: 'power2.inOut',
        });
      });
    }

    // ---- Scroll-Triggered Fade-Ins (for archive/post pages) ----
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.utils.toArray('.post-card, .article-item, .post-item, .archive-item').forEach(function (el, i) {
        gsap.fromTo(
          el,
          { y: 30, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.5,
            delay: i * 0.08,
            scrollTrigger: {
              trigger: el,
              start: 'top 85%',
              toggleActions: 'play none none none',
            },
          },
        );
      });

      // Staggered text lines in articles
      gsap.utils.toArray('.post-content p, .post-content h2, .post-content h3, .post-content blockquote').forEach(function (el, i) {
        gsap.fromTo(
          el,
          { y: 20, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.4,
            delay: i * 0.04,
            scrollTrigger: {
              trigger: el,
              start: 'top 88%',
              toggleActions: 'play none none none',
            },
          },
        );
      });
    }

    // ---- Page Transition Loading Bar ----
    const loadingBar = document.createElement('div');
    loadingBar.className = 'loading-bar';
    document.body.prepend(loadingBar);

    gsap.to(loadingBar, {
      width: '100%',
      duration: 0.8,
      ease: 'power2.inOut',
      onComplete: function () {
        gsap.to(loadingBar, {
          opacity: 0,
          duration: 0.4,
          delay: 0.1,
          onComplete: function () {
            loadingBar.remove();
          },
        });
      },
    });
  }

  // Run on DOMContentLoaded; fallback if already loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnimations);
  } else {
    initAnimations();
  }
})();
