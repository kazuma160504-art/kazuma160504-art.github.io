// 共通スクリプト: アイコン描画・スクロールフェード・写真の拡大表示
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
