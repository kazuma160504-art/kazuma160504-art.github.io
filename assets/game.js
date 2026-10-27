// もりぞうクエスト: ゲームで振り返る 森一真のあゆみ(横スクロールのジャンプゲーム)
(function () {
  'use strict';
  var root = document.getElementById('game');
  if (!root) return;

  var EMOJI_FONT = '"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';
  var TEXT_FONT = '"Zen Kaku Gothic New","Noto Sans JP",sans-serif';

  // 年ごとのステージ。items は思い出アイテム(e: 絵文字, d: 時期, t: 見出し, x: ひとこと, u: くわしいページ)
  var STAGES = [
    { year: '〜2021', title: '修行の日々', outfit: 'dogi',
      sky: ['#a9dbff', '#e9f7ff'], hill: '#a6d68f', tree: '#5fae4e', grass: '#7cc35f', ground: '#c9a46c', sun: '#ffd84d',
      obs: [['🪵', '丸太'], ['🪨', '岩']],
      items: [
        { e: '🥋', d: '高校時代', t: '少林寺拳法 初段', x: '武道で心と体をきたえる日々。', u: 'hobbies.html' },
        { e: '🗾', d: '高校1年', t: '少林寺拳法の全国大会に出場', x: 'ひとりで演じる「規定単独演武」で、全国の舞台へ。', u: 'awards.html' },
        { e: '👥', d: '高校2年', t: 'ふたたび全国大会へ', x: '「自由組演武」と「団体演武」で、仲間と全国大会に出場。', u: 'awards.html' },
        { e: '🏅', d: '2021.12', t: '関東高等学校少林寺拳法選抜大会 入賞', x: '男子団体演武 4位、男子自由組演武 8位(ALSOKぐんま武道館)。', u: 'awards.html' },
        { e: '🎐', d: '趣味', t: '詩吟 1級・雅号「真水」', x: '声を出して吟じる、日本の伝統芸能。', u: 'hobbies.html' }
      ] },
    { year: '2023', title: '佐賀で医学生に', outfit: 'coat',
      sky: ['#9fd4ff', '#f1fbff'], hill: '#98cf7f', tree: '#4f9f45', grass: '#74bd57', ground: '#c4a06a', sun: '#ffd84d',
      obs: [['📚', '教科書の山'], ['🧪', '実習レポート']],
      items: [
        { e: '🩺', d: 'START', t: '佐賀大学 医学部医学科で学ぶ', x: '医学生としての毎日がスタート。', u: 'profile.html' },
        { e: '🌱', d: 'R5', t: '地域みらい創生プロジェクト', x: '高齢者単独世帯の孤独死・突然死を防ぐシステムづくりに挑戦。', u: 'research.html' },
        { e: '☕', d: '2023.10', t: '団地のサロンへ毎月通いはじめる', x: '研究チームとして、毎月のサロン参加をスタート。', u: 'research.html' }
      ] },
    { year: '2024', title: '全国へ飛び出す', outfit: 'coat', snow: true,
      sky: ['#b7d3ee', '#f5f9ff'], hill: '#e4edf6', tree: '#cfe0d6', grass: '#e9f1f8', ground: '#b9c6d3', sun: '#fff2b3',
      obs: [['⛄', '雪だるま'], ['📚', '教科書の山']],
      items: [
        { e: '💉', d: '2024.01', t: 'Vcan 中高ツアー(山形県南陽市)', x: '中学校・高校で、子宮頸がんとHPVワクチンの出張授業。7月にも登壇。', u: 'education.html' },
        { e: '📰', d: '2024.08', t: '「市報なんよう」で特集される', x: '山形県南陽市の広報誌で、Vcanの講師として紹介。', u: 'media.html' },
        { e: '🗺️', d: '2024.09', t: '佐賀大学 地域連携紹介マップに掲載', x: '押しボタンプロジェクトが大学の地域連携マップに。', u: 'media.html' },
        { e: '🎤', d: '2024.10', t: '第83回 日本公衆衛生学会総会(北海道)', x: '筆頭演者として口演発表。押しボタンPJのポスター発表も。', u: 'publications.html' },
        { e: '📘', d: 'KINDLE', t: 'エッセイ集を Kindle で出版', x: '『ぼんやり、いいじゃない:なんでもない日の処方箋』', u: 'creative.html' }
      ] },
    { year: '2025', title: '地域とともに', outfit: 'coat',
      sky: ['#8fd0f5', '#fff6df'], hill: '#9dd07f', tree: '#4c9a44', grass: '#78c05a', ground: '#c7a26b', sun: '#ffc93c',
      obs: [['⏰', '締切'], ['📝', 'レポート'], ['🚧', '工事中']],
      items: [
        { e: '📺', d: '2025.03', t: 'サガテレビで放映', x: '地域での見守りの活動がテレビで紹介された。', u: 'media.html' },
        { e: '💪', d: '2025.03', t: '強みは「活発性・ポジティブ・個別化」', x: 'ストレングスファインダーで分かった、まずやってみる力。(ハート回復)', u: 'profile.html#strengths', power: true },
        { e: '✍️', d: '2025.04', t: 'note でエッセイを書きはじめる', x: '「フットワーク軽いヤツと思われたら勝ち」など、全11記事。', u: 'creative.html' },
        { e: '🎪', d: '2025.05', t: 'SCS は総勢27名に', x: '代表として、団地のサロン・子どもの居場所・夏祭りの健康ブースへ。', u: 'scs.html' },
        { e: '🏫', d: '2025.06', t: '西与賀小学校で授業', x: '「自分を大切にしよう」をテーマに、2クラス約65人へ。翌年もふたたび。', u: 'education.html' },
        { e: '✂️', d: 'ART', t: '切り絵を佐賀大学美術館で展示', x: '歌舞伎十八番「毛抜」を、一枚の黒い紙から。', u: 'hobbies.html' },
        { e: '🏀', d: 'DAO', t: '佐賀バルーナーズDAO モデレーター', x: 'ファンコミュニティの運営で、感謝状をいただく。', u: 'community.html' },
        { e: '🪧', d: '2025.10', t: '第84回 日本公衆衛生学会総会(静岡)', x: '押しボタンプロジェクトをポスター発表。', u: 'publications.html' },
        { e: '🤝', d: '2025.12', t: '永和システムマネジメントと協議', x: '新型ボタンの共同開発に向けて動き出す。', u: 'research.html' }
      ] },
    { year: '2026', title: 'ひろがる輪', outfit: 'coat',
      sky: ['#8c9de6', '#ffd6c9'], hill: '#8fc27a', tree: '#3f8c3f', grass: '#6db552', ground: '#bf9a63', sun: '#ffb74d',
      obs: [['💻', 'CBT'], ['📑', '抄録の締切'], ['⏰', '締切']],
      items: [
        { e: '📊', d: '2026.01', t: '日本疫学会学術総会(長崎)に参加', x: '国際疫学会 西太平洋地域との合同学術集会。', u: 'publications.html' },
        { e: '🏆', d: '2026.02', t: '国際ソロプチミスト佐賀有明より表彰', x: 'SCSの地域活動が評価され、佐賀新聞でも紹介。', u: 'awards.html' },
        { e: '📣', d: '2026.03', t: '佐賀大学が公式プレスリリース', x: '押しボタンプロジェクトを大学として発表。TSUNAGIコンベンションでも展示。', u: 'research.html' },
        { e: '🔘', d: '2026.04', t: '「いろどり+ボタン」実証実験スタート', x: '新型ボタン30台で、見守りが進化。', u: 'research.html' },
        { e: '📻', d: '2026.05', t: 'えびすFMのラジオパーソナリティに', x: '「バルーナーズDAOおとなりさんラジオ」で、バスケと地域の話題を。', u: 'community.html' },
        { e: '🚨', d: '2026.06', t: '災害時の安否確認訓練', x: '城北団地で、見守りボタンを使った訓練を6月・7月に実施。', u: 'research.html' },
        { e: '💰', d: '2026.07', t: '佐賀県CSO"志"支援金に採択', x: 'SCSの活動に助成金をいただく。', u: 'awards.html' },
        { e: '🏛️', d: '2026.07', t: '佐賀県庁で「いろどり+ボタン」を提案', x: '市町の行政向けに新型ボタンを紹介。', u: 'research.html' },
        { e: '📄', d: '2026.08', t: '共著論文が Am J Cardiol に掲載', x: '脂肪肝(MASLD)と心血管リスク予測式の国際共同研究。', u: 'publications.html' },
        { e: '🔬', d: 'NOW', t: '5つの分野で研究中', x: '心臓血管外科・感染症・肝臓・公衆衛生・救急で、それぞれの研究に取り組む。', u: 'publications.html' }
      ] }
  ];
  var GOAL = { e: '🎤', d: '2026.10', t: '第85回 日本公衆衛生学会総会(東京)', x: '筆頭演者として、押しボタンを使った災害時の安否確認訓練を口演発表。' };
  var TOTAL = 0;
  STAGES.forEach(function (s) { TOTAL += s.items.length; });

  var cv = root.querySelector('canvas'), ctx = cv.getContext('2d');
  function $(id) { return document.getElementById(id); }
  var elHearts = $('gm-hearts'), elStage = $('gm-stage'), elCount = $('gm-count'), elToast = $('gm-toast'),
      elStart = $('gm-start'), modal = $('gm-modal'), card = $('gm-card');

  // 論理座標: 高さ 400 固定、幅は画面の比率に合わせる
  var H = 400, GROUND = 340, W = 640, scale = 1, dpr = 1;
  var GRAV = 2300, JUMP1 = 780, JUMP2 = 700, MAXH = 5;
  var LEVELS = [40, 120, 215]; // 思い出アイテムの高さ(地面 / 1段ジャンプ / 2段ジャンプ)

  var state = 'title', stage = 0, got = {}, hearts = 3;
  var px = 0, py = 0, vy = 0, jumps = 0, inv = 0, t = 0, stageT = 0, speed = 250;
  var items = [], obs = [], extras = [], stageEnd = 0, parts = [], floats = [];
  var last = 0, raf = 0, toastTimer = 0;

  var BALLOONS = [], BCOL = ['#e74c3c', '#f39c12', '#3c9a3f', '#2f7fc1', '#9b59b6', '#f06292'];
  for (var i = 0; i < 7; i++) BALLOONS.push({ x: i * 190 + (i * 71) % 90, y: 46 + (i * 47) % 120, r: 13 + (i * 5) % 10, c: BCOL[i % BCOL.length], p: i * 1.7 });
  var SNOW = [];
  for (i = 0; i < 46; i++) SNOW.push({ x: (i * 97) % 1400, y: (i * 53) % H, s: 1.4 + (i % 3), v: 26 + (i % 5) * 9 });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function best() { try { return +localStorage.getItem('morizo-best') || 0; } catch (e) { return 0; } }
  function saveBest(n) { try { if (n > best()) localStorage.setItem('morizo-best', String(n)); } catch (e) {} }
  function countGot() { var n = 0; for (var k in got) if (got[k]) n++; return n; }

  // ---- ステージの組み立て
  function build(s) {
    var st = STAGES[s], sp = 560 + s * 30, x = 620;
    items = []; obs = []; extras = [];
    st.items.forEach(function (it, i) {
      var lv = s === 0 ? [40, 120, 120][i % 3] : LEVELS[(i + s) % 3];
      items.push({ id: s + '-' + i, it: it, x: x, h: lv, got: false });
      var o = st.obs[(i + s) % st.obs.length], n = (s >= 1 && (i + s) % 3 === 2) ? 2 : 1;
      var ox = x + sp * 0.5 + ((i * 37 + s * 13) % 5 - 2) * 16;
      obs.push({ x: ox, w: 26, h: n * 30, n: n, e: o[0], name: o[1] });
      if (s >= 2 && i % 3 === 1) obs.push({ x: ox + 120, w: 26, h: 30, n: 1, e: o[0], name: o[1] });
      if (s >= 2 && i === 2) extras.push({ x: x + 110, h: 110, got: false });
      x += sp;
    });
    stageEnd = x + 80;
  }

  function startStage(s) {
    stage = s; build(s);
    px = 0; py = 0; vy = 0; jumps = 0; inv = 0; stageT = 0; parts = []; floats = [];
    speed = 250 + s * 40;
    hud();
  }

  function newGame() { got = {}; hearts = 3; startStage(0); }

  // ---- 入力
  function jump() {
    if (jumps >= 2) return;
    vy = jumps ? JUMP2 : JUMP1; jumps++;
    if (py <= 0) py = 0.01;
  }

  // ---- 判定
  function hitCircle(cx, cy, r, L, R, B, T) {
    var nx = Math.max(L, Math.min(cx, R)), ny = Math.max(B, Math.min(cy, T)), dx = cx - nx, dy = cy - ny;
    return dx * dx + dy * dy < r * r;
  }

  function burst(x, h, col) {
    for (var k = 0; k < 14; k++) {
      var a = k / 14 * Math.PI * 2, v = 120 + (k % 4) * 40;
      parts.push({ x: x, h: h, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 0.7, c: col[k % col.length] });
    }
  }

  function collect(o) {
    burst(o.x, o.h, ['#ffd54f', '#3c9a3f', '#8cc63f', '#ffffff']);
    toast(o.it.e + ' ' + o.it.d + ' ' + o.it.t);
    if (o.it.power) heal('ポジティブ! ❤+1', o.x, o.h + 30);
    hud();
  }

  function heal(txt, x, h) {
    hearts = Math.min(MAXH, hearts + 1);
    floats.push({ x: x, h: h, txt: txt, c: '#d81b60', life: 1.2 });
    hud();
  }

  function hurt(o) {
    hearts--; inv = 1.2;
    floats.push({ follow: true, h: py + 80, txt: o.name + '!', c: '#e53935', life: 1 });
    try { if (navigator.vibrate) navigator.vibrate(60); } catch (e) {}
    hud();
    if (hearts <= 0) gameOver();
  }

  function update(dt) {
    t += dt; stageT += dt;
    px += speed * (1 + Math.min(px / stageEnd, 1) * 0.12) * dt;
    if (py > 0 || vy > 0) {
      vy -= GRAV * dt; py += vy * dt;
      if (py <= 0) { py = 0; vy = 0; jumps = 0; }
    }
    if (inv > 0) inv -= dt;
    var L = px - 11, R = px + 11, B = py, T = py + 56;
    items.forEach(function (o) {
      if (!o.got && hitCircle(o.x, o.h, 20, L, R, B, T)) { o.got = true; got[o.id] = true; collect(o); }
    });
    extras.forEach(function (o) {
      if (!o.got && hitCircle(o.x, o.h, 18, L, R, B, T)) { o.got = true; burst(o.x, o.h, ['#f06292', '#ffffff']); heal('ポジティブ! ❤+1', o.x, o.h + 30); }
    });
    if (inv <= 0) {
      for (var k = 0; k < obs.length && state === 'run'; k++) {
        var o = obs[k];
        if (!o.hit && R - 3 > o.x && L + 3 < o.x + o.w && B + 2 < o.h) { o.hit = true; hurt(o); }
      }
    }
    parts = parts.filter(function (p) { p.life -= dt; p.x += p.vx * dt; p.h += p.vy * dt; p.vy -= 260 * dt; return p.life > 0; });
    floats = floats.filter(function (f) { f.life -= dt; f.h += 40 * dt; return f.life > 0; });
    if (state === 'run' && px > stageEnd) finishStage();
  }

  // ---- 描画
  function circle(x, y, r) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); }
  function rr(x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function emoji(ch, x, y, size) { ctx.font = size + 'px ' + EMOJI_FONT; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#000'; ctx.fillText(ch, x, y); }
  function label(txt, x, y, size, color) {
    ctx.font = '700 ' + size + 'px ' + TEXT_FONT; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.lineJoin = 'round'; ctx.lineWidth = Math.max(3, size / 4); ctx.strokeStyle = 'rgba(255,255,255,.92)';
    ctx.strokeText(txt, x, y); ctx.fillStyle = color; ctx.fillText(txt, x, y);
  }

  function balloon(x, y, r, c) {
    ctx.fillStyle = c; ctx.beginPath(); ctx.ellipse(x, y, r, r * 1.15, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); ctx.ellipse(x - r * 0.35, y - r * 0.3, r * 0.25, r * 0.45, -0.3, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(80,60,40,.55)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x - r * 0.5, y + r * 0.95); ctx.lineTo(x - r * 0.25, y + r * 1.55); ctx.moveTo(x + r * 0.5, y + r * 0.95); ctx.lineTo(x + r * 0.25, y + r * 1.55); ctx.stroke();
    ctx.fillStyle = '#8d6e63'; ctx.fillRect(x - r * 0.28, y + r * 1.5, r * 0.56, r * 0.4);
  }

  function scenery(x, k, st) {
    var m = ((k % 5) + 5) % 5;
    if (m === 0) { // 団地
      ctx.fillStyle = st.snow ? '#eef3f8' : '#f3ead6'; ctx.fillRect(x - 30, GROUND - 74, 60, 74);
      ctx.fillStyle = st.snow ? '#9fb3c8' : '#b9a27a';
      for (var r = 0; r < 4; r++) for (var c = 0; c < 3; c++) ctx.fillRect(x - 22 + c * 17, GROUND - 66 + r * 17, 10, 9);
      if (st.snow) { ctx.fillStyle = '#ffffff'; ctx.fillRect(x - 32, GROUND - 78, 64, 6); }
    } else if (m === 2) { // 家
      ctx.fillStyle = '#fff3e0'; ctx.fillRect(x - 18, GROUND - 30, 36, 30);
      ctx.fillStyle = st.snow ? '#ffffff' : '#c0504d';
      ctx.beginPath(); ctx.moveTo(x - 24, GROUND - 28); ctx.lineTo(x, GROUND - 48); ctx.lineTo(x + 24, GROUND - 28); ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#8d6e63'; ctx.fillRect(x - 5, GROUND - 16, 10, 16);
    } else { // 木
      var h = 40 + ((k * 17) % 30 + 30) % 30;
      ctx.fillStyle = '#8d6e63'; ctx.fillRect(x - 3, GROUND - h * 0.45, 6, h * 0.45);
      ctx.fillStyle = st.tree; circle(x, GROUND - h * 0.62, h * 0.32); circle(x - h * 0.2, GROUND - h * 0.46, h * 0.22); circle(x + h * 0.2, GROUND - h * 0.46, h * 0.22);
    }
  }

  function sign(x, a, b) {
    if (x < -120 || x > W + 120) return;
    ctx.fillStyle = '#8d6e63'; ctx.fillRect(x - 3, GROUND - 58, 6, 58);
    ctx.fillStyle = '#fff8e1'; rr(x - 62, GROUND - 98, 124, 46, 8); ctx.fill();
    ctx.strokeStyle = '#8d6e63'; ctx.lineWidth = 2; ctx.stroke();
    label(a, x, GROUND - 84, 16, '#3c9a3f'); label(b, x, GROUND - 64, 12, '#1e3322');
  }

  function flag(x, txt) {
    if (x < -80 || x > W + 80) return;
    ctx.fillStyle = '#6d4c41'; ctx.fillRect(x - 2, GROUND - 96, 4, 96);
    ctx.fillStyle = '#3c9a3f'; ctx.beginPath(); ctx.moveTo(x + 2, GROUND - 96); ctx.lineTo(x + 58, GROUND - 82); ctx.lineTo(x + 2, GROUND - 68); ctx.closePath(); ctx.fill();
    label(txt, x + 26, GROUND - 82, 11, '#1e3322');
  }

  function goal(x) {
    if (x < -120 || x > W + 120) return;
    ctx.fillStyle = '#ffffff'; rr(x - 72, GROUND - 64, 144, 64, 10); ctx.fill();
    ctx.strokeStyle = '#3c9a3f'; ctx.lineWidth = 3; ctx.stroke();
    label('GOAL', x, GROUND - 46, 18, '#3c9a3f');
    label('第85回 公衆衛生学会', x, GROUND - 22, 11, '#1e3322');
    emoji(GOAL.e, x, GROUND - 96 + Math.sin(t * 3) * 4, 40);
  }

  function orb(x, y, e, ring) {
    ctx.fillStyle = 'rgba(255,255,255,.35)'; circle(x, y, 26);
    ctx.fillStyle = 'rgba(255,255,255,.95)'; circle(x, y, 20);
    ctx.strokeStyle = ring; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(x, y, 20, 0, Math.PI * 2); ctx.stroke();
    emoji(e, x, y + 1, 23);
  }

  function player(x, y) {
    if (inv > 0 && Math.floor(t * 14) % 2) return;
    var air = py > 0, sw = air ? 0 : Math.sin(px * 0.07), dogi = STAGES[stage].outfit === 'dogi';
    var la = air ? -8 : 0, ra = air ? -10 : 0;
    ctx.lineCap = 'round';
    // 脚
    ctx.strokeStyle = dogi ? '#eceff1' : '#33415c'; ctx.lineWidth = 6; ctx.beginPath();
    if (air) { ctx.moveTo(x - 4, y - 16); ctx.lineTo(x - 9, y - 6); ctx.moveTo(x + 4, y - 16); ctx.lineTo(x + 9, y - 9); }
    else { ctx.moveTo(x - 3, y - 16); ctx.lineTo(x - 3 + sw * 7, y - 2); ctx.moveTo(x + 3, y - 16); ctx.lineTo(x + 3 - sw * 7, y - 2); }
    ctx.stroke();
    // 腕(輪郭つき)
    ctx.strokeStyle = '#b0bec5'; ctx.lineWidth = 7; ctx.beginPath();
    ctx.moveTo(x - 9, y - 34); ctx.lineTo(x - 13 - sw * 4, y - 22 + la); ctx.moveTo(x + 9, y - 34); ctx.lineTo(x + 14 + sw * 4, y - 23 + ra); ctx.stroke();
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 4.5; ctx.stroke();
    ctx.fillStyle = '#f6d2b0'; circle(x - 13 - sw * 4, y - 21 + la, 2.8); circle(x + 14 + sw * 4, y - 22 + ra, 2.8);
    // 体: 高校までは道着、大学からは白衣
    ctx.fillStyle = '#ffffff'; rr(x - 11, y - 38, 22, 25, 6); ctx.fill();
    ctx.strokeStyle = '#b0bec5'; ctx.lineWidth = 1.5; ctx.stroke();
    if (dogi) {
      ctx.beginPath(); ctx.moveTo(x - 6, y - 38); ctx.lineTo(x + 3, y - 25); ctx.moveTo(x + 6, y - 38); ctx.lineTo(x, y - 30); ctx.stroke();
      ctx.fillStyle = '#212121'; ctx.fillRect(x - 11, y - 21, 22, 4); ctx.fillRect(x + 4, y - 19, 3, 7);
    } else {
      ctx.fillStyle = '#3c9a3f'; ctx.beginPath(); ctx.moveTo(x - 5, y - 38); ctx.lineTo(x + 5, y - 38); ctx.lineTo(x, y - 29); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = '#2f7fc1'; ctx.lineWidth = 1.8; ctx.beginPath(); ctx.arc(x + 1, y - 32, 6, 0.2, Math.PI - 0.2); ctx.stroke();
      ctx.fillStyle = '#2f7fc1'; circle(x + 1, y - 25, 2);
    }
    // 頭
    ctx.fillStyle = '#f6d2b0'; circle(x + 1, y - 49, 11);
    ctx.fillStyle = '#2b2b2b'; ctx.beginPath(); ctx.arc(x + 1, y - 50, 11.6, Math.PI * 1.02, Math.PI * 1.98); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x - 10, y - 51); ctx.quadraticCurveTo(x - 3, y - 46, x + 5, y - 53); ctx.lineTo(x + 2, y - 60); ctx.lineTo(x - 8, y - 58); ctx.closePath(); ctx.fill();
    circle(x + 5, y - 48, 1.6); circle(x + 9.5, y - 48, 1.6);
    ctx.strokeStyle = '#b5543c'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.arc(x + 7.5, y - 44.5, 3, 0.15 * Math.PI, 0.85 * Math.PI); ctx.stroke();
    ctx.fillStyle = 'rgba(240,120,120,.45)'; circle(x + 11, y - 45, 2);
  }

  function draw() {
    var st = STAGES[stage], cam = px - W * 0.22, k;
    ctx.setTransform(scale * dpr, 0, 0, scale * dpr, 0, 0);
    var g = ctx.createLinearGradient(0, 0, 0, GROUND);
    g.addColorStop(0, st.sky[0]); g.addColorStop(1, st.sky[1]);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = st.sun; circle(W - 80, 66, 26);
    // 佐賀の空にはバルーン
    var span = W + 240;
    BALLOONS.forEach(function (b) { balloon(((b.x - cam * 0.12) % span + span) % span - 120, b.y + Math.sin(t * 0.8 + b.p) * 6, b.r, b.c); });
    ctx.fillStyle = st.hill; ctx.beginPath(); ctx.moveTo(0, GROUND);
    for (var x = 0; x <= W + 16; x += 16) { var wx = x + cam * 0.3; ctx.lineTo(x, GROUND - 56 - Math.sin(wx * 0.006) * 26 - Math.sin(wx * 0.017) * 9); }
    ctx.lineTo(W + 16, GROUND); ctx.closePath(); ctx.fill();
    var off = cam * 0.6;
    for (k = Math.floor(off / 150) - 1; k * 150 - off < W + 80; k++) scenery(k * 150 - off + ((k * 53) % 60 + 60) % 60, k, st);
    ctx.fillStyle = st.ground; ctx.fillRect(0, GROUND, W, H - GROUND);
    ctx.fillStyle = st.grass; ctx.fillRect(0, GROUND, W, 9);
    ctx.fillStyle = 'rgba(0,0,0,.07)';
    for (k = Math.floor(cam / 64); k * 64 - cam < W; k++) ctx.fillRect(k * 64 - cam, GROUND + 22 + (Math.abs(k) % 2) * 14, 24, 4);
    if (st.snow) {
      ctx.fillStyle = 'rgba(255,255,255,.9)';
      SNOW.forEach(function (s) { circle((((s.x - cam * 0.2) % W) + W) % W, (s.y + t * s.v) % GROUND, s.s); });
    }
    sign(230 - cam, st.year, st.title);
    if (stage === STAGES.length - 1) goal(stageEnd - cam); else flag(stageEnd - cam, '▶ ' + STAGES[stage + 1].year);
    obs.forEach(function (o) {
      var ox = o.x - cam; if (ox < -50 || ox > W + 50) return;
      for (var j = 0; j < o.n; j++) emoji(o.e, ox + o.w / 2, GROUND - 15 - j * 30, 30);
    });
    items.forEach(function (o, i) {
      if (o.got) return;
      var ix = o.x - cam; if (ix < -60 || ix > W + 60) return;
      var iy = GROUND - o.h + Math.sin(t * 3 + i) * 4;
      orb(ix, iy, o.it.e, '#3c9a3f'); label(o.it.d, ix, iy - 31, 11, '#1e3322');
    });
    extras.forEach(function (o) {
      if (o.got) return;
      var ex = o.x - cam; if (ex < -60 || ex > W + 60) return;
      orb(ex, GROUND - o.h + Math.sin(t * 4) * 4, '💖', '#e91e63');
    });
    player(W * 0.22, GROUND - py);
    parts.forEach(function (p) { ctx.globalAlpha = Math.max(0, p.life / 0.7); ctx.fillStyle = p.c; circle(p.x - cam, GROUND - p.h, 3); });
    floats.forEach(function (f) { ctx.globalAlpha = Math.min(1, f.life); label(f.txt, f.follow ? W * 0.22 : f.x - cam, GROUND - f.h, 15, f.c); });
    ctx.globalAlpha = 1;
    if (state === 'run' && stageT < 2.2) {
      ctx.globalAlpha = Math.min(1, (2.2 - stageT) / 0.6);
      label(st.year, W / 2, H * 0.3, 44, '#3c9a3f'); label(st.title, W / 2, H * 0.3 + 38, 20, '#1e3322');
      ctx.globalAlpha = 1;
    }
  }

  // ---- 画面表示
  function hud() {
    var s = '';
    for (var k = 0; k < hearts; k++) s += '❤️';
    elHearts.textContent = s || '💔';
    elStage.textContent = STAGES[stage].year + ' ' + STAGES[stage].title;
    elCount.textContent = '🎁 ' + countGot() + '/' + TOTAL;
  }

  function toast(msg) {
    elToast.textContent = msg; elToast.classList.add('on');
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { elToast.classList.remove('on'); }, 2600);
  }

  function showStart(mode) {
    var b = best();
    elStart.innerHTML = mode === 'pause'
      ? '<h2>ひと休み中</h2><p class="gm-best">準備ができたら再開しよう</p><button class="btn btn-primary" type="button" data-act="resume">▶ つづける</button>'
      : '<p class="gm-kicker">ゲームで振り返る 森一真のあゆみ</p><h2>もりぞうクエスト</h2><button class="btn btn-primary" type="button" data-act="start">▶ スタート</button>' +
        '<p class="gm-best">' + (b ? 'ベスト記録: 思い出 ' + b + ' / ' + TOTAL + ' 個' : 'タップ / スペースでジャンプ(空中でもう1回)') + '</p>';
    elStart.hidden = false; root.classList.add('idle');
  }

  function li(it, ok) {
    if (!ok) return '<li class="miss"><span class="e">❔</span><div><time>' + esc(it.d) + '</time><b>？？？</b><p>見のがした思い出。もう一度あそぶと見つかるかも。</p></div></li>';
    return '<li><span class="e">' + it.e + '</span><div><time>' + esc(it.d) + '</time><b>' + esc(it.t) + '</b><p>' + esc(it.x) + '</p>' +
      '<a href="' + it.u + '" target="_blank" rel="noopener">くわしく見る →</a></div></li>';
  }

  function openModal(html) {
    card.innerHTML = html; modal.hidden = false; card.scrollTop = 0;
    var b = card.querySelector('button');
    if (b) { try { b.focus({ preventScroll: true }); } catch (e) { b.focus(); } }
  }
  function closeModal() { modal.hidden = true; }

  function finishStage() {
    state = 'card'; root.classList.remove('running');
    if (stage === STAGES.length - 1) { ending(); return; }
    var st = STAGES[stage], nx = STAGES[stage + 1], n = 0;
    var list = st.items.map(function (it, k) { var ok = !!got[stage + '-' + k]; if (ok) n++; return li(it, ok); }).join('');
    openModal('<p class="gm-kicker">' + esc(st.year) + ' CLEAR!</p><h2>' + esc(st.title) + '</h2>' +
      '<p class="gm-sub">この時代の思い出 <b>' + n + ' / ' + st.items.length + '</b> 個</p><ul class="gm-list">' + list + '</ul>' +
      '<div class="gm-btns sticky"><button class="btn btn-primary" type="button" data-act="next">' + esc(nx.year) + '「' + esc(nx.title) + '」へ ▶</button></div>');
  }

  function gameOver() {
    state = 'card'; root.classList.remove('running');
    openModal('<p class="gm-kicker">GAME OVER</p><h2>ちょっとひと休み…</h2>' +
      '<p class="gm-sub">でも「まずやってみる」(活発性)が森一真の持ち味。<br>' + esc(STAGES[stage].year) + ' の最初から、もう一度!</p>' +
      '<div class="gm-btns"><button class="btn btn-primary" type="button" data-act="retry">もう一度チャレンジ ▶</button></div>');
  }

  function ending() {
    var n = countGot(); saveBest(n);
    var rank = n === TOTAL ? '🌟 伝説のもりぞう(コンプリート!)' : n >= TOTAL * 0.8 ? '🩺 地域をつなぐ医学生' : n >= TOTAL * 0.5 ? '🔘 見守りボタンの研究員' : '🌱 まずやってみる活発性';
    var album = STAGES.map(function (st, s) {
      return '<h3>' + esc(st.year) + ' ' + esc(st.title) + '</h3><ul class="gm-list">' +
        st.items.map(function (it, k) { return li(it, !!got[s + '-' + k]); }).join('') + '</ul>';
    }).join('');
    openModal('<p class="gm-kicker">GOAL!</p><h2>' + GOAL.e + ' ' + esc(GOAL.t) + '</h2>' +
      '<p class="gm-sub">' + esc(GOAL.d) + ' ／ ' + esc(GOAL.x) + '<br>森一真のあゆみは、まだまだ続く…!</p>' +
      '<div class="gm-score"><span>集めた思い出</span><b>' + n + '</b><small>/ ' + TOTAL + ' 個</small></div>' +
      '<p class="gm-rank">称号: ' + rank + '</p>' +
      '<div class="gm-btns"><button class="btn btn-primary" type="button" data-act="again">もう一度あそぶ</button>' +
      '<button class="btn btn-ghost" type="button" data-act="share">Xでシェア</button><a class="btn btn-ghost" href="index.html">サイトを見る</a></div>' +
      '<h3 class="gm-album">思い出アルバム</h3>' + album);
  }

  function share() {
    var text = 'もりぞうクエストで森一真のあゆみを振り返ったよ! 思い出 ' + countGot() + '/' + TOTAL + ' 個 #もりぞうクエスト';
    window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent(location.href.split('#')[0]), '_blank', 'noopener');
  }

  // ---- ループ
  function frame(ts) {
    raf = 0;
    if (state !== 'run') return;
    var dt = last ? Math.min((ts - last) / 1000, 1 / 30) : 0;
    last = ts;
    update(dt); draw();
    if (state === 'run') raf = requestAnimationFrame(frame);
  }
  function run() {
    state = 'run'; last = 0; elStart.hidden = true; root.classList.remove('idle'); root.classList.add('running');
    if (!raf) raf = requestAnimationFrame(frame);
  }
  function pause() {
    if (state !== 'run') return;
    state = 'pause'; root.classList.remove('running'); showStart('pause');
  }

  function act(a) {
    if (a === 'start' || a === 'again') {
      closeModal(); newGame(); run();
      toast('タップ / スペースでジャンプ! 空中でもう1回ジャンプできるよ');
      if (root.getBoundingClientRect().top < 0) root.scrollIntoView({ block: 'center', behavior: 'smooth' });
    } else if (a === 'resume') run();
    else if (a === 'next') { closeModal(); startStage(stage + 1); run(); }
    else if (a === 'retry') {
      STAGES[stage].items.forEach(function (_, k) { delete got[stage + '-' + k]; });
      hearts = 3; closeModal(); startStage(stage); run();
    } else if (a === 'share') share();
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-act]');
    if (b && (root.contains(b) || modal.contains(b))) act(b.getAttribute('data-act'));
  });
  $('gm-pause').addEventListener('click', pause);
  root.addEventListener('pointerdown', function (e) {
    if (state !== 'run' || (e.target.closest && e.target.closest('button'))) return;
    e.preventDefault(); jump();
  });
  document.addEventListener('keydown', function (e) {
    if (state !== 'run') return;
    if (e.code === 'Space' || e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') { e.preventDefault(); if (!e.repeat) jump(); }
    else if (e.key === 'Escape' || e.key === 'p' || e.key === 'P') pause();
  });
  document.addEventListener('visibilitychange', function () { if (document.hidden) pause(); });
  var rt = 0;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(resize, 120); });

  function resize() {
    var bw = root.clientWidth || 640;
    var bh = bw < 700 ? bw / 1.6 : Math.min(bw / 2.2, window.innerHeight * 0.7);
    bh = Math.max(220, Math.round(bh));
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(bw * dpr); cv.height = Math.round(bh * dpr);
    cv.style.width = bw + 'px'; cv.style.height = bh + 'px';
    scale = bh / H; W = bw / scale;
    draw();
  }

  startStage(0);
  showStart('title');
  resize();
  // 日本語フォントの読み込み後に描き直す
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (state !== 'run') draw(); });
})();
