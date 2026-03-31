/* app.js — 曼妮新娘 v3.0 */

/* ══ NAV scroll ══ */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.style.background = window.scrollY > 60
    ? 'rgba(6,6,13,0.97)' : 'rgba(6,6,13,0.8)';
});

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

/* ══ UPLOAD MODAL ══ */
let uploadStep = 1;

function openUploadModal(plan) {
  uploadStep = 1;
  renderStep(1);
  document.getElementById('uploadOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';

  // Pre-select plan/track radio if provided
  if (plan && typeof plan === 'string' && !['starter','growth','premium'].includes(plan)) {
    const radio = document.querySelector(`input[name="mtrack"][value="${plan}"]`);
    if (radio) radio.checked = true;
  }
}

function closeUploadModal() {
  document.getElementById('uploadOverlay').classList.remove('active');
  document.body.style.overflow = '';
}

function renderStep(n) {
  document.querySelectorAll('.modal-step').forEach(s => s.classList.remove('active'));
  const step = document.getElementById('ms-' + n);
  if (step) step.classList.add('active');
  document.getElementById('modalPrev').style.display = n === 1 ? 'none' : 'block';
  document.getElementById('modalNext').textContent = n === 3 ? '提交申请 ✓' : '下一步 →';
}

function modalStep(dir) {
  const maxStep = 3;
  if (dir === 1 && uploadStep === maxStep) {
    // Submit
    submitUpload();
    return;
  }
  uploadStep = Math.max(1, Math.min(maxStep, uploadStep + dir));
  renderStep(uploadStep);
}

function handlePhotos(input) {
  const previews = document.getElementById('uploadPreviews');
  previews.innerHTML = '';
  Array.from(input.files).slice(0, 10).forEach(file => {
    const url = URL.createObjectURL(file);
    const img = document.createElement('img');
    img.src = url;
    img.className = 'upload-preview-img';
    previews.appendChild(img);
  });
}

// Drag & drop
const dropZone = document.getElementById('dropZone');
if (dropZone) {
  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.style.borderColor = '#c9896a'; });
  dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = ''; });
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.style.borderColor = '';
    const dt = e.dataTransfer;
    const input = document.getElementById('photoInput');
    if (dt.files.length && input) {
      // simulate file input
      handlePhotos({ files: dt.files });
    }
  });
}

function submitUpload() {
  const name = document.getElementById('uName')?.value;
  const phone = document.getElementById('uPhone')?.value;
  const wechat = document.getElementById('uWechat')?.value;

  if (!phone && !wechat) {
    alert('请至少填写手机号或微信号，以便我们联系您。');
    return;
  }

  // Success
  const modal = document.getElementById('uploadModal');
  modal.innerHTML = `
    <div style="text-align:center;padding:40px 20px">
      <div style="font-size:3.5rem;margin-bottom:20px">🎉</div>
      <h3 style="font-family:var(--font-serif);font-size:1.5rem;margin-bottom:12px">申请已提交！</h3>
      <p style="color:var(--text-2);margin-bottom:8px">您的专属IP定制请求已收到</p>
      <p style="color:var(--text-2);font-size:.85rem">我们的团队将在<strong style="color:var(--gold-2)">24小时内</strong>通过微信与您联系</p>
      <p style="font-size:.8rem;color:#c9896a;margin-top:20px">微信：mannibride888</p>
      <button onclick="closeUploadModal()" style="
        margin-top:28px;padding:12px 36px;
        background:linear-gradient(135deg,#c9896a,#ff6b9d);
        color:#fff;border-radius:999px;font-weight:700;font-size:.9rem;
      ">好的</button>
    </div>`;
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
document.getElementById('uploadOverlay').addEventListener('click', e => {
  if (e.target === document.getElementById('uploadOverlay')) closeUploadModal();
});
document.getElementById('partnerOverlay').addEventListener('click', e => {
  if (e.target === document.getElementById('partnerOverlay')) closePartnerModal();
});

/* ══ Escape key ══ */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closeUploadModal();
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
