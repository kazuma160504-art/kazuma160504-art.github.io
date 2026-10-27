// 共通スクリプト: メニュー・スクロールフェード・写真の拡大表示
// スマホ用メニューの開閉
(function(){
  var btn=document.querySelector('.menu-btn'), menu=document.getElementById('menu'); if(!btn||!menu) return;
  function set(open){ menu.hidden=!open; btn.setAttribute('aria-expanded', open); }
  btn.addEventListener('click',function(e){ e.stopPropagation(); set(menu.hidden); });
  menu.addEventListener('click',function(e){ if(e.target.closest('a')) set(false); });
  document.addEventListener('click',function(e){ if(!menu.hidden && !menu.contains(e.target)) set(false); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape' && !menu.hidden){ set(false); btn.focus(); } });
})();
(function(){
  var els = document.querySelectorAll('.fade');
  if(!('IntersectionObserver' in window)){ els.forEach(function(el){ el.classList.add('show'); }); return; }
  // threshold は 0(少しでも画面に入ったら表示)。割合で判定すると、画面より縦に長い要素(ギャラリー等)が表示されないことがある
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('show'); io.unobserve(e.target); } });
  }, {threshold:0, rootMargin:'0px 0px -40px 0px'});
  els.forEach(function(el){ io.observe(el); });
})();
(function(){
  var lb=document.getElementById('lightbox'); if(!lb) return; var im=lb.querySelector('img'), cap=lb.querySelector('figcaption');
  document.querySelectorAll('.gallery img,.photo-row img,.org-img,.art-frame img,.org-posters img').forEach(function(el){
    el.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();im.src=el.src;im.alt=el.alt;
      var fc=el.closest('figure')&&el.closest('figure').querySelector('figcaption'); cap.textContent=fc?fc.textContent:el.alt;
      lb.classList.add('open');});
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
// 長いページの上に「このページ」の目次
(function(){
  var tabs = document.querySelector('.theme-tabs'); if (!tabs) return;
  var heads = [].slice.call(document.querySelectorAll('section h2.sec-title'));
  if (heads.length < 3) return;
  var nav = document.createElement('nav'); nav.className = 'page-toc'; nav.setAttribute('aria-label', 'このページの内容');
  var inner = document.createElement('div'); inner.className = 'in';
  var lab = document.createElement('span'); lab.className = 'toc-label'; lab.textContent = 'このページ'; inner.appendChild(lab);
  heads.forEach(function(h, i){
    var sec = h.closest('section'); if (!sec.id) sec.id = 'sec-' + (i + 1);
    var a = document.createElement('a'); a.href = '#' + sec.id; a.textContent = h.textContent; inner.appendChild(a);
  });
  nav.appendChild(inner); tabs.parentNode.insertBefore(nav, tabs.nextSibling);
})();
// カードの絞り込み(教育・発信など)
(function(){
  document.querySelectorAll('.filter-bar').forEach(function(bar){
    var grid = bar.nextElementSibling; if (!grid) return;
    var cards = [].slice.call(grid.children);
    bar.querySelectorAll('button').forEach(function(b){
      var f = b.getAttribute('data-filter');
      var n = f === 'all' ? cards.length : cards.filter(function(c){ return (' ' + (c.getAttribute('data-cat') || '') + ' ').indexOf(' ' + f + ' ') >= 0; }).length;
      var sm = document.createElement('small'); sm.textContent = n; b.appendChild(sm);
      b.addEventListener('click', function(){
        bar.querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        cards.forEach(function(c){
          var show = f === 'all' || (' ' + (c.getAttribute('data-cat') || '') + ' ').indexOf(' ' + f + ' ') >= 0;
          c.style.display = show ? '' : 'none'; if (show) c.classList.add('show');
        });
      });
    });
  });
})();
// もりぞーを探せ: 各ページのどこかに、もりぞーが1人かくれている(見つけたページは端末に記録)
(function(){
  var PAGES = {index:'トップ',profile:'プロフィール',research:'研究:押しボタンPJ',publications:'論文・学会発表',scs:'SCS 地域交流',community:'バルーナーズDAO・ラジオ',education:'教育・発信',awards:'実績・表彰',media:'メディア・掲載',hobbies:'趣味・アート',creative:'動画編集・執筆',gallery:'ギャラリー',contact:'連絡先・SNS',game:'もりぞうクエスト'};
  var key = (location.pathname.split('/').pop() || 'index.html').replace('.html', '') || 'index';
  if (!PAGES[key]) return;
  var KEYS = Object.keys(PAGES), found = {};
  try { found = JSON.parse(localStorage.getItem('morizo-found') || '{}') || {}; } catch (e) {}
  function save(){ try { localStorage.setItem('morizo-found', JSON.stringify(found)); } catch (e) {} }
  function count(){ return KEYS.filter(function(k){ return found[k]; }).length; }
  var SVG = '<svg viewBox="0 0 48 60" aria-hidden="true"><path d="M13 37 L8 47" stroke="#b0bec5" stroke-width="6" stroke-linecap="round"/><path d="M13 37 L8 47" stroke="#fff" stroke-width="4" stroke-linecap="round"/><circle cx="7.6" cy="48" r="2.6" fill="#f6d2b0"/><path d="M35 36 L42 25" stroke="#b0bec5" stroke-width="6" stroke-linecap="round"/><path d="M35 36 L42 25" stroke="#fff" stroke-width="4" stroke-linecap="round"/><circle cx="42.6" cy="23.6" r="2.8" fill="#f6d2b0"/><path d="M19 52 L18 58 M29 52 L30 58" stroke="#33415c" stroke-width="5" stroke-linecap="round"/><rect x="12" y="31" width="24" height="23" rx="7" fill="#fff" stroke="#b0bec5" stroke-width="1.5"/><path d="M20 31 L28 31 L24 39 Z" fill="#3c9a3f"/><path d="M19 37 a5 5 0 0 0 10 0" fill="none" stroke="#2f7fc1" stroke-width="1.6"/><circle cx="24" cy="43" r="1.7" fill="#2f7fc1"/><circle cx="24" cy="18" r="12.5" fill="#f6d2b0"/><path d="M11.5 18 C11 8 18 4.5 25 5 C32 5.5 37 10 36.5 17 C33 12.5 27 11 21 13 C17 14 14 16 11.5 18 Z" fill="#2b2b2b"/><circle cx="19.5" cy="19.5" r="1.7" fill="#2b2b2b"/><circle cx="28.5" cy="19.5" r="1.7" fill="#2b2b2b"/><path d="M20.5 24 Q24 27.5 27.5 24" stroke="#b5543c" stroke-width="1.5" fill="none" stroke-linecap="round"/><circle cx="16.5" cy="23.5" r="2" fill="#f08080" fill-opacity=".45"/><circle cx="31.5" cy="23.5" r="2" fill="#f08080" fill-opacity=".45"/></svg>';
  var cands = [].slice.call(document.querySelectorAll('main .theme, .theme-grid .theme, a.kpi, .org, .mini-card, .award, .rnow, .hobby, .place-group, .chart, .str, .hub-col, .gm-help li, .art-frame, .contact-box, .news, .gallery figure, .pn a'))
    .filter(function(el){ var r = el.getBoundingClientRect(); return r.width > 140 && r.height > 70; });
  if (!cands.length) return;
  var host = cands[Math.floor(Math.random() * cands.length)], cs = getComputedStyle(host);
  if (cs.position === 'static') host.style.position = 'relative';
  var spots = cs.overflow === 'visible' ? ['peek-tr', 'peek-tl', 'in-br'] : ['in-br', 'in-bl', 'in-tr'];
  var m = document.createElement('span');
  m.className = 'morizo ' + spots[Math.floor(Math.random() * spots.length)] + (found[key] ? ' done' : '');
  m.setAttribute('role', 'button'); m.setAttribute('tabindex', '0'); m.setAttribute('aria-label', 'かくれている もりぞー');
  m.innerHTML = SVG; host.appendChild(m);
  var toastEl = null, toastT = 0, badge = null, panel = null;
  function say(msg){
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'hunt-toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function(){ toastEl.classList.remove('on'); }, 2800);
  }
  function list(){
    return (found[key] ? '' : '<button type="button" class="hunt-hintbtn">🔍 このページのヒントを見る</button>') +
      '<p>各ページのどこかに、もりぞーが1人かくれています。見つけたページに ✓ がつきます。</p><ul>' + KEYS.map(function(k){
      return '<li><a href="' + k + '.html"><span>' + PAGES[k] + '</span><span>' + (found[k] ? '✓' : '?') + '</span></a></li>';
    }).join('') + '</ul>';
  }
  function showBadge(){
    if (!badge) {
      badge = document.createElement('button'); badge.type = 'button'; badge.className = 'hunt-badge'; document.body.appendChild(badge);
      panel = document.createElement('div'); panel.className = 'hunt-panel'; panel.hidden = true; document.body.appendChild(panel);
      badge.addEventListener('click', function(){ panel.innerHTML = list(); panel.hidden = !panel.hidden; });
      // ヒント: もりぞーのいる場所までスクロールして、しばらく光らせる
      panel.addEventListener('click', function(e){
        if (!e.target.closest('.hunt-hintbtn')) return;
        panel.hidden = true;
        m.scrollIntoView({ behavior: 'smooth', block: 'center' });
        m.classList.remove('hint'); void m.offsetWidth; m.classList.add('hint');
        setTimeout(function(){ m.classList.remove('hint'); }, 4600);
        say('このあたりに、もりぞーがいるよ!');
      });
    }
    badge.innerHTML = SVG + 'もりぞー ' + count() + '/' + KEYS.length;
    badge.setAttribute('aria-label', 'もりぞーを見つけたページ: ' + count() + '/' + KEYS.length);
  }
  function celebrate(){
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var C = ['#3c9a3f', '#8cc63f', '#ffd54f', '#e07b24', '#2f7fc1', '#f06292'];
    for (var i = 0; i < 60; i++) {
      var c = document.createElement('i'); c.className = 'confetti';
      c.style.left = (Math.random() * 100) + 'vw'; c.style.background = C[i % C.length]; c.style.animationDelay = (Math.random() * 0.8) + 's';
      document.body.appendChild(c); setTimeout(function(el){ el.remove(); }, 3600, c);
    }
  }
  function hit(e){
    e.preventDefault(); e.stopPropagation();
    var first = !found[key]; found[key] = 1; save();
    m.classList.remove('jump'); void m.offsetWidth; m.classList.add('jump', 'done');
    var n = count(), N = KEYS.length;
    say(first ? (n === N ? '🎉 コンプリート! 全ページのもりぞーを見つけました!' : 'もりぞーを見つけた! (' + n + '/' + N + 'ページ)') : 'このページのもりぞーは、もう見つけたよ (' + n + '/' + N + ')');
    showBadge();
    if (first && n === N) celebrate();
  }
  m.addEventListener('click', hit);
  m.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') hit(e); });
  // ゲームのページでは、遊ぶじゃまにならないよう、見つけるまではボタンを出さない
  if (key !== 'game' || count() > 0) showBadge();
})();
// エフェクト(動きを減らす設定の人には、進み具合のバー以外は出さない)
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  // ページのどこまで読んだかを上端の細いバーで表示
  var bar = document.createElement('div'); bar.className = 'scroll-progress'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
  var pending = false;
  function progress(){ pending = false; var h = document.documentElement.scrollHeight - innerHeight; bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, scrollY / h) : 0) + ')'; }
  addEventListener('scroll', function(){ if (!pending) { pending = true; requestAnimationFrame(progress); } }, { passive: true });
  addEventListener('resize', progress); progress();
  if (reduce) return;
  // 見出しの背景に、ひらひら舞う葉っぱ(画面に見えている間だけ動かす)
  var COLORS = ['#8cc63f', '#6db552', '#a6d68f', '#3c9a3f', '#c5e1a5', '#e6c75a'];
  document.querySelectorAll('.hero, .page-hero').forEach(function(sec){
    if (!('IntersectionObserver' in window)) return;
    var cv = document.createElement('canvas'); cv.className = 'leaf-fx'; cv.setAttribute('aria-hidden', 'true'); sec.appendChild(cv);
    var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, raf = 0, on = false, last = 0, leaves = [];
    function size(){ var r = sec.getBoundingClientRect(); dpr = Math.min(devicePixelRatio || 1, 2); W = r.width; H = r.height; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    function spawn(l, first){ l.x = Math.random() * W; l.y = first ? Math.random() * H : -24; l.s = 9 + Math.random() * 10; l.vy = 16 + Math.random() * 22;
      l.sw = 18 + Math.random() * 30; l.f = 0.4 + Math.random() * 0.8; l.p = Math.random() * 6.3; l.r = Math.random() * 6.3; l.vr = (Math.random() - 0.5) * 1.2;
      l.c = COLORS[Math.floor(Math.random() * COLORS.length)]; l.a = 0.45 + Math.random() * 0.35; }
    function draw(l, t){
      ctx.save(); ctx.translate(l.x + Math.sin(t * l.f + l.p) * l.sw, l.y); ctx.rotate(l.r + Math.sin(t * l.f * 1.3 + l.p) * 0.6);
      ctx.scale(1, 0.5 + 0.5 * Math.abs(Math.cos(t * l.f + l.p))); ctx.globalAlpha = l.a; ctx.fillStyle = l.c;
      ctx.beginPath(); ctx.moveTo(0, -l.s); ctx.quadraticCurveTo(l.s * 0.8, 0, 0, l.s); ctx.quadraticCurveTo(-l.s * 0.8, 0, 0, -l.s); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, -l.s * 0.8); ctx.lineTo(0, l.s * 0.9); ctx.stroke(); ctx.restore();
    }
    function frame(ts){
      raf = 0; if (!on) return;
      var dt = last ? Math.min((ts - last) / 1000, 0.05) : 0, t = ts / 1000; last = ts;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
      leaves.forEach(function(l){ l.y += l.vy * dt; l.r += l.vr * dt; if (l.y > H + 24) spawn(l, false); draw(l, t); });
      raf = requestAnimationFrame(frame);
    }
    function start(){ if (on && !raf) { last = 0; raf = requestAnimationFrame(frame); } }
    size();
    var n = Math.max(4, Math.min(12, Math.round(W * H / 70000)));
    for (var k = 0; k < n; k++) { var l = {}; spawn(l, true); leaves.push(l); }
    addEventListener('resize', size);
    new IntersectionObserver(function(es){ on = es[0].isIntersecting && !document.hidden; start(); }).observe(sec);
    document.addEventListener('visibilitychange', function(){
      if (document.hidden) { on = false; return; }
      var r = sec.getBoundingClientRect(); on = r.bottom > 0 && r.top < innerHeight; start();
    });
  });
  // マウスで触れたカードが、立体的に傾いて光る(パソコンのみ)
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('.theme, a.kpi, .game-promo').forEach(function(el){
    var glare = document.createElement('span'); glare.className = 'fx-glare'; glare.setAttribute('aria-hidden', 'true');
    el.appendChild(glare); el.classList.add('fx-tilt');
    el.addEventListener('pointermove', function(e){
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      el.style.transform = 'perspective(800px) rotateX(' + ((0.5 - y) * 8).toFixed(2) + 'deg) rotateY(' + ((x - 0.5) * 10).toFixed(2) + 'deg) translateY(-6px)';
      glare.style.background = 'radial-gradient(circle at ' + (x * 100).toFixed(1) + '% ' + (y * 100).toFixed(1) + '%, rgba(255,255,255,.6), rgba(255,255,255,0) 55%)';
      glare.style.opacity = '1';
    });
    el.addEventListener('pointerleave', function(){ el.style.transform = ''; glare.style.opacity = '0'; });
  });
})();
