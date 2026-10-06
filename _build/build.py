# -*- coding: utf-8 -*-
"""多ページ版サイトの生成スクリプト。
_build/source.html(旧1枚ページ)から各ブロックを切り出し、
トップ(index.html)+テーマ別8ページを書き出す。共通CSSは assets/style.css。
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(ROOT, '_build', 'source.html'), encoding='utf-8').read()

def take(start, end, s=src, include_start=True):
    i = s.index(start)
    j = s.index(end, i + len(start))
    return s[i if include_start else i + len(start):j]

css_old = take('<style>', '</style>', include_start=False)
about_inner = take('    <div class="about-flex fade">', '  </div>\n</section>')
research = take('    <div class="act-lead fade">', '    <h3 class="works-sub fade" style="margin-top:56px">そのほかの活動</h3>')
other_orgs = take('    <h3 class="works-sub fade" style="margin-top:56px">そのほかの活動</h3>', '    <h3 class="works-sub fade" style="margin-top:56px">コミュニティ活動</h3>')
community = take('    <div class="org-grid">\n      <div class="org fade">\n        <img class="org-img" src="assets/photos/ballooners-dao.webp"', '  </div>\n</section>')
awards = take('    <div class="award-list">', '  </div>\n</section>')
hobbies = take('    <div class="hobby-grid">', '  </div>\n</section>')
gallery = take('    <div class="gallery fade">', '  </div>\n</section>')
skills = take('    <div class="skill-grid">', '  </div>\n</section>')
works = take('    <h3 class="works-sub fade">ショート動画</h3>', '  </div>\n</section>')
services = take('    <div class="svc-grid">', '  </div>\n</section>')
contact_box = take('    <div class="contact-box fade">', '    <div class="hub">')
hub = take('    <div class="hub">', '  </div>\n</section>')

# 旧ギャラリーのfigureを抜き出して再利用
gal_figs = re.findall(r'      <figure>.*?</figure>', gallery)

# ---------------------------------------------------------------- CSS
css_new = css_old + '''
/* ================= multi-page additions ================= */
.nav ul{gap:16px}
.nav .logo{display:flex;align-items:center;gap:8px}
.nav .logo i{width:18px;height:18px;color:var(--accent)}
/* 写実的な草木フレーム */
.nature{position:absolute;pointer-events:none;z-index:1;filter:drop-shadow(0 10px 18px rgba(30,70,20,.18))}
.nature.tl{top:-70px;left:-90px;width:min(330px,44vw);transform-origin:10% 0;animation:sway 9s ease-in-out infinite}
.nature.br{right:-70px;bottom:-30px;width:min(420px,52vw);transform:rotate(200deg);transform-origin:90% 100%;animation:sway2 11s ease-in-out infinite}
.nature.tr{top:-30px;right:-50px;width:min(260px,40vw);transform:scaleX(-1) rotate(8deg);animation:sway3 10s ease-in-out infinite}
.nature.bl{left:-30px;bottom:-20px;width:min(200px,34vw);transform:rotate(-18deg)}
@keyframes sway{0%,100%{transform:rotate(0)}50%{transform:rotate(2.2deg)}}
@keyframes sway2{0%,100%{transform:rotate(200deg)}50%{transform:rotate(197deg)}}
@keyframes sway3{0%,100%{transform:scaleX(-1) rotate(8deg)}50%{transform:scaleX(-1) rotate(5deg)}}
@media (prefers-reduced-motion:reduce){.nature{animation:none!important}}
.hero{background:
    linear-gradient(115deg,rgba(246,251,240,.96) 0%,rgba(243,249,236,.9) 45%,rgba(236,247,226,.55) 100%),
    url(nature/canopy-light.webp) center/cover no-repeat}
.hero::before{z-index:0}
.hero .role{background:rgba(255,255,255,.85);backdrop-filter:blur(4px)}
.nav .logo b{font-weight:900}
.hero-inner{z-index:2}
section{position:relative;overflow:hidden}
.wrap{position:relative;z-index:2}
/* テーマアイコン */
.theme-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media (max-width:900px){.theme-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:420px){.theme-grid{gap:12px}}
.theme{position:relative;display:flex;flex-direction:column;gap:10px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:22px 20px 18px;color:var(--text);overflow:hidden;transition:transform .35s ease,box-shadow .35s ease,border-color .35s ease}
.theme::after{content:"";position:absolute;right:-30px;bottom:-30px;width:120px;height:120px;background:url(nature/sprout.webp) center/contain no-repeat;opacity:.09;transform:rotate(-20deg);transition:opacity .35s ease,transform .35s ease}
.theme:hover{transform:translateY(-6px);box-shadow:0 18px 36px rgba(40,90,30,.14);border-color:var(--accent);opacity:1}
.theme:hover::after{opacity:.22;transform:rotate(-8deg) scale(1.08)}
.theme .ti{width:58px;height:58px;border-radius:18px;display:flex;align-items:center;justify-content:center;background:linear-gradient(140deg,#8cc63f,#3c9a3f);color:#fff;box-shadow:0 8px 18px rgba(60,154,63,.28)}
.theme .ti i,.theme .ti svg{width:28px;height:28px;stroke-width:1.8}
.theme .tn{font-size:11px;font-weight:700;color:var(--accent);letter-spacing:.2em}
.theme h3{font-size:17px;line-height:1.45}
.theme p{color:var(--muted);font-size:12.8px;line-height:1.7;flex:1}
.theme .go{display:flex;align-items:center;gap:6px;font-size:12.5px;font-weight:700;color:var(--accent)}
.theme .go i,.theme .go svg{width:15px;height:15px;transition:transform .3s}
.theme:hover .go svg{transform:translateX(4px)}
@media (max-width:420px){.theme{padding:16px 14px 14px;border-radius:16px}.theme .ti{width:46px;height:46px;border-radius:14px}.theme p{display:none}.theme h3{font-size:15px}}
/* ハイライト */
.news{display:grid;gap:12px;max-width:860px}
.news a{display:flex;gap:16px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;color:var(--text);transition:border-color .3s,transform .3s}
.news a:hover{border-color:var(--accent);transform:translateX(4px);opacity:1}
.news time{flex:0 0 74px;color:var(--accent);font-weight:700;font-size:13px}
.news span{font-size:14.5px}
.news i,.news svg{margin-left:auto;width:16px;height:16px;color:var(--accent);flex:0 0 auto}
/* 下層ページのバナー */
.page-hero{position:relative;overflow:hidden;padding:130px 20px 64px;background:
    linear-gradient(180deg,rgba(243,249,236,.82),rgba(243,249,236,.95)),
    url(nature/canopy-sky.webp) center/cover no-repeat}
.page-hero .wrap{display:flex;gap:22px;align-items:center}
.page-hero .ti{flex:0 0 78px;width:78px;height:78px;border-radius:24px;display:flex;align-items:center;justify-content:center;background:linear-gradient(140deg,#8cc63f,#3c9a3f);color:#fff;box-shadow:0 10px 24px rgba(60,154,63,.3)}
.page-hero .ti svg{width:38px;height:38px;stroke-width:1.7}
.page-hero h1{font-size:clamp(26px,5.5vw,40px);font-weight:900;letter-spacing:.04em}
.page-hero p{color:var(--muted);margin-top:6px;max-width:640px}
.crumb{font-size:12px;color:var(--muted);margin-bottom:6px}
.crumb a{color:var(--accent)}
@media (max-width:560px){.page-hero .wrap{flex-direction:column;align-items:flex-start}.page-hero{padding-top:96px}.nav ul{display:none}.theme-tabs{top:50px}}
/* テーマ切替タブ */
.theme-tabs{position:sticky;top:53px;z-index:90;background:rgba(243,249,236,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.theme-tabs .in{max-width:1080px;margin:0 auto;display:flex;gap:6px;overflow-x:auto;padding:8px 16px;scrollbar-width:none}
.theme-tabs .in::-webkit-scrollbar{display:none}
.theme-tabs a{flex:0 0 auto;display:flex;align-items:center;gap:6px;font-size:12.5px;color:var(--muted);padding:6px 12px;border-radius:999px;border:1px solid transparent}
.theme-tabs a svg{width:15px;height:15px}
.theme-tabs a:hover{color:var(--accent);opacity:1}
.theme-tabs a.on{background:var(--accent);color:#fff}
/* 前後ナビ */
.pn{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
.pn a{display:flex;flex-direction:column;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px;color:var(--text)}
.pn a:hover{border-color:var(--accent);opacity:1}
.pn small{color:var(--accent);font-size:11.5px;font-weight:700;letter-spacing:.14em}
.pn .next{text-align:right}
/* Instagram投稿 */
.ig-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}
.ig{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:var(--text);transition:transform .3s,border-color .3s}
.ig:hover{transform:translateY(-4px);border-color:var(--accent);opacity:1}
.ig img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.ig .b{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px}
.ig time{color:var(--accent);font-size:12px;font-weight:700}
.ig p{font-size:13.5px;line-height:1.65}
.ig .src{font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:4px;margin-top:2px}
.ig .src svg{width:13px;height:13px}
/* GREEN VIBES */
.yt-card{display:flex;gap:22px;align-items:center;background:linear-gradient(120deg,#1f4d24,#3c9a3f 60%,#8cc63f);color:#fff;border-radius:20px;padding:26px 28px;position:relative;overflow:hidden}
.yt-card::after{content:"";position:absolute;right:-40px;top:-30px;width:260px;height:260px;background:url(nature/branch.webp) center/contain no-repeat;opacity:.25}
.yt-card .ti{flex:0 0 70px;height:70px;border-radius:20px;background:rgba(255,255,255,.16);display:flex;align-items:center;justify-content:center}
.yt-card .ti svg{width:36px;height:36px}
.yt-card h3{font-size:20px}
.yt-card p{opacity:.9;font-size:14px;margin-top:4px}
.yt-card .btn{background:#fff;color:#1f4d24;margin-top:14px}
@media (max-width:560px){.yt-card{flex-direction:column;align-items:flex-start}}
.hub-col h3{display:flex;align-items:center;gap:6px}
footer .mini{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-bottom:12px}
footer .mini a{color:var(--muted);font-size:12px}
.theme-grid{grid-template-columns:repeat(4,1fr)}
/* 数字で見る */
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
@media (max-width:820px){.stat-grid{grid-template-columns:repeat(2,1fr)}}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;display:flex;flex-direction:column;gap:6px;position:relative;overflow:hidden}
.kpi .ki{width:40px;height:40px;border-radius:12px;background:var(--accent-dim);color:var(--accent);display:flex;align-items:center;justify-content:center}
.kpi .ki svg{width:20px;height:20px}
.kpi .kv{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:clamp(28px,5vw,40px);line-height:1.1;color:var(--text)}
.kpi .kv small{font-size:.45em;color:var(--muted);margin-left:2px;font-weight:700}
.kpi .kl{font-size:13px;font-weight:700}
.kpi .kd{font-size:11.5px;color:var(--muted);line-height:1.6}
/* チャート共通 */
.chart{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 24px;margin-bottom:22px}
.chart h3{font-size:16px;display:flex;align-items:center;gap:8px}
.chart h3 svg{width:18px;height:18px;color:var(--accent)}
.chart .sub{color:var(--muted);font-size:12.5px;margin:2px 0 14px}
.chart svg.viz{width:100%;height:auto;display:block;overflow:visible}
.chart svg text{font-family:"Noto Sans JP",sans-serif}
.chart details{margin-top:10px;font-size:12.5px;color:var(--muted)}
.chart details summary{cursor:pointer;color:var(--accent);font-weight:700}
.chart table{border-collapse:collapse;margin-top:8px;width:100%;max-width:520px}
.chart td,.chart th{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left}
.chart td.n{text-align:right;font-variant-numeric:tabular-nums}
.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}
.chart-grid .chart{margin-bottom:0}
.chart-grid .wide{grid-column:1/-1}
[data-tip]{cursor:default}
.tip{position:fixed;z-index:300;pointer-events:none;background:#1e3322;color:#fff;font-size:12px;line-height:1.5;padding:6px 10px;border-radius:8px;box-shadow:0 6px 16px rgba(0,0,0,.18);opacity:0;transition:opacity .12s;max-width:240px}
.tip.on{opacity:1}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin-top:8px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}
/* 論文 */
.pub{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px 28px;display:flex;gap:22px}
.pub .pi{flex:0 0 64px;height:64px;border-radius:18px;background:linear-gradient(140deg,#8cc63f,#3c9a3f);color:#fff;display:flex;align-items:center;justify-content:center}
.pub .pi svg{width:32px;height:32px}
.pub .jr{color:var(--accent);font-weight:700;font-size:13px;letter-spacing:.04em}
.pub h3{font-size:18px;line-height:1.55;margin:6px 0 10px}
.pub .au{font-size:13px;color:var(--muted);line-height:1.8}
.pub .au b{color:var(--text);background:var(--accent-dim);padding:0 4px;border-radius:4px}
.pub .kw{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
@media (max-width:560px){.pub{flex-direction:column}}
.mini-card{display:flex;gap:12px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.mini-card .ki{flex:0 0 38px;height:38px;border-radius:11px;background:var(--accent-dim);color:var(--accent);display:flex;align-items:center;justify-content:center}
.mini-card .ki svg{width:19px;height:19px}
.mini-card h4{font-size:14.5px;line-height:1.5}
.mini-card p{font-size:12.5px;color:var(--muted);margin-top:2px}
.mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.video{position:relative;aspect-ratio:16/9;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#000;max-width:760px}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.qr{display:flex;gap:24px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px;max-width:560px;margin:30px auto 0}
.qr img{width:150px;height:150px}
.qr p{font-size:13px;color:var(--muted)}
.qr strong{display:block;font-size:15px;color:var(--text);margin-bottom:4px}
@media (max-width:480px){.qr{flex-direction:column;text-align:center}}
.award .ic svg{width:22px;height:22px;color:var(--accent)}
.prof-col h3 svg,.hub-col h3 svg{width:16px;height:16px}
.fact dt{display:flex;align-items:center;gap:6px}
.fact dt svg{width:14px;height:14px}
'''

LUCIDE = '<script src="https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js"></script>'

THEMES = [
    ('profile',   'user-round',    'PROFILE',   'プロフィール',       '経歴・役職・資格・段位。森一真がどんな人かをひと目で。'),
    ('research',  'bell-ring',     'RESEARCH',  '研究:押しボタンPJ',  '「おはよう」ボタンで独居高齢者を見守る、10年続く地域研究。'),
    ('publications','book-open-text','PUBLICATIONS','論文・学会発表', 'Am J Cardiol 掲載の共著論文と、日本公衆衛生学会での発表。'),
    ('scs',       'hand-heart',    'SCS',       'SCS 地域交流',       '学生団体SCSの代表として、団地サロンや子どもの居場所へ。'),
    ('community', 'radio',         'COMMUNITY', 'バルーナーズDAO・ラジオ', 'DAOのモデレーター、えびすFMのラジオパーソナリティ。'),
    ('education', 'graduation-cap','OUTREACH',  '教育・発信',         '中高生への出張授業、学会発表、地域での健康講演。'),
    ('awards',    'trophy',        'AWARDS',    '実績・表彰',         'CSO志支援金、国際ソロプチミスト表彰、大臣からの手紙ほか。'),
    ('media',     'newspaper',     'MEDIA',     'メディア・掲載',     'サガテレビでの放映、大学の公式発表、地域紙・ラジオ。'),
    ('hobbies',   'palette',       'HOBBIES',   '趣味・アート',       '切り絵(美術館展示)・詩吟1級・少林寺拳法初段・笑い文字。'),
    ('creative',  'clapperboard',  'CREATIVE',  '動画編集・執筆',     'GREEN VIBES CHANNEL運営、ショート動画編集、Kindle・note。'),
    ('gallery',   'images',        'GALLERY',   'ギャラリー',         '団地のサロン、夏祭り、小学校、地域イベント。活動の写真集。'),
    ('contact',   'mail',          'CONTACT',   '連絡先・SNS',        'メール・SNS・各種サイトへのリンクと、このページのQRコード。'),
]

def head(title, desc, rel=''):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="森 一真 公式プロフィール">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Zen+Kaku+Gothic+New:wght@500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header>
  <nav class="nav">
    <a class="logo" href="index.html"><i data-lucide="leaf"></i><b>MORI<span>.</span>KAZUMA</b></a>
    <ul>
      <li><a href="index.html#themes">Themes</a></li>
      <li><a href="awards.html">Awards</a></li>
      <li><a href="index.html#gallery">Gallery</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
  </nav>
</header>
'''

FOOT = '''<footer>
  <div class="mini">''' + ''.join(f'<a href="{k}.html">{t}</a>' for k, _, _, t, _ in THEMES) + '''</div>
  © 2026 Mori Kazuma — Medical Student / Researcher / Community
</footer>
<div class="lightbox" id="lightbox"><img alt=""></div>
''' + LUCIDE + '''
<script src="assets/site.js"></script>
</body>
</html>
'''

def tabs(cur):
    return '<nav class="theme-tabs" aria-label="テーマ"><div class="in">' + ''.join(
        f'<a href="{k}.html"{" class=\"on\"" if k == cur else ""}><i data-lucide="{ic}"></i>{t}</a>' for k, ic, _, t, _ in THEMES) + '</div></nav>\n'

def page(key, lead, body):
    idx = [t[0] for t in THEMES].index(key)
    k, ic, en, title, desc = THEMES[idx]
    prev = THEMES[idx - 1]; nxt = THEMES[(idx + 1) % len(THEMES)]
    html = head(f'{title} | 森 一真', desc)
    html += f'''<section class="page-hero">
  <img class="nature tr" src="assets/nature/leaves-hanging.webp" alt="">
  <div class="wrap">
    <span class="ti"><i data-lucide="{ic}"></i></span>
    <div>
      <p class="crumb"><a href="index.html">トップ</a> / {en}</p>
      <h1>{title}</h1>
      <p>{lead}</p>
    </div>
  </div>
</section>
''' + tabs(key) + body + f'''
<section class="alt">
  <img class="nature bl" src="assets/nature/sprout.webp" alt="">
  <div class="wrap">
    <div class="pn">
      <a href="{prev[0]}.html"><small>← PREV</small>{prev[3]}</a>
      <a class="next" href="{nxt[0]}.html"><small>NEXT →</small>{nxt[3]}</a>
    </div>
    <p style="text-align:center;margin-top:26px"><a class="btn btn-ghost" href="index.html#themes">テーマ一覧へ戻る</a></p>
  </div>
</section>
''' + FOOT
    io.open(os.path.join(ROOT, f'{key}.html'), 'w', encoding='utf-8', newline='\n').write(html)

def sec(inner, label='', title='', alt=False, deco=''):
    h = f'<section{" class=\"alt\"" if alt else ""}>\n{deco}  <div class="wrap">\n'
    if label: h += f'    <p class="sec-label fade">{label}</p>\n'
    if title: h += f'    <h2 class="sec-title fade">{title}</h2>\n'
    return h + inner + '  </div>\n</section>\n'

# ---------------------------------------------------------------- チャート部品
G = '#3c9a3f'; B = '#4a6fd1'; GRID = '#e3eedb'; INK = '#1e3322'; MUTED = '#5b7360'

def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;')

def table(rows, head):
    return ('<details><summary>表で見る</summary><table><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' +
            ''.join('<tr>' + ''.join(f'<td{" class=\"n\"" if i else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows) + '</table></details>')

def chart_wrap(icon, title, sub, svg, extra=''):
    wide = ' wide' if 'hub-svg' in svg else ''
    return f'<div class="chart fade{wide}"><h3><i data-lucide="{icon}"></i>{title}</h3><p class="sub">{sub}</p>{svg}{extra}</div>\n'

def hbars(items, maxv=100, unit='%', w=520, lw=170):
    """横棒(単系列)。items=[(label, value, tip)]"""
    rh = 34; h = rh * len(items) + 24; bw = w - lw - 70
    out = [f'<svg class="viz" viewBox="0 0 {w} {h}" role="img">']
    for t in (0, 25, 50, 75, 100) if maxv == 100 else ():
        x = lw + bw * t / 100
        out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{h-20}" stroke="{GRID}" stroke-width="1"/><text x="{x:.1f}" y="{h-4}" font-size="11" fill="{MUTED}" text-anchor="middle">{t}{unit}</text>')
    for i, (lab, v, tip) in enumerate(items):
        y = i * rh + 6; bl = max(bw * v / maxv, 4)
        out.append(f'<text x="{lw-10}" y="{y+15}" font-size="12.5" fill="{INK}" text-anchor="end">{esc(lab)}</text>')
        out.append(f'<g data-tip="{esc(tip)}"><rect x="{lw}" y="{y-4}" width="{bw}" height="30" fill="transparent"/><path d="M{lw},{y} h{bl-4:.1f} a4,4 0 0 1 4,4 v12 a4,4 0 0 1 -4,4 h-{bl-4:.1f} z" fill="{G}"/></g>')
        out.append(f'<text x="{lw+bl+8:.1f}" y="{y+15}" font-size="12.5" font-weight="700" fill="{INK}">{v:g}{unit}</text>')
    out.append('</svg>')
    return ''.join(out)

def columns(items, w=520, h=220, unit=''):
    """縦棒(単系列)。items=[(label, value, tip)]"""
    n = len(items); mx = max(v for _, v, _ in items); top = 24; base = h - 30
    slot = (w - 40) / n; bw = min(24 * 1.6, slot * .5)
    out = [f'<svg class="viz" viewBox="0 0 {w} {h}" style="max-width:{w}px" role="img"><line x1="20" y1="{base}" x2="{w-20}" y2="{base}" stroke="{GRID}"/>']
    for i, (lab, v, tip) in enumerate(items):
        cx = 20 + slot * (i + .5); bh = (base - top) * v / mx if mx else 0; x = cx - bw / 2; y = base - bh
        out.append(f'<g data-tip="{esc(tip)}"><rect x="{cx-slot/2:.1f}" y="{top}" width="{slot:.1f}" height="{base-top}" fill="transparent"/>')
        if v:
            out.append(f'<path d="M{x:.1f},{base} v-{bh-4:.1f} a4,4 0 0 1 4,-4 h{bw-8:.1f} a4,4 0 0 1 4,4 v{bh-4:.1f} z" fill="{G}"/>')
        out.append(f'</g><text x="{cx:.1f}" y="{y-7:.1f}" font-size="12.5" font-weight="700" fill="{INK}" text-anchor="middle">{v:g}{unit}</text>')
        out.append(f'<text x="{cx:.1f}" y="{h-10}" font-size="12" fill="{MUTED}" text-anchor="middle">{esc(lab)}</text>')
    out.append('</svg>')
    return ''.join(out)

def donut(parts, center, sub, size=220):
    """parts=[(label, value, color)]"""
    import math
    tot = sum(v for _, v, _ in parts); r = 80; c = size / 2; sw = 26; a0 = -math.pi / 2; gap = 0.03
    out = [f'<svg class="viz" viewBox="0 0 {size} {size}" style="max-width:240px;margin:0 auto" role="img">']
    for lab, v, col in parts:
        a1 = a0 + 2 * math.pi * v / tot
        s0, s1 = a0 + gap / 2, a1 - gap / 2
        x0, y0 = c + r * math.cos(s0), c + r * math.sin(s0); x1, y1 = c + r * math.cos(s1), c + r * math.sin(s1)
        large = 1 if s1 - s0 > math.pi else 0
        out.append(f'<path data-tip="{esc(lab)}: {v:g}名" d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        a0 = a1
    out.append(f'<text x="{c}" y="{c+4}" text-anchor="middle" font-size="30" font-weight="900" fill="{INK}" font-family="Zen Kaku Gothic New">{center}</text><text x="{c}" y="{c+26}" text-anchor="middle" font-size="12" fill="{MUTED}">{sub}</text></svg>')
    return ''.join(out)

def gauge(v, lo=0, hi=1, label=''):
    w = 1000; x0 = 20; x1 = w - 20; px = x0 + (x1 - x0) * (v - lo) / (hi - lo)
    return (f'<svg class="viz" viewBox="0 0 {w} 70" role="img"><rect x="{x0}" y="26" width="{x1-x0}" height="12" rx="6" fill="{GRID}"/>'
            f'<rect x="{x0}" y="26" width="{px-x0:.1f}" height="12" rx="6" fill="{G}"/>'
            f'<g data-tip="{esc(label)}"><circle cx="{px:.1f}" cy="32" r="9" fill="{G}" stroke="#fff" stroke-width="3"/></g>'
            f'<text x="{px:.1f}" y="16" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">平均 {v}</text>'
            f'<text x="{x0}" y="62" font-size="13" fill="{MUTED}">0(死亡と同等)</text><text x="{x1}" y="62" font-size="13" fill="{MUTED}" text-anchor="end">1.0(完全な健康)</text></svg>')

def flow_svg():
    """押しボタンの見守りフロー図"""
    nodes = [('bell-ring', '毎朝ボタンを押す', '独居の高齢者'), ('radio-tower', '電波で知らせる', '子機 → 受信機'),
             ('user-check', '見守り担当が確認', '自治会長・民生委員'), ('phone-call', '異変時は連絡・訪問', '家族・地域包括と連携'),
             ('chart-line', '記録をデータ化', '佐賀大学が分析・改善')]
    w = 1000; bw = 172; gap = (w - bw * 5) / 4
    out = [f'<svg class="viz" viewBox="0 0 {w} 190" role="img" aria-label="押しボタンの見守りの流れ">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8cc63f"/></marker></defs>']
    for i, (ic, t, sub) in enumerate(nodes):
        x = i * (bw + gap)
        out.append(f'<rect x="{x:.1f}" y="20" width="{bw}" height="150" rx="18" fill="#fff" stroke="#d2e6c2"/>'
                   f'<circle cx="{x+bw/2:.1f}" cy="62" r="26" fill="#3c9a3f"/>'
                   f'<foreignObject x="{x+bw/2-13:.1f}" y="49" width="26" height="26"><i data-lucide="{ic}" style="color:#fff;width:26px;height:26px"></i></foreignObject>'
                   f'<text x="{x+bw/2:.1f}" y="118" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">{t}</text>'
                   f'<text x="{x+bw/2:.1f}" y="142" text-anchor="middle" font-size="12" fill="{MUTED}">{sub}</text>'
                   f'<text x="{x+16:.1f}" y="42" font-size="12" font-weight="700" fill="#8cc63f">0{i+1}</text>')
        if i < 4:
            out.append(f'<line x1="{x+bw+6:.1f}" y1="95" x2="{x+bw+gap-6:.1f}" y2="95" stroke="#8cc63f" stroke-width="2.5" marker-end="url(#ah)"/>')
    out.append('</svg>')
    return '<div style="overflow-x:auto"><div style="min-width:760px">' + ''.join(out) + '</div></div>'

def hub_svg(center, spokes):
    """中心から放射状に広がる図。spokes=[(icon,label,sub)]"""
    import math
    w, h = 760, 430; cx, cy = w / 2, h / 2; R = 160
    out = [f'<svg class="viz" viewBox="0 0 {w} {h}" role="img">']
    pts = []
    for i in range(len(spokes)):
        a = -math.pi / 2 + 2 * math.pi * i / len(spokes)
        pts.append((cx + R * 1.45 * math.cos(a), cy + R * math.sin(a)))
    for x, y in pts:
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#cfe6bb" stroke-width="2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="#3c9a3f"/><text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="22" font-weight="900" fill="#fff" font-family="Zen Kaku Gothic New">{center[0]}</text><text x="{cx}" y="{cy+20}" text-anchor="middle" font-size="11.5" fill="#e9f6dc">{center[1]}</text>')
    for (x, y), (ic, lab, sub) in zip(pts, spokes):
        out.append(f'<g data-tip="{esc(lab)}:{esc(sub)}"><rect x="{x-82:.1f}" y="{y-30:.1f}" width="164" height="60" rx="14" fill="#fff" stroke="#d2e6c2"/>'
                   f'<foreignObject x="{x-72:.1f}" y="{y-12:.1f}" width="24" height="24"><i data-lucide="{ic}" style="color:#3c9a3f;width:22px;height:22px"></i></foreignObject>'
                   f'<text x="{x-42:.1f}" y="{y-3:.1f}" font-size="13.5" font-weight="700" fill="{INK}">{esc(lab)}</text>'
                   f'<text x="{x-42:.1f}" y="{y+15:.1f}" font-size="11" fill="{MUTED}">{esc(sub)}</text></g>')
    out.append('</svg>')
    return '<div class="hub-svg" style="overflow-x:auto"><div style="min-width:600px;max-width:860px;margin:0 auto">' + ''.join(out) + '</div></div>'

def year_line(events):
    """年表グラフ。2016年の運用開始〜2023年は省略記号でつなぎ、2023年以降を広く取る"""
    w = 1000; base = 200
    xs = {2016: 80, 2023: 330, 2024: 530, 2025: 730, 2026: 920}
    out = [f'<svg class="viz" viewBox="0 0 {w} 260" role="img">',
           f'<line x1="40" y1="{base}" x2="{xs[2016]+60}" y2="{base}" stroke="#cfe6bb" stroke-width="3"/>',
           f'<line x1="{xs[2016]+60}" y1="{base}" x2="{xs[2023]-60}" y2="{base}" stroke="#cfe6bb" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>',
           f'<text x="{(xs[2016]+xs[2023])/2:.0f}" y="{base-12}" text-anchor="middle" font-size="12.5" fill="{MUTED}">住民主導で7年間 運用を継続</text>',
           f'<line x1="{xs[2023]-60}" y1="{base}" x2="{w-30}" y2="{base}" stroke="#cfe6bb" stroke-width="3"/>']
    for y, x in xs.items():
        out.append(f'<text x="{x}" y="{base+30}" text-anchor="middle" font-size="14" font-weight="700" fill="{MUTED}">{y}</text>')
    stack = {}
    for y, lab in events:
        k = stack.get(y, 0); stack[y] = k + 1
        yy = base - 34 - k * 40; x = xs[y]
        out.append(f'<g data-tip="{y}年:{esc(lab)}"><line x1="{x}" y1="{base}" x2="{x}" y2="{yy+12}" stroke="#d2e6c2"/><circle cx="{x}" cy="{base}" r="7" fill="{G}" stroke="#fff" stroke-width="2"/>'
                   f'<rect x="{x-88}" y="{yy-16}" width="176" height="28" rx="14" fill="#fff" stroke="#bfe0a6"/><text x="{x}" y="{yy+3}" text-anchor="middle" font-size="13" fill="{INK}">{esc(lab)}</text></g>')
    out.append('</svg>')
    return '<div style="overflow-x:auto"><div style="min-width:760px">' + ''.join(out) + '</div></div>'

# ---------------------------------------------------------------- 各ページ
# 1 プロフィール
about2 = (about_inner.replace('<dt>NICKNAME</dt>', '<dt><i data-lucide="smile"></i>NICKNAME</dt>').replace('<dt>AFFILIATION</dt>', '<dt><i data-lucide="school"></i>AFFILIATION</dt>')
          .replace('<dt>ROLE</dt>', '<dt><i data-lucide="badge-check"></i>ROLE</dt>').replace('<dt>STRENGTHS</dt>', '<dt><i data-lucide="sparkles"></i>STRENGTHS</dt>')
          .replace('<h3>経歴・役職</h3>', '<h3><i data-lucide="briefcase"></i> 経歴・役職</h3>').replace('<h3>資格・段位</h3>', '<h3><i data-lucide="award"></i> 資格・段位</h3>'))
lang = '<div class="chart-grid">' + chart_wrap('languages', '語学スコア', '満点に対する到達度', hbars([('TOEIC 760 / 990', 76.8, 'TOEIC 760点(満点990)'), ('TOEFL iBT 80 / 120', 66.7, 'TOEFL iBT 従来スコア80相当(CEFR B2)')], lw=150),
        table([('TOEIC', '760 / 990'), ('TOEFL iBT', '80 / 120 相当')], ['試験', 'スコア'])) + \
    chart_wrap('compass', '活動の広がり', 'いま取り組んでいる5つの領域', hub_svg(('森 一真', 'もりぞう'), [('stethoscope', '医学', '佐賀大学 医学科'), ('bell-ring', '研究', '押しボタンPJ'), ('hand-heart', '地域交流', 'SCS 代表'), ('radio', 'コミュニティ', 'DAO・ラジオ'), ('clapperboard', '発信', 'YouTube・執筆')])) + '</div>'
page('profile', '医学生・研究員・地域活動家。データと共感で、人と地域をつなぐ。', sec(about2) + sec(lang, 'AT A GLANCE', 'ひと目でわかる森一真', alt=True))

# 2 研究
research_body = research.replace('    <h3 class="works-sub fade">押しボタンプロジェクト(おはようボタン)</h3>\n', '')
grant = '''    <h3 class="works-sub fade" style="margin-top:56px">関連する研究助成</h3>
    <div class="org-grid">
      <div class="org fade">
        <img class="org-img" src="assets/photos/oshibotan-danchi.webp" alt="佐賀市内の団地" loading="lazy">
        <span class="tag">GRANT</span>
        <h4>地域みらい創生プロジェクト(令和5年度)</h4>
        <p>「地域に根差した高齢者単独世帯の孤独死・突然死回避のシステム構築」に取り組みました。</p>
      </div>
    </div>
'''
sc_items = [('地域への信頼感', 56.3, '地域への信頼感が向上した参加者 56.3%'), ('社会的結束感', 56.3, '社会的結束感が向上 56.3%'),
            ('社会参加', 18.8, '社会参加が向上 18.8%'), ('互恵性', 6.3, '互恵性が向上 6.3%')]
outcome = [('ボタン押下率95%以上', 100, '参加者13名全員が有効日数の95%以上で押下'), ('生活リズム・役割意識の形成', 64.3, '14名中9名(約64%)')]
charts = (chart_wrap('workflow', '見守りの流れ', 'ボタン1つで、本人・地域・大学がつながる仕組み', flow_svg()) +
    '<div class="chart-grid">' +
    chart_wrap('activity', '参加者に見られた変化', '1年間の運用・インタビュー調査より(参加者に占める割合)', hbars(outcome, lw=200),
               table([(a, f'{b:g}%') for a, b, _ in outcome], ['項目', '割合'])) +
    chart_wrap('users', 'ソーシャルキャピタルの変化', '各項目が向上した参加者の割合', hbars(sc_items, lw=130),
               table([(a, f'{b:g}%') for a, b, _ in sc_items], ['項目', '向上した割合'])) +
    '</div><div style="height:22px"></div>' +
    chart_wrap('heart-pulse', '生活の質(QOL)', 'EQ-5D-5L 平均スコア 0.898(SD 0.060)。地域在住高齢者として良好な水準', gauge(0.898, label='平均 0.898 / SD 0.060')) +
    chart_wrap('calendar-range', '10年の歩み', '2016年の運用開始から、研究・共同開発・行政への提案へ',
               year_line([(2016, '団地で運用開始'), (2023, 'R5 地域みらい'), (2023, '研究チーム参加'), (2024, '倫理承認・研究開始'), (2024, '公衆衛生学会 発表'),
                          (2025, 'サガテレビ放映'), (2025, '公衆衛生学会 発表'), (2025, '永和システムと協議'), (2026, 'プレスリリース'), (2026, 'いろどり+実証'), (2026, '県庁で提案')])))
page('research', '佐賀大学医学部附属病院 救急医学講座 × 地域コミュニティ。「おはよう」でつながる見守りの輪。',
     sec(research_body + grant, 'OSHIBOTAN PROJECT', '押しボタンプロジェクト(おはようボタン)') +
     sec(charts, 'DATA', 'データで見る押しボタン', alt=True))

# 3 SCS
IG = [
    ('ig-johoku-heatstroke', '2026.08.02', '城北サロンで、熱中症・紫外線対策のお話と脳トレ。', 'Dbj-19jET-h'),
    ('ig-kids-place-2', '2026.06.17', '子どもの居場所へ。宿題のあとは外でも中でも元気いっぱい。', 'DZtk3PykbYb'),
    ('ig-johoku-hobby-talk', '2026.06.07', '城北サロンで「部員の趣味紹介」。折り紙・筋トレ・書道・演劇。', 'DZj8wuIkQhP'),
    ('ig-zaimoku-lecture', '2026.05.16', '材木町公民分館で熱中症をテーマに健康講演。', 'DYa_jAukwzG'),
    ('ig-johoku-cognicise', '2026.05.03', '城北団地の高齢者サロンでコグニサイズ(後出しジャンケン)。', 'DX3aCOPkbYL'),
    ('ig-kids-place-1', '2026.04.22', '上高木公民館での子どもの居場所づくりをサポート。', 'DXdaoOQkUf8'),
    ('ig-recruit-2026', '2026.04.06', '2026年度 新メンバー募集中!地域に飛び込み、同じ目線でつながる。', 'DWyKG7cEeQK'),
]
ig_html = '    <div class="ig-grid">\n' + '\n'.join(
    f'''      <a class="ig fade" href="https://www.instagram.com/p/{code}/" target="_blank" rel="noopener"><img src="assets/photos/{img}.webp" alt="{cap}" loading="lazy"><span class="b"><time>{d}</time><p>{cap}</p><span class="src"><i data-lucide="instagram"></i>@scs.official2025</span></span></a>'''
    for img, d, cap, code in IG) + '\n    </div>\n'
scs_intro = '''    <div class="act-lead fade">
      <p class="role-line">佐賀大学 学生地域交流の会(SCS) ／ 代表</p>
      <p>地域に飛び込み、そこに暮らす人たちと同じ目線でつながる学生ボランティア団体。医学科・看護学科の学生を中心に、団地の高齢者サロンでの健康講話や体操、子どもの居場所づくりのサポート、公民館での健康講演などを続けています。</p>
    </div>
    <div class="pill-links fade" style="margin-bottom:34px">
      <a href="https://scs-website-ten.vercel.app/" target="_blank" rel="noopener">SCS 公式サイト →</a>
      <a href="https://www.instagram.com/scs.official2025/" target="_blank" rel="noopener">Instagram @scs.official2025 →</a>
      <a href="https://scs-website-ten.vercel.app/contacts" target="_blank" rel="noopener">連絡先一覧(部員・関係者限定) →</a>
    </div>
    <div class="photo-row">
      <figure class="fade"><img src="assets/photos/salon-exercise.webp" alt="高齢者サロンで体操" loading="lazy"><figcaption>高齢者サロンで体操</figcaption></figure>
      <figure class="fade"><img src="assets/photos/scs-balloon-show.webp" alt="地域イベント" loading="lazy"><figcaption>地域イベント</figcaption></figure>
      <figure class="fade"><img src="assets/photos/salon-newspaper.webp" alt="活動が地域紙に" loading="lazy"><figcaption>活動が地域紙に掲載</figcaption></figure>
    </div>
'''
matsuri = '''    <p class="creative-lead fade" style="margin-top:-18px">地域の夏祭りにSCSとしてブースを出展。血圧測定、心肺蘇生(CPR)体験、妊婦体験ジャケットなど、子どもから大人まで楽しみながら健康について学べる場をつくりました。</p>
    <div class="photo-row">
      <figure class="fade"><img src="assets/photos/drv-matsuri-cpr.webp" alt="心肺蘇生体験ブース" loading="lazy"><figcaption>心肺蘇生(CPR)体験</figcaption></figure>
      <figure class="fade"><img src="assets/photos/drv-matsuri-bp.webp" alt="血圧測定" loading="lazy"><figcaption>血圧測定コーナー</figcaption></figure>
      <figure class="fade"><img src="assets/photos/drv-matsuri-booth.webp" alt="健康ブース" loading="lazy"><figcaption>SCSの健康ブース</figcaption></figure>
      <figure class="fade"><img src="assets/photos/drv-matsuri-team.webp" alt="地域の方と" loading="lazy"><figcaption>地域の方と一緒に</figcaption></figure>
      <figure class="fade"><img src="assets/photos/drv-matsuri-yagura.webp" alt="夏祭りの会場" loading="lazy"><figcaption>夏祭りの会場</figcaption></figure>
      <figure class="fade"><img src="assets/photos/drv-matsuri-selfie.webp" alt="SCSメンバーと" loading="lazy"><figcaption>SCSメンバーと</figcaption></figure>
    </div>
'''
scs_g = '    <div class="gallery fade">\n' + '\n'.join(f for f in gal_figs if any(x in f for x in ['scs-', 'salon-', 'balloon-art', 'kids-tanabata'])) + '\n    </div>\n'
scs_map = '<div class="chart-grid">' + chart_wrap('map', 'SCSの活動フィールド', '地域のさまざまな場所へ出向いています', hub_svg(('SCS', '学生地域交流の会'),
        [('armchair', '団地サロン', '健康講話・体操・脳トレ'), ('baby', '子どもの居場所', '宿題サポート・遊び'), ('mic', '健康講演', '公民館で熱中症予防など'),
         ('tent', '夏祭り', '血圧測定・CPR体験'), ('school', '小学校', '健康の授業'), ('heart-handshake', '地域イベント', 'バルーン・交流')])) + \
    chart_wrap('pie-chart', 'メンバー構成', '2025年5月時点・総勢27名', donut([('医学生', 23, G), ('薬学部・理工学部', 4, B)], '27', '名') +
        '<div class="legend" style="justify-content:center"><span><i style="background:#3c9a3f"></i>医学生 23名</span><span><i style="background:#4a6fd1"></i>薬学部・理工学部 4名</span></div>' +
        table([('医学生', '23名'), ('薬学部・理工学部', '4名')], ['所属', '人数'])) + '</div>'
page('scs', '団地のサロン、子どもの居場所、公民館。地域の「となり」にいる学生でありたい。',
     sec(scs_intro, 'SCS', 'SCS(佐賀大学学生地域交流の会)') +
     sec(scs_map, 'FIELD', '活動の全体像', alt=True) +
     sec(matsuri, 'FESTIVAL', '地域のお祭りで健康ブース') +
     sec(ig_html, 'INSTAGRAM', '最近の活動(Instagramより)', alt=True) +
     sec(scs_g, 'GALLERY', '活動の様子'))

# 4 コミュニティ
page('community', 'スポーツの力で地域課題に挑む。ファンコミュニティとラジオで、人と人をつなぐ。',
     sec(community, 'BALLOONERS DAO', '佐賀バルーナーズDAO'))

# 5 教育・発信
vcan = re.search(r'      <a class="org fade" href="https://vcan-hpv.org.*?</a>\n', other_orgs, re.S).group(0)
edu = f'''    <div class="org-grid">
{vcan}      <div class="org fade">
        <img class="org-img" src="assets/photos/drv-nishiyoka-class.webp" alt="西与賀小学校での授業" loading="lazy">
        <span class="tag">SCHOOL</span>
        <h4>佐賀市立西与賀小学校での授業(2025年6月)</h4>
        <p>SCSのメンバーと小学校を訪問し、子どもたちに向けて健康について考える授業を行いました。</p>
      </div>
      <div class="org fade">
        <img class="org-img" src="assets/photos/ig-zaimoku-lecture.webp" alt="公民館での健康講演" loading="lazy">
        <span class="tag">LECTURE</span>
        <h4>地域での健康講演</h4>
        <p>公民館や団地のサロンで、熱中症予防やフレイル予防など、医学部で学んだ知識を地域の方へ分かりやすくお伝えしています。</p>
      </div>
      <div class="org fade">
        <img class="org-img" src="assets/photos/vcan-poster.webp" alt="じぶんごとcaféのチラシ" loading="lazy" style="object-fit:contain;background:#f6f0fa">
        <span class="tag">EVENT</span>
        <h4>Vcan じぶんごとcafé(佐賀市)</h4>
        <p>佐賀市と連携したワークショップ型イベントで、参加者と一緒に健康を「自分ごと」として考えました。</p>
      </div>
    </div>
    <h3 class="works-sub fade" style="margin-top:56px">学会発表</h3>
    <ul class="timeline fade">
      <li><time>2025.10</time><span>第84回 日本公衆衛生学会総会(静岡) ポスター発表</span></li>
      <li><time>2024.10</time><span>第83回 日本公衆衛生学会総会(北海道) ポスター・口演発表</span></li>
      <li><time>2026.03</time><span>佐賀TSUNAGIコンベンションで研究成果を発表・展示</span></li>
    </ul>
'''
page('education', '学んだことを、地域と次の世代へ。授業・講演・学会での発信。', sec(edu))

# 6 実績
aw = awards
for em, ic in [('💐', 'hand-coins'), ('📰', 'newspaper'), ('🏆', 'trophy'), ('✉️', 'mail-open'), ('🏀', 'medal'), ('🎤', 'presentation'), ('✂️', 'scissors'), ('🌱', 'sprout')]:
    aw = aw.replace(f'<span class="ic">{em}</span>', f'<span class="ic"><i data-lucide="{ic}"></i></span>')
yr = chart_wrap('bar-chart-3', '年ごとの実績・発表', '日付のわかる実績・表彰・発表の件数(手紙・感謝状・展示は除く)',
    columns([('2023', 1, '地域みらい創生プロジェクト'), ('2024', 1, '第83回 日本公衆衛生学会'), ('2025', 1, '第84回 日本公衆衛生学会'), ('2026', 5, 'CSO志支援金・ソロプチミスト表彰・プレスリリース・TSUNAGI発表・論文掲載')], unit='件'),
    table([('2023', '1件'), ('2024', '1件'), ('2025', '1件'), ('2026', '5件')], ['年', '件数']))
page('awards', '団体として、個人として。これまでにいただいた評価と支援。', sec(aw) + sec(yr, 'TREND', '実績の推移', alt=True))

# 7 趣味
page('hobbies', '手を動かし、声を出し、体を動かす。切り絵・詩吟・少林寺拳法・カリンバ・笑い文字。', sec(hobbies, 'HOBBIES', '好きなこと'))

# 8 クリエイティブ
yt = '''    <div class="yt-card fade">
      <span class="ti"><i data-lucide="youtube"></i></span>
      <div style="position:relative;z-index:1">
        <h3>GREEN VIBES CHANNEL</h3>
        <p>自分で運営しているYouTubeチャンネル。花・植物・花言葉・雑学をテーマに、ショート動画とコミュニティ投稿を発信しています。</p>
        <a class="btn" href="https://www.youtube.com/@GREENVIBESch" target="_blank" rel="noopener">チャンネルを見る →</a>
      </div>
    </div>
'''
page('creative', '医療の知識を活かして、伝わる動画と文章を。YouTubeチャンネルも運営中。',
     sec(yt + '<div style="height:40px"></div>\n' + skills) +
     sec(works, 'WORKS', '制作実績', alt=True) +
     sec(services, 'SERVICES', '対応可能な業務') +
     sec('<div class="chart-grid">' + chart_wrap('pen-line', 'note の執筆本数', '年ごとの公開記事数(全11記事)', columns([('2025', 10, '2025年: 10記事'), ('2026', 1, '2026年: 1記事')], w=360, unit='本'),
         table([('2025', '10本'), ('2026', '1本')], ['年', '本数'])) +
         chart_wrap('layers', 'できること', '制作の流れ', hub_svg(('制作', '医療×伝わる'), [('scissors', 'カット', '不要部分を整理'), ('type', 'テロップ', '読みやすく'), ('music', 'BGM・SE', '雰囲気づくり'), ('wand-sparkles', 'エフェクト', '印象に残す'), ('file-text', '構成・台本', 'シナリオ作成')])) + '</div>', 'DATA', '数字と図で見る', alt=True))

pub = """    <div class="pub fade">
      <span class="pi"><i data-lucide="file-text"></i></span>
      <div>
        <span class="jr">The American Journal of Cardiology ／ 2026年8月 ／ Vol.277, pp.63–65</span>
        <h3>Performance of Cardiovascular Risk Equations for Cardiovascular Mortality Prediction in Adults With Metabolic Dysfunction-Associated Steatotic Liver Disease</h3>
        <p class="au">Tioh JK, Tsutsumi T, <b>Mori K</b>, Takahashi H, Muthiah M, Mehta A, Sperling L, Ng CH, Huang W, Yoneda M</p>
        <div class="kw"><span class="tag">MASLD(代謝機能障害関連脂肪性肝疾患)</span><span class="tag">心血管死亡の予測</span><span class="tag">PREVENT</span><span class="tag">Pooled Cohort Equations</span></div>
        <p style="color:var(--muted);font-size:13.5px">脂肪肝(MASLD)のある成人で、心血管リスク予測式(PREVENT・PCE)が心血管死亡をどの程度予測できるかを検証した国際共同研究。佐賀大学 肝臓・糖尿病・内分泌内科の立場で共著者として参加しました。</p>
        <p style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-primary" href="https://doi.org/10.1016/j.amjcard.2026.08.006" target="_blank" rel="noopener">論文を読む(DOI)</a><a class="btn btn-ghost" href="https://pubmed.ncbi.nlm.nih.gov/42600722/" target="_blank" rel="noopener">PubMed</a></p>
      </div>
    </div>
"""
confs = """    <div class="mini-grid">
      <div class="mini-card fade"><span class="ki"><i data-lucide="presentation"></i></span><div><h4>第84回 日本公衆衛生学会総会(静岡)</h4><p>2025年10月 ／ ポスター発表 ／ 押しボタンプロジェクト</p></div></div>
      <div class="mini-card fade"><span class="ki"><i data-lucide="presentation"></i></span><div><h4>第83回 日本公衆衛生学会総会(北海道)</h4><p>2024年10月 ／ ポスター・口演発表 ／ 押しボタンプロジェクト</p></div></div>
      <div class="mini-card fade"><span class="ki"><i data-lucide="lightbulb"></i></span><div><h4>佐賀TSUNAGIコンベンション</h4><p>2026年3月 ／ 研究成果の発表・展示</p></div></div>
      <div class="mini-card fade"><span class="ki"><i data-lucide="users"></i></span><div><h4>佐賀疫学研究会</h4><p>2026年1月 ／ 参加</p></div></div>
    </div>
"""
fields = chart_wrap('network', '研究のフィールド', '地域の見守りから、肝臓・循環器の臨床研究まで', hub_svg(('研究', 'Research'),
    [('bell-ring', '地域見守り', '押しボタンPJ'), ('users', '社会疫学', 'ソーシャルキャピタル'), ('activity', '肝臓・代謝', 'MASLD'), ('heart-pulse', '循環器', '心血管リスク予測'), ('siren', '救急医学', '孤立死・突然死の回避')]))
page('publications', '査読付き国際誌への共著論文と、学会での研究発表。', sec(pub, 'PAPER', '論文') + sec(confs, 'CONFERENCE', '学会・研究会発表', alt=True) + sec(fields, 'FIELDS', '研究の広がり'))

media = """    <div class="mini-grid">
      <a class="mini-card fade" href="https://www.saga-u.ac.jp/koho/%e4%bc%9a%e8%a6%8b/2026033040388" target="_blank" rel="noopener" style="color:inherit"><span class="ki"><i data-lucide="newspaper"></i></span><div><h4>佐賀大学 公式プレスリリース</h4><p>2026年3月 ／ 押しボタンプロジェクトを大学として発表</p></div></a>
      <div class="mini-card fade"><span class="ki"><i data-lucide="tv"></i></span><div><h4>サガテレビ 取材</h4><p>2026年2月 ／ 住民向け説明会の様子が取材されました</p></div></div>
      <a class="mini-card fade" href="https://youtu.be/Bt9TFAmHH0I" target="_blank" rel="noopener" style="color:inherit"><span class="ki"><i data-lucide="tv"></i></span><div><h4>サガテレビ 放映</h4><p>2025年3月 ／ 地域での活動が紹介されました</p></div></a>
      <a class="mini-card fade" href="community.html" style="color:inherit"><span class="ki"><i data-lucide="radio"></i></span><div><h4>えびすFM「バルーナーズDAOおとなりさんラジオ」</h4><p>2026年5月〜 ／ パーソナリティとして出演</p></div></a>
      <a class="mini-card fade" href="https://www.suric.saga-u.ac.jp/saga_project_map/" target="_blank" rel="noopener" style="color:inherit"><span class="ki"><i data-lucide="map-pin"></i></span><div><h4>佐賀大学 地域連携紹介マップ</h4><p>2024年9月 ／ プロジェクトが掲載</p></div></a>
      <div class="mini-card fade"><span class="ki"><i data-lucide="file-image"></i></span><div><h4>地域紙への掲載</h4><p>SCSのサロン活動が地域の新聞で紹介</p></div></div>
    </div>
"""
video = """    <div class="video fade"><iframe src="https://www.youtube-nocookie.com/embed/Bt9TFAmHH0I" title="サガテレビ おはようボタン" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
    <div class="photo-row" style="margin-top:22px">
      <figure class="fade"><img src="assets/photos/salon-newspaper.webp" alt="地域紙に掲載" loading="lazy"><figcaption>地域紙に掲載されたサロン活動</figcaption></figure>
      <figure class="fade"><img src="assets/photos/oshibotan-system.webp" alt="押しボタンの図解" loading="lazy"><figcaption>発表で使った見守りシステムの図解</figcaption></figure>
    </div>
"""
page('media', 'テレビ・大学の公式発表・地域紙・ラジオで紹介された取り組み。', sec(media, 'MEDIA', '掲載・出演') + sec(video, 'VIDEO', 'サガテレビで紹介されました', alt=True))

all_figs = list(dict.fromkeys(gal_figs + [f'      <figure><img src="assets/photos/{n}.webp" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for n, c in
    [('drv-matsuri-cpr', '夏祭りでCPR体験ブース'), ('drv-matsuri-bp', '夏祭りで血圧測定'), ('drv-matsuri-booth', 'SCSの健康ブース'), ('drv-matsuri-team', '地域の方と'), ('drv-nishiyoka-team', '西与賀小学校にて'),
     ('drv-nishiyoka-class', '小学校での授業'), ('ig-johoku-heatstroke', '城北サロンで熱中症の話'), ('ig-johoku-hobby-talk', '城北サロンで趣味紹介'), ('ig-zaimoku-lecture', '公民館で健康講演'),
     ('ig-johoku-cognicise', 'コグニサイズ'), ('ig-kids-place-1', '子どもの居場所'), ('ig-kids-place-2', '子どもの居場所(神社で)'), ('oshibotan-walk', '住民の方と一緒に'), ('oshibotan-salon-talk', '押しボタンPJの説明')]]))
page('gallery', '団地のサロン、夏祭り、小学校、地域イベント。写真で振り返る活動。', sec('    <div class="gallery fade">\n' + '\n'.join(all_figs) + '\n    </div>\n', 'GALLERY', f'活動の写真 {len(all_figs)}枚'))

import segno
segno.make('https://kazuma160504-art.github.io/', error='m').save(os.path.join(ROOT, 'assets', 'qr-site.svg'), scale=6, border=2, dark='#1e3322')
qr = """    <div class="qr fade"><img src="assets/qr-site.svg" alt="このサイトのQRコード"><p><strong>このページのQRコード</strong>名刺やスライドに載せてご利用ください。<br>https://kazuma160504-art.github.io/</p></div>
"""
hub_icons = hub.replace('<h3>SNS</h3>', '<h3><i data-lucide="share-2"></i>SNS</h3>').replace('<h3>CREATIVE</h3>', '<h3><i data-lucide="clapperboard"></i>CREATIVE</h3>').replace('<h3>PROJECT / PROFILE</h3>', '<h3><i data-lucide="sprout"></i>PROJECT / PROFILE</h3>')
hub_icons = hub_icons.replace('<a href="#works">動画編集の実績<small>このページ内</small></a>', '<a href="creative.html">動画編集の実績<small>CREATIVE</small></a>')
hub_icons = hub_icons.replace('        <a href="https://scs-website-ten.vercel.app/contacts"', '        <a href="https://www.instagram.com/scs.official2025/" target="_blank" rel="noopener">SCS Instagram<small>@scs.official2025</small></a>\n        <a href="https://scs-website-ten.vercel.app/contacts"')
page('contact', '研究・地域活動、講演・取材、制作のご依頼など、お気軽にご連絡ください。', sec(contact_box + hub_icons + qr, 'CONTACT', '連絡先・リンク'))

# ---------------------------------------------------------------- トップ
hero = take('<section class="hero" id="top">', '</section>') + '</section>\n'
hero = hero.replace('<section class="hero" id="top">', '<section class="hero" id="top">\n  <img class="nature tl" src="assets/nature/leaves-hanging.webp" alt="">\n  <img class="nature br" src="assets/nature/branch-long.webp" alt="">')
hero = hero.replace('<a class="btn btn-ghost" href="#activities">活動を見る</a>', '<a class="btn btn-ghost" href="#themes">12のテーマを見る</a>')
hero = hero.replace('<a class="btn btn-ghost" href="#awards">実績・表彰</a>', '<a class="btn btn-ghost" href="awards.html">実績・表彰</a>')

tiles = '    <div class="theme-grid">\n' + '\n'.join(
    f'''      <a class="theme fade" href="{k}.html"><span class="ti"><i data-lucide="{ic}"></i></span><span class="tn">{n:02d} {en}</span><h3>{t}</h3><p>{d}</p><span class="go">くわしく見る<i data-lucide="arrow-right"></i></span></a>'''
    for n, (k, ic, en, t, d) in enumerate(THEMES, 1)) + '\n    </div>\n'

news = '''    <div class="news fade">
      <a href="publications.html"><time>2026.08</time><span>共著論文が The American Journal of Cardiology に掲載</span><i data-lucide="chevron-right"></i></a>
      <a href="awards.html"><time>2026.07</time><span>SCSとして佐賀県CSO"志"支援金に採択されました</span><i data-lucide="chevron-right"></i></a>
      <a href="community.html"><time>2026.05</time><span>えびすFM「バルーナーズDAOおとなりさんラジオ」パーソナリティに</span><i data-lucide="chevron-right"></i></a>
      <a href="research.html"><time>2026.04</time><span>新型「いろどり+ボタン」の実証実験を開始</span><i data-lucide="chevron-right"></i></a>
      <a href="research.html"><time>2026.03</time><span>押しボタンプロジェクトが佐賀大学から公式発表</span><i data-lucide="chevron-right"></i></a>
      <a href="awards.html"><time>2026.02</time><span>SCSが国際ソロプチミスト佐賀有明より表彰</span><i data-lucide="chevron-right"></i></a>
    </div>
'''
extra_figs = [f'      <figure><img src="assets/photos/{n}.webp" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for n, c in [('drv-matsuri-cpr', '夏祭りでCPR体験ブース'), ('ig-johoku-hobby-talk', '城北サロンで趣味紹介'), ('drv-nishiyoka-team', '西与賀小学校にて'), ('ig-zaimoku-lecture', '公民館で健康講演')]]
gal_top = '    <div class="gallery fade">\n' + '\n'.join((extra_figs + gal_figs[:10])) + '\n    </div>\n    <p style="text-align:center;margin-top:20px"><a class="btn btn-ghost" href="scs.html">SCSの活動をもっと見る</a></p>\n'

hub_new = hub.replace('<h3>SNS</h3>', '<h3><i data-lucide="share-2"></i>SNS</h3>').replace('<h3>CREATIVE</h3>', '<h3><i data-lucide="clapperboard"></i>CREATIVE</h3>').replace('<h3>PROJECT / PROFILE</h3>', '<h3><i data-lucide="sprout"></i>PROJECT / PROFILE</h3>')
hub_new = hub_new.replace('<a href="#works">動画編集の実績<small>このページ内</small></a>', '<a href="creative.html">動画編集の実績<small>CREATIVE</small></a>')
hub_new = hub_new.replace('        <a href="https://scs-website-ten.vercel.app/contacts"', '        <a href="https://www.instagram.com/scs.official2025/" target="_blank" rel="noopener">SCS Instagram<small>@scs.official2025</small></a>\n        <a href="https://scs-website-ten.vercel.app/contacts"')

index = head('森 一真 | 医学生・研究員 — 公式プロフィール',
             '佐賀大学医学部医学科・押しボタンプロジェクト研究員・SCS代表、森一真の公式プロフィール。研究・地域活動、実績、趣味、制作、連絡先を12のテーマでまとめています。')
index += hero + '\n'
index += sec(tiles, 'THEMES', '12のテーマで、森一真を知る', alt=True,
             deco='  <img class="nature tr" src="assets/nature/branch.webp" alt="" style="width:min(220px,30vw);opacity:.85">\n').replace('<section class="alt">', '<section id="themes" class="alt">', 1)
kpis = [('calendar-heart', 10, '年+', '見守りの継続', '2016年から団地で運用'), ('bell-ring', 95, '%+', 'ボタン押下率', '参加者13名全員'),
        ('shield-check', 0, '件', '孤立死', '研究運用の1年11か月'), ('book-open-text', 1, '本', '査読付き論文', 'Am J Cardiol 2026'),
        ('presentation', 3, '回', '学会・研究発表', '公衆衛生学会ほか'), ('trophy', 8, '件', '実績・表彰', '助成・表彰・掲載'),
        ('users', 27, '名', 'SCSの仲間', '2025年5月時点'), ('pen-line', 11, '本', 'note記事', 'エッセイを発信')]
kpi_html = '    <div class="stat-grid">\n' + '\n'.join(
    f'      <div class="kpi fade"><span class="ki"><i data-lucide="{ic}"></i></span><span class="kv"><span data-count="{v}">{v}</span><small>{u}</small></span><span class="kl">{l}</span><span class="kd">{d}</span></div>'
    for ic, v, u, l, d in kpis) + '\n    </div>\n'
index += sec(kpi_html, 'NUMBERS', '数字で見る森一真').replace('<section>', '<section id="numbers">', 1)
index += sec(news, 'HIGHLIGHTS', '最近のできごと', alt=True).replace('<section class="alt">', '<section id="news" class="alt">', 1)
index += sec(gal_top.replace('href="scs.html">SCSの活動をもっと見る', 'href="gallery.html">写真をもっと見る'), 'GALLERY', '活動の様子').replace('<section>', '<section id="gallery">', 1)
index += sec(contact_box + hub_new, 'CONTACT', '連絡先・リンク',
             alt=True, deco='  <img class="nature bl" src="assets/nature/sprout.webp" alt="">\n').replace('<section class="alt">', '<section id="contact" class="alt">', 1)
index += FOOT
io.open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(index)

io.open(os.path.join(ROOT, 'assets', 'style.css'), 'w', encoding='utf-8', newline='\n').write(css_new.strip() + '\n')
js = '''// 共通スクリプト: アイコン描画・スクロールフェード・写真の拡大表示
if (window.lucide) lucide.createIcons();
(function(){
  var els = document.querySelectorAll('.fade');
  if(!('IntersectionObserver' in window)){ els.forEach(function(el){ el.classList.add('show'); }); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('show'); io.unobserve(e.target); } });
  }, {threshold:.12, rootMargin:'0px 0px -40px 0px'});
  els.forEach(function(el){ io.observe(el); });
})();
(function(){
  var lb=document.getElementById('lightbox'); if(!lb) return; var im=lb.querySelector('img');
  document.querySelectorAll('.gallery img,.photo-row img,.org-img').forEach(function(el){
    el.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();im.src=el.src;im.alt=el.alt;lb.classList.add('open');});
  });
  lb.addEventListener('click',function(){lb.classList.remove('open');});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('open');});
})();
// グラフのツールチップ
(function(){
  var tip=document.createElement('div'); tip.className='tip'; document.body.appendChild(tip);
  document.querySelectorAll('[data-tip]').forEach(function(el){
    el.addEventListener('mousemove',function(e){tip.textContent=el.getAttribute('data-tip');tip.style.left=(e.clientX+14)+'px';tip.style.top=(e.clientY+14)+'px';tip.classList.add('on');});
    el.addEventListener('mouseleave',function(){tip.classList.remove('on');});
  });
})();
// 数字のカウントアップ
(function(){
  var els=document.querySelectorAll('[data-count]'); if(!els.length||!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){ if(!e.isIntersecting) return; io.unobserve(e.target);
    var el=e.target, to=+el.getAttribute('data-count'), t0=null;
    function step(t){ if(!t0) t0=t; var p=Math.min((t-t0)/1100,1); el.textContent=Math.round(to*(1-Math.pow(1-p,3))); if(p<1) requestAnimationFrame(step); }
    requestAnimationFrame(step); });},{threshold:.4});
  els.forEach(function(el){ el.textContent='0'; io.observe(el); });
})();
// 現在のテーマタブを見える位置へ
(function(){ var on=document.querySelector('.theme-tabs a.on'); if(on) on.scrollIntoView({inline:'center',block:'nearest'}); })();
'''
io.open(os.path.join(ROOT, 'assets', 'site.js'), 'w', encoding='utf-8', newline='\n').write(js)
print('built', [t[0] for t in THEMES])
