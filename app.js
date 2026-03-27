// ===========================
// 曼妮新娘 MANNY BRIDE - JS
// ===========================

document.addEventListener('DOMContentLoaded', () => {

  // ----- Navbar scroll effect -----
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // ----- Hamburger menu -----
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const navLinks = document.querySelector('.nav-links');
  if (hamburgerBtn) {
    hamburgerBtn.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
    });
  }

  // ----- Particle background -----
  const particlesContainer = document.getElementById('particles');
  if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      const size = Math.random() * 6 + 2;
      const x = Math.random() * 100;
      const delay = Math.random() * 8;
      const duration = Math.random() * 6 + 6;
      particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(201,137,106,0.6), transparent);
        left: ${x}%;
        top: ${Math.random() * 100}%;
        animation: particleFloat ${duration}s ${delay}s ease-in-out infinite;
        pointer-events: none;
      `;
      particlesContainer.appendChild(particle);
    }

    const style = document.createElement('style');
    style.textContent = `
      @keyframes particleFloat {
        0%, 100% { transform: translateY(0) scale(1); opacity: 0.4; }
        50% { transform: translateY(-60px) scale(1.5); opacity: 0.8; }
      }
    `;
    document.head.appendChild(style);
  }

  // ----- Counter animation -----
  const counters = document.querySelectorAll('.stat-num');
  let countersStarted = false;

  const animateCounter = (el) => {
    const target = parseInt(el.getAttribute('data-target'));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = Math.floor(current);
    }, 16);
  };

  const startCounters = () => {
    if (!countersStarted) {
      countersStarted = true;
      counters.forEach(counter => animateCounter(counter));
    }
  };

  // ----- Intersection Observer for all animations -----
  const observerOptions = { threshold: 0.15 };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');

        // Trigger counters when hero stats come into view
        if (entry.target.closest('#hero')) {
          startCounters();
        }

        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe fade-up elements
  document.querySelectorAll('.about-card, .case-card, .plan-card').forEach(el => {
    el.classList.add('fade-up');
    observer.observe(el);
  });

  // Observe timeline items
  document.querySelectorAll('.timeline-item').forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.15}s`;
    observer.observe(el);
  });

  // Trigger hero stats counter on load
  const heroSection = document.getElementById('hero');
  if (heroSection) {
    const heroObserver = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) startCounters();
    }, { threshold: 0.3 });
    heroObserver.observe(heroSection);
  }

  // ----- Smooth scroll for all anchor links -----
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        const offsetTop = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: offsetTop, behavior: 'smooth' });
      }
      // Close mobile menu
      if (window.innerWidth <= 768 && navLinks) {
        navLinks.style.display = 'none';
      }
    });
  });

  // ----- Download button click effects -----
  ['ios-download-btn', 'android-download-btn'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.addEventListener('click', () => {
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => btn.style.transform = '', 200);
        showToast('🚀 App即将上线，敬请期待！');
      });
    }
  });

  // ----- Plan buttons -----
  ['plan-starter-btn', 'plan-growth-btn', 'plan-premium-btn'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        showToast('💄 感谢您的关注！顾问将在24小时内与您联系');
      });
    }
  });

  // ----- Toast notification -----
  const showToast = (message) => {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 32px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: rgba(61,26,46,0.95);
      color: white;
      padding: 14px 28px;
      border-radius: 100px;
      font-size: 15px;
      font-weight: 500;
      z-index: 9999;
      backdrop-filter: blur(20px);
      border: 1px solid rgba(201,137,106,0.3);
      box-shadow: 0 10px 40px rgba(61,26,46,0.3);
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      opacity: 0;
    `;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  };

  // ----- Parallax on scroll -----
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const orbs = document.querySelectorAll('.hero-orb');
    orbs.forEach((orb, i) => {
      const speed = 0.1 + i * 0.05;
      orb.style.transform = `translateY(${scrollY * speed}px)`;
    });
  }, { passive: true });

  // ----- Initialize: start counter immediately if hero visible -----
  if (heroSection) {
    const rect = heroSection.getBoundingClientRect();
    if (rect.top < window.innerHeight) startCounters();
  }

  console.log('%c曼妮新娘 MANNY BRIDE', 'font-size:24px;font-weight:bold;color:#c9896a;');
  console.log('%c为高价值女性打造百万网红超级个人IP', 'font-size:14px;color:#6b4c5e;');
});
