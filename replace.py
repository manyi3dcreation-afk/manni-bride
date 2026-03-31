import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title & Meta
content = re.sub(r'<title>.*?</title>', '<title>曼妮新娘 | 打造 7x24 持续进化的超级个人IP</title>', content)
content = re.sub(r'<meta name="description".*?/>', '<meta name="description" content="从人设、形象、内容到平台运营，曼妮新娘帮你打造数字分身与超级个人IP，让你被看见、被记住，并逐步走向更高价值的成交。" />', content)

# Nav Links
nav_links = """<ul class="nav-links" id="navLinks">
        <li><a href="#about">系统价值</a></li>
        <li><a href="#audience">适合谁</a></li>
        <li><a href="#workflow">交付流程</a></li>
        <li><a href="#ips">明星IP</a></li>
        <li><a href="#plans">服务套餐</a></li>
      </ul>"""
content = re.sub(r'<ul class="nav-links" id="navLinks">.*?</ul>', nav_links, content, flags=re.DOTALL)

# Nav Actions
nav_actions = """<div class="nav-actions">
        <a href="mailto:hello@maneebrides.shop" class="nav-partner-btn">联系顾问</a>
        <button class="nav-cta" onclick="document.getElementById('plans').scrollIntoView()">立即定制</button>
      </div>"""
content = re.sub(r'<div class="nav-actions">.*?</div>', nav_actions, content, flags=re.DOTALL)

# Hero Section
hero_eyebrow = """<div class="hero-eyebrow">
          <span class="eyebrow-dot"></span>
          <span>超级个人IP · 数字分身 · 全平台运营</span>
        </div>"""
content = re.sub(r'<div class="hero-eyebrow">.*?</div>', hero_eyebrow, content, flags=re.DOTALL)

hero_title = """<h1 class="hero-title">
          <span class="ht-line1">为你打造 7×24</span>
          <span class="ht-line2 gradient-text">持续进化的</span>
          <span class="ht-line3">超级个人IP</span>
        </h1>"""
content = re.sub(r'<h1 class="hero-title">.*?</h1>', hero_title, content, flags=re.DOTALL)

hero_desc = """<p class="hero-desc">
          从人设、形象、内容到平台运营，曼妮新娘帮你打造数字分身与超级个人IP，<br />
          <em>让你被看见、被记住，并逐步走向更高价值的成交。</em>
        </p>"""
content = re.sub(r'<p class="hero-desc">.*?</p>', hero_desc, content, flags=re.DOTALL)

hero_cta = """<div class="hero-dual-cta">
          <button class="dual-cta-btn cta-c" id="hero-cta-c" onclick="document.getElementById('plans').scrollIntoView()">
            <div class="dcta-icon">✨</div>
            <div class="dcta-text">
              <strong>查看服务套餐</strong>
              <span>明确变现闭环与阶梯</span>
            </div>
            <div class="dcta-arrow">→</div>
          </button>
          <button class="dual-cta-btn cta-b" id="hero-cta-b" onclick="document.getElementById('plans').scrollIntoView()">
            <div class="dcta-icon">💎</div>
            <div class="dcta-text">
              <strong>先做IP诊断</strong>
              <span>寻找最适合你的商业路径</span>
            </div>
            <div class="dcta-arrow">→</div>
          </button>
        </div>"""
content = re.sub(r'<div class="hero-dual-cta">.*?</div>', hero_cta, content, flags=re.DOTALL)

hero_trust = """<div class="hero-trust">
          <span class="trust-item"><span class="trust-num">人设</span> 定位</span>
          <span class="trust-divider\">|</span>
          <span class="trust-item"><span class="trust-num">数字</span> 分身</span>
          <span class="trust-divider\">|</span>
          <span class="trust-item"><span class="trust-num">7×24h</span> 平台运营</span>
        </div>"""
content = re.sub(r'<div class="hero-trust">.*?</div>', hero_trust, content, count=1, flags=re.DOTALL)

what_we_do = """
  <section class="section dark-section" id="about">
    <div class="container">
      <div class="section-header">
        <div class="section-tag light">系统价值</div>
        <h2 class="section-title light">一套真正能走向商业价值的<br /><span class="gradient-text-light">个人IP系统</span></h2>
      </div>
      <div style="max-width: 800px; margin: 0 auto; text-align: center; color: #a1a1aa; font-size: 1.15rem; line-height: 2.2;">
        <p style="font-size: 1.3rem; font-weight: 500; margin-bottom: 2rem; color: #fff;">
          我们不只帮你发内容，<br/>我们为您打造一个能持续表达、持续吸引、持续进化的核心商业资产。
        </p>
        <p><strong>账号定位：</strong>为你找到最具差异化的变现人设；</p>
        <p><strong>数字分身：</strong>解决每天出片、拍摄的高昂成本与容貌焦虑；</p>
        <p><strong>平台分发：</strong>从小红书到海外社交媒体，全天候全自动曝光；</p>
        <p><strong>商业承接：</strong>用信任感极高的视觉内容，沉淀精准粉丝。</p>
      </div>
    </div>
  </section>
"""
content = content.replace('<!-- ══ HOW IT WORKS ══ -->', what_we_do + '\n  <!-- ══ HOW IT WORKS ══ -->')

workflow_str = """<section class="section how-section" id="workflow">
    <div class="container">
      <div class="section-header">
        <div class="section-tag">交付流程</div>
        <h2 class="section-title">五步服务流程：<br /><span class="gradient-text">如何为你打造超级IP</span></h2>
      </div>
      <div class="steps-flow" style="display:flex; flex-wrap:wrap; justify-content:center; gap:2rem">
        <div class="step-item reveal" style="flex:1 1 250px">
          <div class="step-num">01</div>
          <div class="step-icon-ring">📸</div>
          <h3>诊断定位与方向</h3>
          <p>出具最容易变现的赛道切入报告及风格调性。</p>
        </div>
        <div class="step-item reveal" style="flex:1 1 250px">
          <div class="step-num">02</div>
          <div class="step-icon-ring">🎭</div>
          <h3>建立数字分身形象</h3>
          <p>构建符合全网高级审美的基础数字影像与分身资产。</p>
        </div>
        <div class="step-item reveal" style="flex:1 1 250px">
          <div class="step-num">03</div>
          <div class="step-icon-ring">🎯</div>
          <h3>明确重点与内容</h3>
          <p>锁定平台级打法策略，规划能够高赞、高转化的人设图文。</p>
        </div>
        <div class="step-item reveal" style="flex:1 1 250px">
          <div class="step-num">04</div>
          <div class="step-icon-ring">📈</div>
          <h3>持续输出与微调</h3>
          <p>每日自动化高频内容分发，结合业务指标不断优化细节。</p>
        </div>
        <div class="step-item reveal" style="flex:1 1 250px">
          <div class="step-num">05</div>
          <div class="step-icon-ring">💎</div>
          <h3>积累信任与成交</h3>
          <p>形成全网可见度，最终自然顺畅地承接咨询接单和单子。</p>
        </div>
      </div>
    </div>
  </section>"""
content = re.sub(r'<section class="section how-section dark-section".*?</section>', workflow_str, content, flags=re.DOTALL)

audience_str = """<section class="section tracks-section dark-section" id="audience" style="background:#0F1014">
    <div class="container">
      <div class="section-header">
        <div class="section-tag light">适合人群</div>
        <h2 class="section-title light">这套服务<br /><span class="gradient-text-light">正好适合你</span></h2>
        <p class="section-desc light">通过精准的标签对号入座，找到自己目前最大的瓶颈与解法</p>
      </div>
      <div class="tracks-grid">
        <div class="track-card">
          <div class="track-bg" style="--tgc1:#7c3aed;--tgc2:#c026d3"></div>
          <div class="track-icon">01</div>
          <div class="track-content">
            <h3 style="font-size:1.15rem; line-height:1.6; margin-top:1rem; min-height:60px">想做个人IP赚取商业红利，但卡在不会定位和起步的人</h3>
            <p style="margin-top:1rem; font-size:0.9rem; color:#a1a1aa">帮你挖掘商业变现基底，梳理内容策略。</p>
          </div>
        </div>
        <div class="track-card">
          <div class="track-bg" style="--tgc1:#c9896a;--tgc2:#f5c842"></div>
          <div class="track-icon">02</div>
          <div class="track-content">
            <h3 style="font-size:1.15rem; line-height:1.6; margin-top:1rem; min-height:60px">时间有限，不想每天纠结穿搭、布景和修图的人</h3>
            <p style="margin-top:1rem; font-size:0.9rem; color:#a1a1aa">通过数字分身一次解决容貌焦虑与产出效率。</p>
          </div>
        </div>
        <div class="track-card">
          <div class="track-bg" style="--tgc1:#0ea5e9;--tgc2:#6366f1"></div>
          <div class="track-icon">03</div>
          <div class="track-content">
            <h3 style="font-size:1.15rem; line-height:1.6; margin-top:1rem; min-height:60px">希望在小红书、抖音、TikTok进行全阵地收网的人</h3>
            <p style="margin-top:1rem; font-size:0.9rem; color:#a1a1aa">极低成本撬动全球8大平台矩阵自动化运营。</p>
          </div>
        </div>
        <div class="track-card">
          <div class="track-bg" style="--tgc1:#be185d;--tgc2:#9d174d"></div>
          <div class="track-icon">04</div>
          <div class="track-content">
            <h3 style="font-size:1.15rem; line-height:1.6; margin-top:1rem; min-height:60px">想把高端的形象审美与真实的商业转化价值连在一起的人</h3>
            <p style="margin-top:1rem; font-size:0.9rem; color:#a1a1aa">曼妮独家高级赛道审美品控。</p>
          </div>
        </div>
        <div class="track-card">
          <div class="track-bg" style="--tgc1:#8b5cf6;--tgc2:#06b6d4"></div>
          <div class="track-icon">05</div>
          <div class="track-content">
            <h3 style="font-size:1.15rem; line-height:1.6; margin-top:1rem; min-height:60px">品牌出海或有全域影响力诉求的高端个体验</h3>
            <p style="margin-top:1rem; font-size:0.9rem; color:#a1a1aa">提供驻场团队协助外网霸榜与商单承接。</p>
          </div>
        </div>
        <div class="track-card">
          <div class="track-bg" style="--tgc1:#333;--tgc2:#666"></div>
          <div class="track-icon">💼</div>
          <div class="track-content">
            <h3 style="font-size:1.15rem; line-height:1.6; margin-top:1rem; min-height:60px">还不确定适合哪个？</h3>
            <div class="track-select-btn" onclick="document.getElementById('plans').scrollIntoView()" style="margin-top:1rem">先做IP诊断 →</div>
          </div>
        </div>
      </div>
    </div>
  </section>"""
content = re.sub(r'<section class="section tracks-section".*?</section>', audience_str, content, flags=re.DOTALL)

plans_str = """<section class="section plans-section" id="plans">
    <div class="container">
      <div class="section-header">
        <div class="section-tag">服务套餐明细</div>
        <h2 class="section-title">选择适合你的<br /><span class="gradient-text">服务套餐</span></h2>
        <p class="section-desc">清晰明朗的变现阶梯，找到你当前最该做的事。</p>
      </div>
      <div class="plans-grid" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));">
        <div class="plan-card">
          <div class="plan-name">IP定位诊断</div>
          <div class="plan-price"><span class="price-currency">¥</span><span class="price-num">199</span></div>
          <ul class="plan-features">
            <li><strong style="color:#7c3aed">适合谁：</strong>准备起步、找不到自己优势赛道的人。</li>
            <li><strong style="color:#7c3aed">服务重点：</strong>深度报告挖掘变现基底与人设风格，避坑。</li>
          </ul>
          <button class="plan-btn" onclick="window.location.href='checkout.html'">先做IP诊断</button>
        </div>
        <div class="plan-card">
          <div class="plan-name">单平台基础起号</div>
          <div class="plan-price"><span class="price-currency">¥</span><span class="price-num">698</span><span class="price-period">/月</span></div>
          <ul class="plan-features">
            <li><strong style="color:#c9896a">适合谁：</strong>想在单一平台低门槛跑通变现闭环的人。</li>
            <li><strong style="color:#c9896a">服务重点：</strong>建立分身模型，每日产出拉升账号基础权重。</li>
          </ul>
          <button class="plan-btn" onclick="window.location.href='checkout.html'">咨询 698 方案</button>
        </div>
        <div class="plan-card featured-plan">
          <div class="plan-badge">爆款推荐</div>
          <div class="plan-name">单平台分身强化</div>
          <div class="plan-price"><span class="price-currency">¥</span><span class="price-num">1,280</span><span class="price-period">/月</span></div>
          <ul class="plan-features">
            <li><strong style="color:#0ea5e9">适合谁：</strong>要求高质感视觉以承接高客单商单的创作者。</li>
            <li><strong style="color:#0ea5e9">服务重点：</strong>多风格分身组合，大幅提升高级感与爆款率。</li>
          </ul>
          <button class="plan-btn featured-btn" onclick="window.location.href='checkout.html'">咨询 1280 方案</button>
        </div>
        <div class="plan-card premium-plan">
          <div class="plan-badge premium-badge">全网核心</div>
          <div class="plan-name">全平台超级定制</div>
          <div class="plan-price"><span class="price-currency">¥</span><span class="price-num">4,980</span><span class="price-period">/月起</span></div>
          <ul class="plan-features">
            <li><strong style="color:#db2777">适合谁：</strong>拥有清晰品牌出海及全球多平台起号影响力的个体。</li>
            <li><strong style="color:#db2777">服务重点：</strong>五大核心社媒全线霸榜与主管驻场。</li>
          </ul>
          <button class="plan-btn premium-btn" onclick="window.location.href='checkout.html'">申请定制方案</button>
        </div>
      </div>
    </div>
  </section>"""
content = re.sub(r'<section class="section plans-section".*?</section>', plans_str, content, flags=re.DOTALL)

reassurance_str = """
  <section class="section dark-section" style="border-top:1px solid rgba(255,255,255,0.1); padding: 4rem 1rem; text-align:center;">
    <div class="container">
      <h2 class="section-title light">准备好开始打造你的个人IP了吗？</h2>
      <p style="color: #a1a1aa; font-size: 1.1rem; margin-bottom: 2.5rem; max-width:600px; margin-left:auto; margin-right:auto;">
        如果你还不确定自己目前处于什么阶段、适合哪一档服务，建议先从“IP定位诊断”开始，或者直接联络顾问咨询。
      </p>
      <div style="display:flex; justify-content:center; gap:1.5rem; flex-wrap:wrap;">
        <button class="btn-primary-lg" onclick="window.location.href='checkout.html'">先做IP诊断</button>
        <button class="nav-cta" onclick="window.location.href='mailto:hello@maneebrides.shop'">直接联系顾问</button>
      </div>
    </div>
  </section>
"""
content = content.replace('<!-- ══ FOOTER ══ -->', reassurance_str + '\n  <!-- ══ FOOTER ══ -->')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Success')
