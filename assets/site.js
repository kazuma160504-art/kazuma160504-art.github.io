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
// 現在のテーマタブを見える位置へ
(function(){ var on=document.querySelector('.theme-tabs a.on'); if(on) on.scrollIntoView({inline:'center',block:'nearest'}); })();
