import codecs, re

# Read current index.html to extract Header & Footer
with codecs.open('index.html', 'r', 'utf-8') as f:
    base_html = f.read()

header_match = re.search(r'(<!DOCTYPE html>.*?<!-- Hero Section -->)', base_html, re.DOTALL)
footer_match = re.search(r'(  <!-- Footer -->.*</html>)', base_html, re.DOTALL)

if not header_match or not footer_match:
    print("Error extracting header/footer.")
    exit(1)

# we don't want the <!-- Hero Section --> string in the header, we slice it out by replacing it with empty space
header = header_match.group(1).replace('<!-- Hero Section -->', '')
footer = footer_match.group(1)

# Update nav links in header to point to new pages
header = header.replace('href="#plans"', 'href="services.html"')
header = header.replace('href="#services"', 'href="services.html"')
header = header.replace('href="#faq-contact"', 'href="faq.html"')
header = header.replace('href="#ips"', 'href="faq.html"')
header = header.replace('href="#cases"', 'href="faq.html"')
header = header.replace('成功案例', '常见问题')
header = header.replace('关于我们', '首页')
header = header.replace('href="#about"', 'href="index.html"')
header = header.replace('href="#what-we-do"', 'href="index.html"')

footer = footer.replace('href="#services"', 'href="services.html"')
footer = footer.replace('href="#cases"', 'href="faq.html"')
footer = footer.replace('href="#plans"', 'href="services.html"')
footer = footer.replace('成功案例', '常见问题')

inquiry_modal_html = """
  <!-- ══ INQUIRY AUX MODAL ══ -->
  <div class="modal-overlay" id="inquiryOverlay">
    <div class="modal-box" id="inquiryModal" style="max-width:450px;">
      <button class="modal-close" onclick="closeInquiryModal()">✕</button>
      <div class="modal-header" style="text-align:center;">
        <h3 style="color:#fff;font-size:1.4rem;font-weight:400;margin-bottom:0.5rem">备用咨询表单</h3>
        <p style="color:var(--text-2);font-size:0.95rem;line-height:1.6">由于目前是高客单高定制化服务，为了保证质量，我们强烈建议您优先添加主理人微信进行1对1沟通。<br/><br/>若暂不方便即时添加，您可在此留下联系方式，主理人将主动与您建联。</p>
      </div>
      <div class="partner-form" style="display:flex;flex-direction:column;gap:1.2rem;margin-top:2rem;">
        <input type="text" placeholder="您的称呼（如：王女士）" class="modal-input" id="iName" />
        <input type="text" placeholder="您的微信号 / 手机号（必填）" class="modal-input" id="iContact" />
        <textarea placeholder="请简述您的核心需求或目前遇到的瓶颈..." class="modal-input" id="iDesc" rows="3" style="resize:none;font-family:inherit;"></textarea>
        <button class="btn-primary" style="width:100%; padding:1rem; border-radius:8px; margin-top:0.5rem; border:none; cursor:pointer;" onclick="submitInquiry()">提交留言</button>
      </div>
    </div>
  </div>
"""

if "inquiryOverlay" not in footer:
    footer = footer.replace('<!-- Floating WeChat CTA -->', inquiry_modal_html + '\n  <!-- Floating WeChat CTA -->')
footer = footer.replace('openUploadModal()', 'openInquiryModal()')
footer = footer.replace('<span class="wechat-float-label">立即定制</span>', '<span class="wechat-float-label">留言咨询</span>')

# ================= SERVICE FILE =================
services_main = """
  <!-- Main Content wrapped properly -->
  <main style="padding-top: 120px; min-height: 80vh;">
    <section class="services section" style="padding: 4rem 0;">
      <div class="container" style="max-width: 900px;">
        <div class="section-header" style="text-align: center; margin-bottom: 5rem;">
          <h1 style="font-size: 3rem; font-weight: 300; margin-bottom: 1rem;"><span class="gradient-text">标准服务体系</span></h1>
          <p style="color: var(--text-2); font-size: 1.1rem; font-weight: 300;">适合按阶段购买服务，快速启动个人IP，建立专业视觉模型。</p>
        </div>

        <!-- 199/299 Tier -->
        <div class="service-detail-card" style="margin-bottom: 3rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 3rem; transition: border-color 0.3s ease;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
            <div>
              <h2 style="font-size: 2rem; font-weight: 400; margin-bottom: 0.5rem; color: #fff;">IP定位诊断</h2>
              <p style="color: var(--text-2); font-size: 1rem; font-weight: 300;">适合刚开始做个人IP、还不清楚自己该怎么定位的人。</p>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 2.5rem; color: var(--text); font-weight: 300; font-family: 'Playfair Display', serif;"><span style="font-size:1rem">¥</span> 199 <span style="font-size:1rem; color:var(--text-3)">/ 299</span></div>
            </div>
          </div>
          <div style="margin-bottom: 2.5rem; margin-top: 2rem;">
            <h4 style="color: #fff; font-weight: 400; font-size: 1.1rem; margin-bottom: 1rem;">你将获得：</h4>
            <ul style="color: var(--text-2); font-weight: 300; line-height: 2; list-style-type: disc; padding-left: 1.5rem;">
              <li>一次基础定位分析</li>
              <li>一个更适合你的平台方向建议</li>
              <li>一份初步人设方向建议</li>
              <li>5 个起步内容方向</li>
              <li>一条账号简介优化建议</li>
            </ul>
          </div>
          <a href="javascript:alert('【Stripe 支付跳转】\\n\\n低客单直购通道：此按钮将直接拉起 Stripe 收银台。');" class="btn-secondary" style="border: 1px solid rgba(255,255,255,0.2); background: transparent; color: #fff; padding: 1rem 3rem; border-radius: 8px;">直购诊断卡 (Stripe)</a>
        </div>

        <!-- 698 Tier -->
        <div class="service-detail-card" style="margin-bottom: 3rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 3rem; transition: border-color 0.3s ease;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
            <div>
              <h2 style="font-size: 2rem; font-weight: 400; margin-bottom: 0.5rem; color: #fff;">单平台基础起号服务</h2>
              <p style="color: var(--text-2); font-size: 1rem; font-weight: 300;">适合预算有限、希望先从一个平台开始启动的人。</p>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 2.5rem; color: var(--text); font-weight: 300; font-family: 'Playfair Display', serif;"><span style="font-size:1rem">¥</span> 698 <span style="font-size:1rem; color:var(--text-3)">/ 月</span></div>
            </div>
          </div>
          <div style="margin-bottom: 2.5rem; margin-top: 2rem;">
            <h4 style="color: #fff; font-weight: 400; font-size: 1.1rem; margin-bottom: 1rem;">你将获得：</h4>
            <ul style="color: var(--text-2); font-weight: 300; line-height: 2; list-style-type: disc; padding-left: 1.5rem;">
              <li>单平台基础定位</li>
              <li>基础人设整理</li>
              <li>内容方向建议</li>
              <li>起号节奏建议</li>
              <li>轻量持续优化建议</li>
            </ul>
          </div>
          <a href="checkout.html?tier=698" class="btn-primary" style="background: rgba(255,255,255,0.1); color: #fff; padding: 1rem 3rem; border-radius: 8px;">咨询 698 方案</a>
        </div>

        <!-- 1280 Tier -->
        <div class="service-detail-card highlight" style="margin-bottom: 3rem; background: linear-gradient(180deg, rgba(255,107,157,0.05), rgba(10,10,15,0.5)); border: 1px solid var(--primary); box-shadow: 0 0 30px rgba(255,107,157,0.1); border-radius: 12px; padding: 3rem; position: relative;">
          <div style="position: absolute; top:0; left:50%; transform:translateX(-50%); background: var(--primary); color:#fff; font-size:0.8rem; padding: 0.3rem 1.5rem; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">核心推荐</div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
            <div>
              <h2 style="font-size: 2rem; font-weight: 400; margin-bottom: 0.5rem; color: #fff;">单平台数字分身强化版</h2>
              <p style="color: var(--text-2); font-size: 1rem; font-weight: 300;">适合想在小红书或抖音建立更清晰数字分身形象的人。</p>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 2.5rem; color: var(--primary); font-weight: 300; font-family: 'Playfair Display', serif;"><span style="font-size:1rem">¥</span> 1,280 <span style="font-size:1rem; color:var(--text-3)">/ 月</span></div>
            </div>
          </div>
          <div style="margin-bottom: 2.5rem; margin-top: 2rem;">
            <h4 style="color: #fff; font-weight: 400; font-size: 1.1rem; margin-bottom: 1rem;">你将获得：</h4>
            <ul style="color: var(--text-2); font-weight: 300; line-height: 2; list-style-type: disc; padding-left: 1.5rem;">
              <li>专属数字分身定位</li>
              <li>单平台风格强化</li>
              <li>内容主题与表达方向</li>
              <li>形象感持续迭代建议</li>
              <li>单平台深度运营辅助</li>
            </ul>
          </div>
          <a href="checkout.html?tier=1280" class="btn-primary" style="padding: 1rem 3rem; border-radius: 8px;">咨询 1280 方案</a>
        </div>

        <!-- 4980 Tier -->
        <div class="service-detail-card" style="margin-bottom: 4rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(201,137,106,0.3); border-radius: 12px; padding: 3rem; transition: border-color 0.3s ease;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
            <div>
              <h2 style="font-size: 2rem; font-weight: 400; margin-bottom: 0.5rem; color: #c9896a;">全平台超级IP定制版</h2>
              <p style="color: var(--text-2); font-size: 1rem; font-weight: 300;">适合想布局更强个人品牌、多平台表达与高价值商业形象的人。</p>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 2.5rem; color: #c9896a; font-weight: 300; font-family: 'Playfair Display', serif;"><span style="font-size:1rem">¥</span> 4,980 <span style="font-size:1rem; color:var(--text-3)">/ 月</span></div>
            </div>
          </div>
          <div style="margin-bottom: 2.5rem; margin-top: 2rem;">
            <h4 style="color: #fff; font-weight: 400; font-size: 1.1rem; margin-bottom: 1rem;">你将获得：</h4>
            <ul style="color: var(--text-2); font-weight: 300; line-height: 2; list-style-type: disc; padding-left: 1.5rem;">
              <li>全案级IP定位</li>
              <li>数字分身形象体系</li>
              <li>多平台方向规划</li>
              <li>持续内容与形象迭代</li>
              <li>高价值个人IP定制支持</li>
            </ul>
          </div>
          <a href="checkout.html?tier=4980" class="btn-secondary" style="border: 1px solid #c9896a; color: #c9896a; padding: 1rem 3rem; border-radius: 8px; background: transparent;">申请定制方案</a>
        </div>

        <!-- ══ JOINT INCUBATION SECTION ══ -->
        <div style="margin-top: 8rem; margin-bottom: 5rem; text-align: center;">
          <h2 style="font-size: 2.5rem; font-weight: 300; margin-bottom: 1.5rem;"><span class="gradient-text">联合孵化计划</span></h2>
          <p style="color: var(--text-2); font-size: 1.1rem; font-weight: 300; max-width: 600px; margin: 0 auto;">深度共建 · 长期合作 · 共享成长收益</p>
        </div>

        <div class="service-detail-card" style="background: linear-gradient(135deg, rgba(201,137,106,0.1), rgba(255,107,157,0.05)); border: 1px solid rgba(201,137,106,0.4); border-radius: 12px; padding: 4rem; text-align: center; position: relative; overflow: hidden;">
          <div style="position: absolute; top:0; right:0; padding: 1rem; color: rgba(201,137,106,0.2); font-size: 4rem; font-weight: 700; line-height: 1;">PARTNER</div>
          <div style="max-width: 600px; margin: 0 auto;">
            <h3 style="color: #c9896a; font-size: 1.8rem; font-weight: 400; margin-bottom: 1.5rem;">长期 IP 战略合伙人</h3>
            <p style="color: var(--text-2); font-size: 1.05rem; line-height: 1.8; font-weight: 300; margin-bottom: 2.5rem;">
              联合孵化方案专为寻求**深度战略合作**的用户设计。与标准服务不同，孵化模型下曼妮新娘将投入更核心的资源与您共建 IP 矩阵，并根据长期收益共享成长价值。<br/><br/>
              该计划旨在筛选志同道合、具备长期主义视野的合作伙伴。<strong style="color:#fff;">本计划目前仅通过主理人深度评估后进入。</strong>
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; margin-bottom: 3rem;">
              <span style="background: rgba(255,255,255,0.05); padding: 0.5rem 1.2rem; border-radius: 4px; font-size: 0.9rem; color: #c9896a;">长期共建</span>
              <span style="background: rgba(255,255,255,0.05); padding: 0.5rem 1.2rem; border-radius: 4px; font-size: 0.9rem; color: #c9896a;">利益共享</span>
              <span style="background: rgba(255,255,255,0.05); padding: 0.5rem 1.2rem; border-radius: 4px; font-size: 0.9rem; color: #c9896a;">申请制进入</span>
            </div>
            <a href="checkout.html?type=incubation" class="btn-primary" style="background: #c9896a; border: none; color: #fff; padding: 1.2rem 4rem; border-radius: 8px; font-size: 1.1rem;">立即申请联合孵化</a>
          </div>
        </div>

        <!-- 推荐路径区 -->
        <div class="path-recommendation" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 3rem; border-radius: 12px;">
          <h3 style="color: #fff; font-size: 1.5rem; font-weight: 300; margin-bottom: 2rem; text-align: center;">轻量推荐路径</h3>
          <ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 1.2rem; color: var(--text-2); font-weight: 300;">
            <li style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 1rem;">
              <span>不确定方向</span>
              <a href="javascript:alert('【Stripe 支付跳转】\\n\\n低客单直购通道：此按钮将直接拉起 Stripe 收银台。');" style="color: #fff; opacity: 0.8; text-decoration: none;">&rarr; 直购诊断卡</a>
            </li>
            <li style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 1rem;">
              <span>想先从一个平台起步</span>
              <a href="checkout.html?tier=698" style="color: #fff; opacity: 0.8; text-decoration: none;">&rarr; 咨询 ¥698</a>
            </li>
            <li style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 1rem;">
              <span>想强化单平台数字分身</span>
              <a href="checkout.html?tier=1280" style="color: var(--primary); text-decoration: none;">&rarr; 咨询 ¥1,280</a>
            </li>
            <li style="display: flex; justify-content: space-between; align-items: center;">
              <span>想做更完整的高价值全平台IP</span>
              <a href="checkout.html?tier=4980" style="color: #c9896a; text-decoration: none;">&rarr; 咨询 ¥4,980</a>
            </li>
          </ul>
        </div>

      </div>
      <style>.service-detail-card:hover:not(.highlight) { border-color: rgba(255,255,255,0.3) !important; }</style>
    </section>
  </main>
"""

with codecs.open('services.html', 'w', 'utf-8') as f:
    f.write(header + services_main + footer)

# ================= CHECKOUT FILE =================
checkout_main = """
  <main style="padding-top: 15vh; min-height: 80vh;">
    <section class="checkout section" style="padding: 2rem 0;">
      <div class="container" style="max-width: 800px; text-align: center;">
        
        <div class="section-tag light" style="margin-bottom: 1.5rem; letter-spacing: 3px;">开始行动</div>
        <h1 style="font-size: 3rem; font-weight: 300; color:#fff; margin-bottom: 1.5rem;">开始打造你的<span class="gradient-text">超级个人IP</span></h1>
        
        <p style="color: var(--text-2); font-size: 1.1rem; font-weight: 300; max-width: 600px; margin: 0 auto 1.5rem auto; line-height: 1.8;">
          根据你现在的阶段和目标，选择适合你的启动路径。
        </p>
        
        <div style="display: inline-block; background: rgba(255,107,157,0.08); border: 1px solid rgba(255,107,157,0.2); color: #fff; padding: 0.8rem 1.8rem; border-radius: 40px; font-size: 0.95rem; margin-bottom: 4rem; letter-spacing: 0.5px;">
          💡 如果你还不确定适合哪一档，建议 <a href="#wechat-consult" onclick="document.getElementById('wechat-qr').scrollIntoView({behavior:'smooth'});" style="color:var(--primary); text-decoration:underline; font-weight:400;">先向我们咨询</a>，或直接从 <strong>IP定位诊断</strong> 开始。
        </div>

        <div style="display: flex; flex-direction: column; gap: 2rem; text-align: left;">
          
          <!-- Path 1 -->
          <a href="javascript:alert('【Stripe 支付跳转】\\n\\n因为是低客单标品，此入口已绕过人工咨询，直接通过 Stripe 进行支付转化，缩短决策链路。');" style="text-decoration: none;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); padding: 2.5rem; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; transition: background 0.3s ease;">
              <div>
                <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem; font-weight: 400; letter-spacing: 1px; margin-bottom: 0.8rem;">「 状态：不确定方向 」</p>
                <h3 style="color: #fff; font-size: 1.5rem; font-weight: 400; margin-bottom: 0.5rem;">先做 IP 定位诊断 <span style="font-size: 1rem; color:var(--text-3); font-weight:300;">(¥199 / ¥299)</span></h3>
                <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem;">无需等待咨询，点击前往 Stripe 安全支付，获取专属视觉与方向诊断。</p>
              </div>
              <div style="color: var(--text-3); font-size: 1.5rem;">💳 购买</div>
            </div>
          </a>

          <!-- Path 3 -->
          <a href="#wechat-consult" onclick="document.getElementById('wechat-qr').scrollIntoView({behavior:'smooth'});" style="text-decoration: none;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); padding: 2.5rem; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
              <div>
                <p style="color: var(--text-3); font-size: 0.85rem; font-weight: 400; letter-spacing: 1px; margin-bottom: 0.8rem;">「 状态：有明确目标或希望购买标准套餐 」</p>
                <h3 style="color: #fff; font-size: 1.5rem; font-weight: 400; margin-bottom: 0.5rem;">咨询标准服务套餐 <span style="font-size: 1rem; color:var(--text-3); font-weight:300;">(¥698 - ¥4980)</span></h3>
                <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem;">咨询月度起号、分身强化及超级 IP 定制。通过微信确认需求后再获取链接。</p>
              </div>
              <div style="color: var(--text-3); font-size: 1.5rem;">&rarr; 咨询</div>
            </div>
          </a>

          <!-- Path 4 -->
          <a href="#wechat-consult" onclick="document.getElementById('wechat-qr').scrollIntoView({behavior:'smooth'});" style="text-decoration: none;">
            <div style="background: linear-gradient(90deg, rgba(201,137,106,0.1), transparent); border: 1px solid #c9896a; padding: 2.5rem; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 20px rgba(201,137,106,0.05);">
              <div>
                <p style="color: #c9896a; font-size: 0.85rem; font-weight: 400; letter-spacing: 1px; margin-bottom: 0.8rem;">「 状态：想做更完整的高价值 IP 共建与孵化 」</p>
                <h3 style="color: #c9896a; font-size: 1.5rem; font-weight: 400; margin-bottom: 0.5rem;">申请联合孵化计划 <span style="font-size: 1rem; color:var(--text-3); font-weight:300;">(申请制)</span></h3>
                <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem;">由主理人亲自跟进的深度合伙陪跑。添加微信提交资质申请并进行项目评估。</p>
              </div>
              <div style="color: #c9896a; font-size: 1.5rem;">&rarr; 申请</div>
            </div>
          </a>

        </div>

        <!-- 付款后流程区块 -->
        <div style="margin-top: 5rem; padding: 2.5rem; background: rgba(255,255,255,0.015); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-align: left;">
          <h4 style="color: #fff; font-size: 1.15rem; font-weight: 400; margin-bottom: 1.5rem;">🚀 提交/付款后会发生什么？</h4>
          <div style="display: flex; flex-direction: column; gap: 1.2rem; color: var(--text-2); font-weight: 300; font-size: 0.95rem;">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
              <span style="color: var(--primary); font-weight: 400; margin-top:2px;">01.</span> 
              <span>确认订单并进入对应服务路径</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
              <span style="color: var(--primary); font-weight: 400; margin-top:2px;">02.</span> 
              <span>确认您的目标平台、账号方向与基础资料</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
              <span style="color: var(--primary); font-weight: 400; margin-top:2px;">03.</span> 
              <span>进行首轮 IP 定位诊断与内容启动</span>
            </div>
          </div>
        </div>

        <!-- 统一承接引流 -->
        <div id="wechat-qr" style="margin-top: 6rem; padding-top: 4rem; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">
          <h3 style="color: #fff; font-size: 1.4rem; font-weight: 300; margin-bottom: 1rem;">主理人微信对接</h3>
          <p style="color: var(--text-2); font-size: 1rem; font-weight: 300; margin-bottom: 2rem;">无论你是准备好购买，还是需要协助判断方案，都可以毫无压力地添加微信。<br/>付款及后续服务合同均将在安全环境下对接。</p>
          <div style="width: 200px; height: 200px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); margin: 0 auto; display: flex; align-items: center; justify-content: center; border-radius: 12px; margin-bottom: 1rem;">
             <span style="color: #fff; opacity:0.3; font-size:0.9rem">[ 扫码添加微信 ]</span>
          </div>
          <p style="color: #fff; font-size: 1.2rem; font-weight: 400; letter-spacing: 1px;">WeChat ID: <span style="color: var(--primary);">mannibride888</span></p>

          <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px dashed rgba(255,255,255,0.05);">
            <p style="color: var(--text-3); font-size: 0.95rem; margin-bottom: 1rem;">不方便当下加微信？或者手机暂无法扫码？</p>
            <button class="btn-secondary" onclick="openInquiryModal()" style="background:transparent; border:1px solid rgba(255,255,255,0.2); color:#fff; padding:0.6rem 2rem; border-radius:40px; font-size:0.9rem;">
              填写备用留言单，由我们联系您 &rarr;
            </button>
          </div>
        </div>

      </div>
    </section>
  </main>
"""

with codecs.open('checkout.html', 'w', 'utf-8') as f:
    f.write(header + checkout_main + footer)

# ================= FAQ FILE =================
faq_main = """
  <main style="padding-top: 15vh; min-height: 80vh;">
    <section class="faq section" style="padding: 2rem 0;">
      <div class="container" style="max-width: 800px;">
        <div class="section-header" style="text-align: center; margin-bottom: 5rem;">
          <h1 style="font-size: 3rem; font-weight: 300; margin-bottom: 1rem;"><span class="gradient-text">常见问题</span></h1>
          <p style="color: var(--text-2); font-size: 1.1rem; font-weight: 300;">在正式行动前，我们希望坦诚地解答你可能存在的疑虑。</p>
        </div>

        <div class="faq-list" style="display: flex; flex-direction: column; gap: 2rem;">
          
          <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 2rem;">
            <h3 style="color: #fff; font-size: 1.2rem; font-weight: 400; margin-bottom: 1rem;">1. 曼妮新娘到底是做什么的？</h3>
            <p style="color: var(--text-2); font-weight: 300; font-size: 1rem; line-height: 1.8;">曼妮新娘主要帮助用户打造数字分身与超级个人IP，<br/>从定位、人设、形象、内容到平台运营，<br/>逐步建立更清晰的表达方式与更高价值的个人品牌呈现。</p>
          </div>

          <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 2rem;">
            <h3 style="color: #fff; font-size: 1.2rem; font-weight: 400; margin-bottom: 1rem;">2. 这和普通代运营有什么区别？</h3>
            <p style="color: var(--text-2); font-weight: 300; font-size: 1rem; line-height: 1.8;">普通代运营更偏向帮你发内容，<br/>曼妮新娘更强调从人设、形象、内容方向与长期表达体系出发，<br/>帮助你建立真正属于自己的个人IP与数字分身。</p>
          </div>

          <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 2rem;">
            <h3 style="color: #fff; font-size: 1.2rem; font-weight: 400; margin-bottom: 1rem;">3. 我适合从哪一档开始？</h3>
            <p style="color: var(--text-2); font-weight: 300; font-size: 1rem; line-height: 1.8;">如果你还没有想清楚方向，建议先从 IP定位诊断开始。<br/>如果你已经确定想做某个平台，可以根据预算和目标选择 698 或 1280。<br/>如果你希望打造更完整的高价值个人品牌，可以申请 4980 定制方案。</p>
          </div>

          <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 2rem;">
            <h3 style="color: #fff; font-size: 1.2rem; font-weight: 400; margin-bottom: 1rem;">4. 账号归谁？</h3>
            <p style="color: var(--text-2); font-weight: 300; font-size: 1rem; line-height: 1.8;">账号归客户本人所有。<br/>曼妮新娘提供的是定位、形象、内容与运营服务，<br/>不是占有客户账号资产。</p>
          </div>

          <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 2rem;">
            <h3 style="color: #fff; font-size: 1.2rem; font-weight: 400; margin-bottom: 1rem;">5. 什么是联合孵化方案？</h3>
            <p style="color: var(--text-2); font-weight: 300; font-size: 1rem; line-height: 1.8;">联合孵化适合高信任、长期合作型用户。与标准服务不同，孵化方案更强调“长期共建”与“共享成长收益”。该计划采取申请制，需要经过主理人对项目潜力与合作意向的深度评估后方可进入。</p>
          </div>

          <div style="padding-top: 2rem; margin-top: 2rem; border-top: 1px dashed rgba(255,255,255,0.1);">
            <h3 style="color: #c9896a; font-size: 1.1rem; font-weight: 300; margin-bottom: 2rem; letter-spacing: 2px;">更多常见问题</h3>
            
            <div style="margin-bottom: 2rem;">
              <h4 style="color: #fff; font-size: 1.05rem; font-weight: 400; margin-bottom: 0.5rem;">5. 需要我提供哪些资料？</h4>
              <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem; line-height: 1.6;">合作开始后我们会请您填写一份专属档案表。<br/>如果您有原生的照片或视频素材，我们将基于此进行包装与视觉加工。</p>
            </div>

            <div style="margin-bottom: 2rem;">
              <h4 style="color: #fff; font-size: 1.05rem; font-weight: 400; margin-bottom: 0.5rem;">6. 付款后多久开始？</h4>
              <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem; line-height: 1.6;">对接完成后 24-48 小时内建群。<br/>我们将为您进行首次方向诊断分析，并确认后续的服务排期表。</p>
            </div>

            <div style="margin-bottom: 2rem;">
              <h4 style="color: #fff; font-size: 1.05rem; font-weight: 400; margin-bottom: 0.5rem;">7. 是否保证涨粉或变现？</h4>
              <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem; line-height: 1.6;">真正的个人IP不仅是虚假数据的流量游戏，更是建立高维度的信任壁垒。<br/>我们保证您的视觉与内容呈现会远超同行，极大地提升转化可信度与商业溢价。</p>
            </div>

            <div style="margin-bottom: 1rem;">
              <h4 style="color: #fff; font-size: 1.05rem; font-weight: 400; margin-bottom: 0.5rem;">8. 如果我还没想清楚方向怎么办？</h4>
              <p style="color: var(--text-2); font-weight: 300; font-size: 0.95rem; line-height: 1.6;">这非常正常。建议您先进行轻量的「IP定位诊断」，<br/>借用专业的外脑视角，帮您梳理出最匹配自身优势的变现赛道。</p>
            </div>
          </div>

        </div>
        
        <div style="text-align: center; margin-top: 5rem;">
          <a href="checkout.html" class="btn-primary" style="padding: 1rem 3rem; border-radius: 8px;">准备好了，开始行动</a>
        </div>
      </div>
    </section>
  </main>
"""

with codecs.open('faq.html', 'w', 'utf-8') as f:
    f.write(header + faq_main + footer)

# ================= UPDATE INDEX.HTML =================
with codecs.open('index.html', 'r', 'utf-8') as f:
    idx_html = f.read()

# 1. Update text in Header
idx_html = idx_html.replace('href="#plans"', 'href="services.html"')
idx_html = idx_html.replace('href="#services"', 'href="services.html"')
idx_html = idx_html.replace('href="#faq-contact"', 'href="faq.html"')
idx_html = idx_html.replace('href="#cases"', 'href="faq.html"')
idx_html = idx_html.replace('成功案例', '常见问题')
idx_html = idx_html.replace('href="#ips"', 'href="faq.html"')

# 2. Hero Section Update
idx_html = re.sub(
    r'<span class="title-line-1".*?</span>',
    '<span class="title-line-1" style="font-weight: 300; font-size: 2.8rem; display:block;">为你打造 7×24 持续进化的</span>',
    idx_html, count=1
)
idx_html = re.sub(
    r'<span class="title-line-2 gradient-text".*?</span>',
    '<span class="title-line-2 gradient-text" style="font-size: 4.5rem; line-height: 1.2;">超级个人IP</span>',
    idx_html, count=1
)
idx_html = re.sub(
    r'<p class="hero-desc".*?</p>',
    '<p class="hero-desc" style="font-size: 1.2rem; line-height: 1.8; max-width: 650px; margin: 0 auto 3rem auto; color: var(--text-2); font-weight: 300;">从人设、形象、内容到平台运营，曼妮新娘帮助你打造数字分身与超级个人IP，<br/>让你被看见、被记住，并逐步走向更高价值的成交。</p>',
    idx_html, flags=re.DOTALL
)
idx_html = re.sub(r'<a href="[^"]*?" class="btn-primary" id="hero-start-btn"[^>]*>.*?</a>', '<a href="services.html" class="btn-primary" id="hero-start-btn" style="padding: 1.2rem 3rem; font-size: 1.1rem; border-radius: 40px;">查看服务套餐</a>', idx_html)
idx_html = re.sub(r'<a href="[^"]*?" class="btn-secondary" id="hero-learn-btn"[^>]*>.*?</a>', '<a href="checkout.html?type=diagnostic" class="btn-secondary" id="hero-learn-btn" style="padding: 1.2rem 3rem; font-size: 1.1rem; border-radius: 40px; background: rgba(255,255,255,0.05); color: #fff; border: 1px solid rgba(255,255,255,0.2);">先做IP诊断</a>', idx_html)

# 3. What We Do - Simplify into elegant paragraph
what_we_do_new = """
  <!-- ══ V1: WHAT WE DO ══ -->
  <section class="what-we-do section dark-section" id="what-we-do" style="padding: 8rem 0;">
    <div class="container" style="max-width: 700px; text-align: center;">
      <h2 style="font-size: 1.8rem; font-weight: 300; color:#fff; line-height: 2; margin-bottom: 2rem;">
        “我们不只帮你发内容，<br/>
        我们帮助你打造一个能<span class="gradient-text">持续表达、持续吸引、持续进化</span>的超级个人IP。”
      </h2>
      <p style="color: var(--text-2); font-size: 1.1rem; line-height: 2; font-weight: 300; margin-bottom: 0;">
        从账号定位，到数字分身形象；<br/>
        从内容方向，到平台运营；<br/>
        从前端曝光，到咨询承接；<br/>
        曼妮新娘为你建立一套真正能走向商业价值的 <strong style="color:#fff; font-weight:400;">个人IP服务路径</strong>。
      </p>
    </div>
  </section>
"""
idx_html = re.sub(r'<!-- ══ V1: WHAT WE DO ══ -->.*?<!-- ══ V1: WHO IS IT FOR ══ -->', what_we_do_new + '\n\n  <!-- ══ V1: WHO IS IT FOR ══ -->', idx_html, flags=re.DOTALL)

# 3.5 Cooperation Models - Explicit choice
cooperation_models_new = """
  <!-- ══ V1: COOPERATION MODELS ══ -->
  <section class="cooperation-models section" id="cooperation" style="padding: 6rem 0; background: rgba(255,255,255,0.01);">
    <div class="container" style="max-width: 900px;">
      <div class="section-tag" style="text-align: center; letter-spacing: 3px; margin-bottom: 2rem;">合作模式</div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 3rem; border-radius: 12px;">
          <h3 style="color: #fff; font-size: 1.4rem; font-weight: 400; margin-bottom: 1rem;">标准服务体系</h3>
          <p style="color: var(--text-2); font-size: 0.95rem; line-height: 1.8; font-weight: 300; margin-bottom: 2rem;">
            适合按阶段购买服务，快速启动个人 IP。我们提供从定位到形象产出的专业全流程支持。
          </p>
          <a href="services.html" style="color: var(--primary); font-size: 0.95rem; text-decoration: none;">了解详情 &rarr;</a>
        </div>
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(201,137,106,0.3); padding: 3rem; border-radius: 12px;">
          <h3 style="color: #c9896a; font-size: 1.4rem; font-weight: 400; margin-bottom: 1rem;">联合孵化计划</h3>
          <p style="color: var(--text-2); font-size: 0.95rem; line-height: 1.8; font-weight: 300; margin-bottom: 2rem;">
            适合寻求长期共建、共享成长收益的深度合作伙伴。申请制进入，深度资源注入。
          </p>
          <a href="services.html#joint-incubation" style="color: #c9896a; font-size: 0.95rem; text-decoration: none;">申请加入 &rarr;</a>
        </div>
      </div>
    </div>
  </section>
"""
# We will insert it just before WHO IS IT FOR. Since WHAT WE DO sub already handles it, we can sub again or just chain.
# To be safe, let's just insert it after the what_we_do_new sub.
idx_html = idx_html.replace('<!-- ══ V1: WHO IS IT FOR ══ -->', cooperation_models_new + '\n\n  <!-- ══ V1: WHO IS IT FOR ══ -->')

# 4. Target Audience - Lightweight list without heavy cards
audience_new = """
  <!-- ══ V1: WHO IS IT FOR ══ -->
  <section class="target-audience section" id="target-audience" style="padding: 3rem 0 6rem 0;">
    <div class="container" style="max-width: 600px;">
      <div class="section-tag" style="text-align: center; letter-spacing: 3px; margin-bottom: 2rem;">适合谁</div>
      <ul style="list-style: none; padding: 0; color: #fff; font-size: 1.1rem; font-weight: 300; line-height: 2.2;">
        <li style="display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom:1rem;">
          <span style="color: var(--primary); font-size: 1.2rem;">✓</span>
          <span>想打造个人IP但不知道从哪里开始的人</span>
        </li>
        <li style="display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom:1rem;">
          <span style="color: var(--primary); font-size: 1.2rem;">✓</span>
          <span>想拥有专属数字分身形象的人</span>
        </li>
        <li style="display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom:1rem;">
          <span style="color: var(--primary); font-size: 1.2rem;">✓</span>
          <span>想在小红书、抖音、TikTok、海外等平台发力的人</span>
        </li>
        <li style="display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem;">
          <span style="color: var(--primary); font-size: 1.2rem;">✓</span>
          <span>想把内容与商业价值连起来的人</span>
        </li>
      </ul>
    </div>
  </section>
"""
idx_html = re.sub(r'<!-- ══ V1: WHO IS IT FOR ══ -->.*?<!-- ══ V1: WORKFLOW ══ -->', audience_new + '\n\n  <!-- ══ V1: WORKFLOW ══ -->', idx_html, flags=re.DOTALL)


# 6. Pricing Preview updating links & text
idx_html = re.sub(r'<div class="pv1-card".*?IP定位诊断.*?</div>\s*</div>', 
  '<div class="pv1-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 2.5rem 2rem; text-align: center; display: flex; flex-direction: column;">'
  '<h3 style="font-size: 1.4rem; color: #fff; font-weight: 400; margin-bottom: 0.5rem;">IP定位诊断</h3>'
  '<p style="color: var(--text-2); font-size: 0.95rem; font-weight: 300; margin-bottom: 1.5rem; flex-grow: 1;">适合：准备起步阶段的人。</p>'
  '<div style="font-size: 1.8rem; color: var(--text); font-weight: 300; margin-bottom: 2rem; font-family: \'Playfair Display\', serif;">199 <span style="font-size:0.9rem; color:var(--text-3)">/ 299</span></div>'
  '<a href="checkout.html?tier=199" class="btn-secondary" style="border: 1px solid rgba(255,255,255,0.2); background: transparent; color: #fff; padding: 0.8rem; border-radius: 8px; font-size: 0.95rem;">先做诊断</a>'
  '</div>', idx_html, flags=re.DOTALL, count=1)

idx_html = re.sub(r'<div class="pv1-card".*?单平台基础起号.*?</div>\s*</div>', 
  '<div class="pv1-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 2.5rem 2rem; text-align: center; display: flex; flex-direction: column;">'
  '<h3 style="font-size: 1.4rem; color: #fff; font-weight: 400; margin-bottom: 0.5rem;">单平台基础起号</h3>'
  '<p style="color: var(--text-2); font-size: 0.95rem; font-weight: 300; margin-bottom: 1.5rem; flex-grow: 1;">适合：先从一个平台启动的人。</p>'
  '<div style="font-size: 1.8rem; color: var(--text); font-weight: 300; margin-bottom: 2rem; font-family: \'Playfair Display\', serif;">698 <span style="font-size:0.9rem; color:var(--text-3)">/ 月</span></div>'
  '<a href="checkout.html?tier=698" class="btn-primary" style="background: rgba(255,255,255,0.1); color: #fff; padding: 0.8rem; border-radius: 8px; font-size: 0.95rem;">咨询 698 方案</a>'
  '</div>', idx_html, flags=re.DOTALL, count=1)

idx_html = re.sub(r'<div class="pv1-card highlight".*?数字分身强化版.*?</div>\s*</div>', 
  '<div class="pv1-card highlight" style="position: relative; background: linear-gradient(180deg, rgba(255,107,157,0.05), rgba(10,10,15,0.5)); border: 1px solid var(--primary); border-radius: 12px; padding: 2.5rem 2rem; text-align: center; display: flex; flex-direction: column; box-shadow: 0 0 30px rgba(255,107,157,0.1);">'
  '<h3 style="font-size: 1.4rem; color: #fff; font-weight: 400; margin-bottom: 0.5rem;">数字分身强化版</h3>'
  '<p style="color: var(--text-2); font-size: 0.95rem; font-weight: 300; margin-bottom: 1.5rem; flex-grow: 1;">适合：想在小红书建立极高视觉壁垒的客户。</p>'
  '<div style="font-size: 1.8rem; color: var(--primary); font-weight: 300; margin-bottom: 2rem; font-family: \'Playfair Display\', serif;">1,280 <span style="font-size:0.9rem; color:var(--text-3)">/ 月</span></div>'
  '<a href="checkout.html?tier=1280" class="btn-primary" style="padding: 0.8rem; border-radius: 8px; font-size: 0.95rem;">咨询 1280 方案</a>'
  '</div>', idx_html, flags=re.DOTALL, count=1)

idx_html = re.sub(r'<div class="pv1-card".*?全.*超级IP定制.*?</div>\s*</div>', 
  '<div class="pv1-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(201,137,106,0.3); border-radius: 12px; padding: 2.5rem 2rem; text-align: center; display: flex; flex-direction: column;">'
  '<h3 style="font-size: 1.4rem; color: #c9896a; font-weight: 400; margin-bottom: 0.5rem;">全平台超级IP定制版</h3>'
  '<p style="color: var(--text-2); font-size: 0.95rem; font-weight: 300; margin-bottom: 1.5rem; flex-grow: 1;">适合：成熟玩家、高净值女性全网护航。</p>'
  '<div style="font-size: 1.8rem; color: #c9896a; font-weight: 300; margin-bottom: 2rem; font-family: \'Playfair Display\', serif;">4,980 <span style="font-size:0.9rem; color:var(--text-3)">/ 月</span></div>'
  '<a href="checkout.html?tier=4980" class="btn-secondary" style="border: 1px solid #c9896a; background: transparent; color: #c9896a; padding: 0.8rem; border-radius: 8px; font-size: 0.95rem;">申请定制方案</a>'
  '</div>', idx_html, flags=re.DOTALL, count=1)

# 7. FAQ Contact section in index.html, transform to extremely simple
footer_contact_new = """
  <!-- ══ V1: LIGHT CONVERSION ══ -->
  <section class="conversion-footer section" style="padding: 6rem 0; text-align: center;">
    <div class="container" style="max-width: 600px;">
      <p style="color: #fff; font-size: 1.1rem; line-height: 1.8; font-weight: 300; margin-bottom: 2rem;">
        如果你还不确定适合哪一档服务，建议先从 <strong>IP定位诊断</strong> 开始，<br/>或者直接咨询，我们会帮你判断适合的路径。
      </p>
      <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
        <a href="faq.html" class="btn-secondary" style="border: 1px solid rgba(255,255,255,0.3); background: transparent; color: #fff; padding: 0.8rem 2rem; border-radius: 8px;">常见疑虑解答 (FAQ)</a>
        <a href="checkout.html" class="btn-primary" style="padding: 0.8rem 2rem; border-radius: 8px;">直接咨询详情</a>
      </div>
    </div>
  </section>
"""
idx_html = re.sub(r'<!-- ══ V1: FAQ & CONTACT ══ -->.*?(?=<!-- App Download Section -->)', footer_contact_new + '\n\n  ', idx_html, flags=re.DOTALL)

# Inject inquiry modal and update floating button on index.html
if "inquiryOverlay" not in idx_html:
    idx_html = idx_html.replace('<!-- Floating WeChat CTA -->', inquiry_modal_html + '\n  <!-- Floating WeChat CTA -->')
idx_html = idx_html.replace('openUploadModal()', 'openInquiryModal()')
idx_html = idx_html.replace('<span class="wechat-float-label">立即定制</span>', '<span class="wechat-float-label">留言咨询</span>')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(idx_html)

print("v1 pages massively deployed!")
