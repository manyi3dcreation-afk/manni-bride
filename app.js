/* app.js — 曼妮新娘 v4.0 Luxury Edition */

/* ══ NAV scroll ══ */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

/* ══ Language Toggle ══ */
function switchLang(lang) {
  document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
  localStorage.setItem('manee-lang', lang);
}

/* ══ Theme Switcher ══ */
function switchTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  document.querySelectorAll('.theme-dot').forEach(dot => {
    dot.classList.toggle('active', dot.dataset.theme === theme);
  });
  localStorage.setItem('manee-theme', theme);
}

// Restore saved preferences on load
(function() {
  const savedLang = localStorage.getItem('manee-lang');
  if (savedLang) switchLang(savedLang);
  const savedTheme = localStorage.getItem('manee-theme');
  if (savedTheme) switchTheme(savedTheme);
})();

/* ══ Hamburger ══ */
const hamburgerBtn = document.getElementById('hamburgerBtn');
const navLinks = document.getElementById('navLinks');
if (hamburgerBtn) {
  hamburgerBtn.addEventListener('click', () => {
    navLinks.classList.toggle('mobile-open');
    hamburgerBtn.classList.toggle('open');
  });
}

/* Mobile nav styles injected */
const mobileStyle = document.createElement('style');
mobileStyle.textContent = `
  @media(max-width:768px){
    #navLinks.mobile-open{
      display:flex;flex-direction:column;gap:0;
      position:fixed;top:68px;left:0;right:0;
      background:rgba(6,6,13,.98);
      border-bottom:1px solid rgba(255,255,255,.08);
      padding:16px 24px; z-index:999;
    }
    #navLinks.mobile-open li a{
      display:block;padding:14px 0;
      border-bottom:1px solid rgba(255,255,255,.06);
      font-size:1rem;
    }
    .hamburger.open span:nth-child(1){transform:translateY(7px) rotate(45deg)}
    .hamburger.open span:nth-child(2){opacity:0}
    .hamburger.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
  }`;
document.head.appendChild(mobileStyle);

/* ══ Smooth scroll nav links ══ */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      navLinks.classList.remove('mobile-open');
      hamburgerBtn.classList.remove('open');
    }
  });
});

/* ══ Hero IP Carousel ══ */
let currentIP = 0;
let ipTimer = null;

function switchIP(idx) {
  const cards = document.querySelectorAll('.ip-card');
  const dots = document.querySelectorAll('.ip-dot');
  cards.forEach(c => c.classList.remove('ip-card-active'));
  dots.forEach(d => d.classList.remove('active'));
  cards[idx] && cards[idx].classList.add('ip-card-active');
  dots[idx] && dots[idx].classList.add('active');
  currentIP = idx;
}

function startIPCarousel() {
  ipTimer = setInterval(() => {
    const total = document.querySelectorAll('.ip-card').length;
    switchIP((currentIP + 1) % total);
  }, 3500);
}

document.querySelectorAll('.ip-dot').forEach((dot, i) => {
  dot.addEventListener('click', () => {
    clearInterval(ipTimer);
    switchIP(i);
    startIPCarousel();
  });
});

startIPCarousel();

/* ══ Reveal on scroll ══ */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, i * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ══ Partner Calculator ══ */
let calcPrice = 298;

function updateCalc() {
  const clients = parseInt(document.getElementById('clientSlider').value);
  document.getElementById('clientVal').textContent = clients;
  const monthly = Math.round(clients * calcPrice * 0.3);
  animateNum('calcAmount', monthly, '¥ ', '');
}

function selectPlan(btn, price) {
  document.querySelectorAll('.calc-sel').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  calcPrice = price;
  updateCalc();
}

function animateNum(id, target, prefix = '', suffix = '') {
  const el = document.getElementById(id);
  if (!el) return;
  const start = 0;
  const dur = 600;
  const startTime = performance.now();
  function step(now) {
    const p = Math.min((now - startTime) / dur, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = prefix + Math.round(start + (target - start) * ease).toLocaleString('zh-CN') + suffix;
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

updateCalc();

/* ══ Track selection ══ */
window.selectedTrack = null;

function selectTrack(card, track) {
  document.querySelectorAll('.track-card').forEach(c => c.classList.remove('track-selected'));
  card.classList.add('track-selected');
  window.selectedTrack = track;

  // Add CSS for selected
  if (!document.getElementById('track-sel-style')) {
    const s = document.createElement('style');
    s.id = 'track-sel-style';
    s.textContent = `.track-selected{border-color:rgba(201,137,106,.6)!important;box-shadow:0 0 0 2px rgba(201,137,106,.2)!important;}`;
    document.head.appendChild(s);
  }

  // Auto open upload modal with track pre-selected
  setTimeout(() => openUploadModal(track), 200);
}

/* ══ INQUIRY MODAL (Auxiliary Form) ══ */
function openInquiryModal() {
  const overlay = document.getElementById('inquiryOverlay');
  if(overlay) {
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeInquiryModal() {
  const overlay = document.getElementById('inquiryOverlay');
  if(overlay) {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function submitInquiry() {
  const contact = document.getElementById('iContact')?.value;

  if (!contact || contact.trim() === '') {
    alert('请务必填写您的微信号或手机号，以便我们能够联系到您。');
    return;
  }

  // Success State
  const modal = document.getElementById('inquiryModal');
  if(modal) {
    modal.innerHTML = `
      <div style="text-align:center;padding:40px 20px">
        <div style="font-size:3.5rem;margin-bottom:20px">✅</div>
        <h3 style="font-family:var(--font-serif);font-size:1.5rem;margin-bottom:12px">留言已成功提交</h3>
        <p style="color:var(--text-2);margin-bottom:8px">主理人将在 <strong style="color:var(--primary)">24小时内</strong> 主动添加您！</p>
        <p style="color:var(--text-3);font-size:.85rem;margin-top:20px">您也可以随时主动添加微信：mannibride888</p>
        <button onclick="closeInquiryModal()" style="
          margin-top:28px;padding:12px 36px;
          background:linear-gradient(135deg,rgba(255,107,157,0.2),rgba(201,137,106,0.2));
          border:1px solid var(--primary);
          color:#fff;border-radius:999px;font-weight:400;font-size:.9rem;cursor:pointer;
        ">明白，关闭</button>
      </div>`;
  }
}

/* ══ PARTNER MODAL ══ */
function openPartnerModal() {
  document.getElementById('partnerOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closePartnerModal() {
  document.getElementById('partnerOverlay').classList.remove('active');
  document.body.style.overflow = '';
}

function submitPartner() {
  const phone = document.getElementById('pPhone')?.value;
  const wechat = document.getElementById('pWechat')?.value;
  if (!phone && !wechat) {
    alert('请至少填写手机号或微信号。');
    return;
  }
  const modal = document.getElementById('partnerModal');
  modal.innerHTML = `
    <div style="text-align:center;padding:40px 20px">
      <div style="font-size:3.5rem;margin-bottom:20px">💎</div>
      <h3 style="font-family:var(--font-serif);font-size:1.4rem;margin-bottom:12px">申请已提交！</h3>
      <p style="color:rgba(240,230,211,.65);margin-bottom:8px">欢迎加入曼妮新娘合伙人大家庭</p>
      <p style="color:rgba(240,230,211,.65);font-size:.85rem">专属顾问将在<strong style="color:#e8b87a">24小时内</strong>与您联系，为您开通合伙人后台</p>
      <p style="font-size:.8rem;color:#c9896a;margin-top:20px">微信：mannibride888</p>
      <button onclick="closePartnerModal()" style="
        margin-top:28px;padding:12px 36px;
        background:linear-gradient(135deg,#c9896a,#f5c842);
        color:#fff;border-radius:999px;font-weight:700;font-size:.9rem;
      ">好的</button>
    </div>`;
}

/* ══ Close modals on overlay click ══ */
document.getElementById('inquiryOverlay')?.addEventListener('click', e => {
  if (e.target === document.getElementById('inquiryOverlay')) closeInquiryModal();
});
document.getElementById('partnerOverlay')?.addEventListener('click', e => {
  if (e.target === document.getElementById('partnerOverlay')) closePartnerModal();
});

/* ══ Escape key ══ */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closeInquiryModal();
    closePartnerModal();
  }
});

/* ══ Floating CTA hide on hero ══ */
const floatBtn = document.getElementById('wechatFloat');
const heroSection = document.getElementById('hero');
if (floatBtn && heroSection) {
  const heroObserver = new IntersectionObserver(([entry]) => {
    floatBtn.style.opacity = entry.isIntersecting ? '0' : '1';
    floatBtn.style.pointerEvents = entry.isIntersecting ? 'none' : 'auto';
  }, { threshold: 0.3 });
  heroObserver.observe(heroSection);
}

/* ══ Counter animation on scroll ══ */
function animateCounters() {
  document.querySelectorAll('[data-target]').forEach(el => {
    const target = parseInt(el.getAttribute('data-target'));
    const start = performance.now();
    const dur = 1500;
    const step = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const ease = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(target * ease);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounters();
      statsObserver.disconnect();
    }
  });
}, { threshold: 0.3 });

const statsSection = document.querySelector('.matrix-stats');
if (statsSection) statsObserver.observe(statsSection);

/* ══ Platform node entrance animation ══ */
const nodeObserver = new IntersectionObserver(([entry]) => {
  if (entry.isIntersecting) {
    document.querySelectorAll('.p-node').forEach((node, i) => {
      setTimeout(() => {
        node.style.opacity = '1';
        node.style.transform = 'scale(1)';
      }, i * 80);
    });
    nodeObserver.disconnect();
  }
}, { threshold: 0.3 });

const matrixSection = document.querySelector('.matrix-visual');
if (matrixSection) {
  // Initially hide nodes for animation
  document.querySelectorAll('.p-node').forEach(n => {
    n.style.opacity = '0';
    n.style.transform = 'scale(0)';
    n.style.transition = 'opacity .4s, transform .4s';
  });
  nodeObserver.observe(matrixSection);
}


  // Energy Bar Animation logic from C193112
  function animateStats() {
    const stats = document.querySelectorAll('.stat-num');
    const bars = document.querySelectorAll('.stat-bar-fill');
    
    stats.forEach(stat => {
      const target = +stat.getAttribute('data-target');
      let current = 0;
      const increment = target / 40;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          stat.innerText = target;
          clearInterval(timer);
        } else {
          stat.innerText = Math.ceil(current);
        }
      }, 30);
    });

    bars.forEach(bar => {
      const width = bar.style.width;
      bar.style.width = '0';
      setTimeout(() => {
        bar.style.transition = 'width 1.5s ease-out';
        bar.style.width = width;
      }, 300);
    });
  }

  document.addEventListener('DOMContentLoaded', () => { if(typeof animateStats === 'function') animateStats(); });
