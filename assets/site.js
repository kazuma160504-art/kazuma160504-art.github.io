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
