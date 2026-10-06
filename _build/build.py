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
'''

LUCIDE = '<script src="https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js"></script>'

THEMES = [
    ('profile',   'user-round',    'PROFILE',   'プロフィール',       '経歴・役職・資格・段位。森一真がどんな人かをひと目で。'),
    ('research',  'bell-ring',     'RESEARCH',  '研究:押しボタンPJ',  '「おはよう」ボタンで独居高齢者を見守る、10年続く地域研究。'),
    ('scs',       'hand-heart',    'SCS',       'SCS 地域交流',       '学生団体SCSの代表として、団地サロンや子どもの居場所へ。'),
    ('community', 'radio',         'COMMUNITY', 'バルーナーズDAO・ラジオ', 'DAOのモデレーター、えびすFMのラジオパーソナリティ。'),
    ('education', 'graduation-cap','OUTREACH',  '教育・発信',         '中高生への出張授業、学会発表、地域での健康講演。'),
    ('awards',    'trophy',        'AWARDS',    '実績・表彰',         'CSO志支援金、国際ソロプチミスト表彰、大臣からの手紙ほか。'),
    ('hobbies',   'palette',       'HOBBIES',   '趣味・アート',       '切り絵(美術館展示)・詩吟1級・少林寺拳法初段・笑い文字。'),
    ('creative',  'clapperboard',  'CREATIVE',  '動画編集・執筆',     'GREEN VIBES CHANNEL運営、ショート動画編集、Kindle・note。'),
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
    <p style="text-align:center;margin-top:26px"><a class="btn btn-ghost" href="index.html#themes">8つのテーマ一覧へ戻る</a></p>
  </div>
</section>
''' + FOOT
    io.open(os.path.join(ROOT, f'{key}.html'), 'w', encoding='utf-8', newline='\n').write(html)

def sec(inner, label='', title='', alt=False, deco=''):
    h = f'<section{" class=\"alt\"" if alt else ""}>\n{deco}  <div class="wrap">\n'
    if label: h += f'    <p class="sec-label fade">{label}</p>\n'
    if title: h += f'    <h2 class="sec-title fade">{title}</h2>\n'
    return h + inner + '  </div>\n</section>\n'

# ---------------------------------------------------------------- 各ページ
# 1 プロフィール
page('profile', '医学生・研究員・地域活動家。データと共感で、人と地域をつなぐ。', sec(about_inner))

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
page('research', '佐賀大学医学部附属病院 救急医学講座 × 地域コミュニティ。「おはよう」でつながる見守りの輪。',
     sec(research_body + grant, 'OSHIBOTAN PROJECT', '押しボタンプロジェクト(おはようボタン)'))

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
page('scs', '団地のサロン、子どもの居場所、公民館。地域の「となり」にいる学生でありたい。',
     sec(scs_intro, 'SCS', 'SCS(佐賀大学学生地域交流の会)') +
     sec(matsuri, 'FESTIVAL', '地域のお祭りで健康ブース', alt=True) +
     sec(ig_html, 'INSTAGRAM', '最近の活動(Instagramより)') +
     sec(scs_g, 'GALLERY', '活動の様子', alt=True))

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
page('awards', '団体として、個人として。これまでにいただいた評価と支援。', sec(awards))

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
     sec(services, 'SERVICES', '対応可能な業務'))

# ---------------------------------------------------------------- トップ
hero = take('<section class="hero" id="top">', '</section>') + '</section>\n'
hero = hero.replace('<section class="hero" id="top">', '<section class="hero" id="top">\n  <img class="nature tl" src="assets/nature/leaves-hanging.webp" alt="">\n  <img class="nature br" src="assets/nature/branch-long.webp" alt="">')
hero = hero.replace('<a class="btn btn-ghost" href="#activities">活動を見る</a>', '<a class="btn btn-ghost" href="#themes">8つのテーマを見る</a>')
hero = hero.replace('<a class="btn btn-ghost" href="#awards">実績・表彰</a>', '<a class="btn btn-ghost" href="awards.html">実績・表彰</a>')

tiles = '    <div class="theme-grid">\n' + '\n'.join(
    f'''      <a class="theme fade" href="{k}.html"><span class="ti"><i data-lucide="{ic}"></i></span><span class="tn">{n:02d} {en}</span><h3>{t}</h3><p>{d}</p><span class="go">くわしく見る<i data-lucide="arrow-right"></i></span></a>'''
    for n, (k, ic, en, t, d) in enumerate(THEMES, 1)) + '\n    </div>\n'

news = '''    <div class="news fade">
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
             '佐賀大学医学部医学科・押しボタンプロジェクト研究員・SCS代表、森一真の公式プロフィール。研究・地域活動、実績、趣味、制作、連絡先を8つのテーマでまとめています。')
index += hero + '\n'
index += sec(tiles, 'THEMES', '8つのテーマで、森一真を知る', alt=True,
             deco='  <img class="nature tr" src="assets/nature/branch.webp" alt="" style="width:min(220px,30vw);opacity:.85">\n').replace('<section class="alt">', '<section id="themes" class="alt">', 1)
index += sec(news, 'HIGHLIGHTS', '最近のできごと').replace('<section>', '<section id="news">', 1)
index += sec(gal_top, 'GALLERY', '活動の様子', alt=True).replace('<section class="alt">', '<section id="gallery" class="alt">', 1)
index += sec(contact_box + hub_new, 'CONTACT', '連絡先・リンク',
             deco='  <img class="nature bl" src="assets/nature/sprout.webp" alt="">\n').replace('<section>', '<section id="contact">', 1)
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
// 現在のテーマタブを見える位置へ
(function(){ var on=document.querySelector('.theme-tabs a.on'); if(on) on.scrollIntoView({inline:'center',block:'nearest'}); })();
'''
io.open(os.path.join(ROOT, 'assets', 'site.js'), 'w', encoding='utf-8', newline='\n').write(js)
print('built', [t[0] for t in THEMES])
