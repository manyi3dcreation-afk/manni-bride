import re

css_path = 'style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Replace :root
root_new = '''
:root {
  --bg:          #fdf8f5;
  --bg-2:        #f8ece4;
  --bg-card:     #ffffff;
  --bg-card-h:   #ffffff;

  --gold-1:      #c9896a;
  --gold-2:      #d4af37;
  --rose:        #f4c2a8;
  --pur-1:       #3d1a2e;
  --pur-2:       #5c2b46;
  --cyan:        #d4af37;

  --grad-main:   linear-gradient(135deg, #c9896a 0%, #e8b89a 50%, #f4c2a8 100%);
  --grad-pur:    linear-gradient(135deg, #3d1a2e 0%, #5c2b46 100%);
  --grad-gold:   linear-gradient(135deg, #d4af37 0%, #f0d060 100%);
  --grad-cyan:   linear-gradient(135deg, #f4c2a8, #fae8d8);

  --text:        #1a0e14;
  --text-2:      #6b4c5e;
  --text-3:      #8a6d7d;

  --border:      rgba(201,137,106,0.2);
  --border-h:    rgba(201,137,106,0.4);

  --font-serif:  'Noto Serif SC', serif;
  --font-sans:   'Noto Sans SC', sans-serif;
  --font-disp:   'Playfair Display', serif;

  --r:  12px;
  --r2: 24px;
  --shadow: 0 20px 60px rgba(61,26,46,0.12);
}
'''
css = re.sub(r':root\s*\{.*?\n\}', root_new.strip(), css, flags=re.DOTALL)

# 2. General Hardcoded Backgrounds & Texts
css = css.replace('background: rgba(6,6,13,.8);', 'background: rgba(253, 248, 245, 0.92);')
css = css.replace('background: #040408;', 'background: var(--pur-1);')
css = css.replace('background: rgba(13,13,26,.9);', 'background: rgba(255,255,255,.9);')
css = css.replace('background: rgba(4,4,8,.88);', 'background: rgba(61,26,46,.88);')

css = css.replace('linear-gradient(160deg, #13132a 0%, #0d0d1e 60%, #0b0b18 100%)', 'linear-gradient(160deg, #ffffff 0%, #fdf8f5 100%)')
css = css.replace('rgba(255,255,255,.04)', 'rgba(201,137,106,.04)')
css = css.replace('rgba(255,255,255,.06)', 'rgba(201,137,106,.06)')
css = css.replace('rgba(255,255,255,.08)', 'rgba(201,137,106,.08)')
css = css.replace('rgba(255,255,255,.1)', 'rgba(201,137,106,.1)')
css = css.replace('rgba(255,255,255,.12)', 'rgba(201,137,106,.12)')
css = css.replace('rgba(255,255,255,.15)', 'rgba(201,137,106,.15)')

# Specific color fixes for text that shouldn't be white on white bg
css = re.sub(r'color:\s*#fff;', 'color: var(--text);', css)

# Revert button text and .dark-section text back to white
css = css.replace('.btn-primary-lg {\n  background: var(--grad-main);\n  color: var(--text);', '.btn-primary-lg {\n  background: var(--grad-main);\n  color: #fff;')
css = css.replace('.nav-cta {\n  background: var(--grad-main); color: var(--text);', '.nav-cta {\n  background: var(--grad-main); color: #fff;')
css = css.replace('.section-title.light { color: var(--text); }', '.section-title.light { color: #fff; }')
css = css.replace('.section-desc.light { color: rgba(255,255,255,.65); }', '.section-desc.light { color: rgba(255,255,255,.8); }')

# Fix dark sections to be plum
css = css.replace('var(--bg-2)', 'var(--grad-pur)')

# Fix modal text since we inverted bg
css = css.replace('.modal-header h3 {\\n  font-family', '.modal-header h3 {\\n  color: var(--text); font-family')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print('style.css patched.')
