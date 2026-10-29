// もりぞうクエストのほかのあそび: クイズと、思い出カード(神経衰弱)。思い出データは game.js と共通
(function () {
  'use strict';
  var STAGES = window.MORIZO_STAGES;
  if (!STAGES) return;

  var ALL = [];
  STAGES.forEach(function (s) { s.items.forEach(function (it) { ALL.push(it); }); });
  function yearOf(it) { var m = /^(\d{4})/.exec(it.d); return m ? +m[1] : (it.d === 'R5' ? 2023 : null); }
  var DATED = ALL.filter(function (it) { return yearOf(it); });
  var MONTHLY = ALL.filter(function (it) { return /^\d{4}\.\d{2}$/.test(it.d); });

  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, String(v)); } catch (e) {} return null; }
  function more(it) { return '<a class="mg-more" href="' + it.u + '" target="_blank" rel="noopener">くわしく見る →</a>'; }

  // ---- あそびの切り替え(タブ)
  var tabs = [].slice.call(document.querySelectorAll('.mode-tabs [data-mode]'));
  var panels = { run: document.getElementById('mode-run'), quiz: document.getElementById('mode-quiz'), memory: document.getElementById('mode-memory') };
  function show(mode, scroll) {
    if (!panels[mode]) mode = 'run';
    tabs.forEach(function (b) { var on = b.getAttribute('data-mode') === mode; b.classList.toggle('on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
    Object.keys(panels).forEach(function (k) { panels[k].hidden = k !== mode; });
    if (mode !== 'run') document.dispatchEvent(new Event('morizo:pause'));
    else window.dispatchEvent(new Event('resize'));
    if (mode === 'quiz' && !quiz.started) quizIntro();
    if (mode === 'memory' && !mem.started) memIntro();
    try { history.replaceState(null, '', mode === 'run' ? location.pathname : '#' + mode); } catch (e) {}
    if (scroll) document.querySelector('.mode-tabs').scrollIntoView({ block: 'start', behavior: 'smooth' });
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-mode')); }); });
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-go]');
    if (b) show(b.getAttribute('data-go'), true);
  });

  // ================================================================ もりぞうクイズ
  var qBox = document.getElementById('quiz-box');
  var quiz = { started: false, list: [], i: 0, score: 0, right: 0, streak: 0, timer: 0, left: 0, answered: false };
  var Q_TIME = 12;

  function makeQuestions() {
    var qs = [], used = {};
    function fresh(pool) {
      for (var k = 0; k < 40; k++) { var it = pool[Math.floor(Math.random() * pool.length)]; if (!used[it.t]) { used[it.t] = 1; return it; } }
      return pool[Math.floor(Math.random() * pool.length)];
    }
    while (qs.length < 10) {
      var r = Math.random(), it, y, opts;
      if (r < 0.4) {
        it = fresh(DATED); y = yearOf(it);
        opts = shuffle([y].concat(shuffle([2021, 2022, 2023, 2024, 2025, 2026].filter(function (v) { return v !== y; })).slice(0, 3)));
        qs.push({ it: it, text: it.e + ' 「' + it.t + '」は、何年のできごと?', opts: opts.map(function (v) { return v + '年'; }), ans: opts.indexOf(y) });
      } else if (r < 0.75) {
        it = fresh(DATED); y = yearOf(it);
        var others = shuffle(DATED.filter(function (o) { return yearOf(o) !== y; })).slice(0, 3);
        opts = shuffle([it].concat(others));
        qs.push({ it: it, text: y + '年のできごとは、どれ?', opts: opts.map(function (o) { return o.e + ' ' + o.t; }), ans: opts.indexOf(it) });
      } else {
        var a = fresh(MONTHLY), b = null;
        for (var k = 0; k < 40 && !b; k++) { var c = MONTHLY[Math.floor(Math.random() * MONTHLY.length)]; if (c.d !== a.d) b = c; }
        if (!b) continue;
        var first = a.d < b.d ? a : b;
        opts = shuffle([a, b]);
        qs.push({ it: first, text: '先に起きたのは、どっち?', opts: opts.map(function (o) { return o.e + ' ' + o.t; }), ans: opts.indexOf(first), pair: opts });
      }
    }
    return qs;
  }

  function quizIntro() {
    var best = +store('morizo-quiz-best') || 0;
    qBox.innerHTML = '<p class="mg-kicker">QUIZ</p><h2>もりぞうクイズ</h2>' +
      '<p class="mg-lead">森一真のあゆみから全10問。早く答えるほど高得点、連続正解でボーナス!</p>' +
      (best ? '<p class="mg-best">ハイスコア ★ ' + best + '</p>' : '') +
      '<button class="btn btn-primary mg-start" type="button" data-q="start">▶ スタート</button>';
  }
  function quizStart() {
    quiz.started = true; quiz.list = makeQuestions(); quiz.i = 0; quiz.score = 0; quiz.right = 0; quiz.streak = 0;
    quizAsk();
  }
  function quizAsk() {
    var q = quiz.list[quiz.i];
    quiz.answered = false; quiz.left = Q_TIME;
    qBox.innerHTML = '<div class="mg-top"><span>Q' + (quiz.i + 1) + ' / ' + quiz.list.length + '</span><span>★ ' + quiz.score + '</span>' +
      (quiz.streak >= 2 ? '<span class="mg-streak">🔥 ' + quiz.streak + '連続</span>' : '') + '</div>' +
      '<div class="mg-timer"><i style="width:100%"></i></div>' +
      '<p class="mg-q">' + esc(q.text) + '</p><div class="mg-opts' + (q.opts.length === 2 ? ' two' : '') + '">' +
      q.opts.map(function (o, k) { return '<button type="button" class="mg-opt" data-a="' + k + '">' + esc(o) + '</button>'; }).join('') +
      '</div><div class="mg-feedback" aria-live="polite"></div>';
    clearInterval(quiz.timer);
    var bar = qBox.querySelector('.mg-timer i'), t0 = Date.now();
    quiz.timer = setInterval(function () {
      quiz.left = Math.max(0, Q_TIME - (Date.now() - t0) / 1000);
      bar.style.width = (quiz.left / Q_TIME * 100) + '%';
      if (quiz.left <= 0) quizAnswer(-1);
    }, 100);
  }
  function quizAnswer(k) {
    if (quiz.answered) return;
    quiz.answered = true; clearInterval(quiz.timer);
    var q = quiz.list[quiz.i], ok = k === q.ans, gain = 0;
    if (ok) { quiz.right++; quiz.streak++; gain = 100 + Math.round(quiz.left * 10) + Math.min(quiz.streak - 1, 5) * 30; quiz.score += gain; }
    else quiz.streak = 0;
    [].forEach.call(qBox.querySelectorAll('.mg-opt'), function (b, n) {
      b.disabled = true;
      if (n === q.ans) b.classList.add('right'); else if (n === k) b.classList.add('wrong');
    });
    var note = q.pair ? q.pair.map(function (o) { return o.e + ' ' + esc(o.d) + ' ' + esc(o.t); }).join('<br>') : esc(q.it.d) + ' ／ ' + esc(q.it.x);
    qBox.querySelector('.mg-feedback').innerHTML = '<p class="mg-result ' + (ok ? 'ok' : 'ng') + '">' +
      (ok ? '⭕ 正解! +' + gain : (k < 0 ? '⏰ 時間切れ…' : '❌ ざんねん…')) + '</p><p class="mg-note">' + note + '</p>' + more(q.it) +
      '<button class="btn btn-primary mg-next" type="button" data-q="next">' + (quiz.i + 1 < quiz.list.length ? '次の問題へ ▶' : '結果を見る ▶') + '</button>';
    var nx = qBox.querySelector('.mg-next');
    try { nx.focus({ preventScroll: true }); } catch (e) {}
  }
  function quizEnd() {
    var best = +store('morizo-quiz-best') || 0, isBest = quiz.score > best;
    if (isBest) store('morizo-quiz-best', quiz.score);
    window.mzTrack && mzTrack('quiz_finish', { score: quiz.score, correct: quiz.right });
    var r = quiz.right, title = r === 10 ? '🎓 もりぞう博士' : r >= 7 ? '🩺 もりぞう通' : r >= 4 ? '🌱 もりぞうファン' : '📖 これから知っていこう';
    qBox.innerHTML = '<p class="mg-kicker">RESULT</p><h2>' + r + ' / 10 問 正解</h2>' +
      '<p class="mg-big">★ ' + quiz.score + '</p>' + (isBest ? '<p class="mg-best">🎉 ハイスコア更新!</p>' : (best ? '<p class="mg-best">ハイスコア ★ ' + best + '</p>' : '')) +
      '<p class="mg-title">称号: ' + title + '</p>' +
      '<div class="mg-btns"><button class="btn btn-primary" type="button" data-q="start">もう一度</button>' +
      '<button class="btn btn-ghost" type="button" data-go="memory">🃏 思い出カードであそぶ</button><button class="btn btn-ghost" type="button" data-go="run">🏃 ランであそぶ</button></div>';
  }
  qBox.addEventListener('click', function (e) {
    var a = e.target.closest('[data-a]'), q = e.target.closest('[data-q]');
    if (a) quizAnswer(+a.getAttribute('data-a'));
    else if (q) {
      var v = q.getAttribute('data-q');
      if (v === 'start') quizStart();
      else if (v === 'next') { quiz.i++; if (quiz.i < quiz.list.length) quizAsk(); else quizEnd(); }
    }
  });

  // ================================================================ 思い出カード(神経衰弱)
  var mBox = document.getElementById('memory-box');
  var mem = { started: false, pairs: 6, cards: [], open: [], done: 0, moves: 0, t0: 0, lock: false, tick: 0 };

  function memIntro() {
    function best(n) { var b = store('morizo-mem-best-' + n); return b ? b + '手' : '—'; }
    mBox.innerHTML = '<p class="mg-kicker">MEMORY</p><h2>思い出カード</h2>' +
      '<p class="mg-lead">同じ思い出のカードを2枚そろえよう。そろうと、その思い出を読めるよ。少ない手数でクリアをめざそう!</p>' +
      '<div class="mg-btns"><button class="btn btn-primary" type="button" data-m="6">かんたん(6ペア)</button><button class="btn btn-primary" type="button" data-m="8">ふつう(8ペア)</button></div>' +
      '<p class="mg-best">ベスト: かんたん ' + best(6) + ' ／ ふつう ' + best(8) + '</p>';
  }
  function memStart(pairs) {
    mem.started = true; mem.pairs = pairs; mem.open = []; mem.done = 0; mem.moves = 0; mem.lock = false; mem.t0 = Date.now();
    var seen = {}, pool = shuffle(ALL).filter(function (it) { if (seen[it.e]) return false; seen[it.e] = 1; return true; }).slice(0, pairs);
    mem.cards = shuffle(pool.concat(pool)).map(function (it) { return { it: it, open: false, done: false }; });
    mBox.innerHTML = '<div class="mg-top"><span id="mm-moves">手数 0</span><span id="mm-time">0秒</span><span>そろった <b id="mm-done">0</b> / ' + pairs + '</span></div>' +
      '<div class="mm-grid" style="--cols:4">' + mem.cards.map(function (c, k) {
        return '<button type="button" class="mm-card" data-c="' + k + '" aria-label="カード ' + (k + 1) + '"><span class="mm-in"><span class="mm-back">🍀</span>' +
          '<span class="mm-front"><b>' + c.it.e + '</b><small>' + esc(c.it.d) + '</small></span></span></button>';
      }).join('') + '</div><div class="mg-feedback mm-info" aria-live="polite"><p class="mg-note">カードをタップしてめくろう</p></div>';
    clearInterval(mem.tick);
    mem.tick = setInterval(function () { var el = document.getElementById('mm-time'); if (el) el.textContent = Math.floor((Date.now() - mem.t0) / 1000) + '秒'; }, 500);
  }
  function memFlip(k) {
    var c = mem.cards[k];
    if (mem.lock || c.open || c.done) return;
    c.open = true; mBox.querySelector('[data-c="' + k + '"]').classList.add('flip');
    mem.open.push(k);
    if (mem.open.length < 2) return;
    mem.moves++; document.getElementById('mm-moves').textContent = '手数 ' + mem.moves;
    var a = mem.cards[mem.open[0]], b = mem.cards[mem.open[1]], pair = mem.open.slice();
    mem.open = [];
    if (a.it === b.it) {
      a.done = b.done = true; mem.done++;
      document.getElementById('mm-done').textContent = mem.done;
      pair.forEach(function (n) { mBox.querySelector('[data-c="' + n + '"]').classList.add('done'); });
      mBox.querySelector('.mm-info').innerHTML = '<p class="mg-result ok">✨ そろった!</p><p class="mg-note"><b>' + a.it.e + ' ' + esc(a.it.d) + ' ' + esc(a.it.t) + '</b><br>' + esc(a.it.x) + '</p>' + more(a.it);
      if (mem.done === mem.pairs) setTimeout(memEnd, 700);
    } else {
      mem.lock = true;
      setTimeout(function () {
        pair.forEach(function (n) { mem.cards[n].open = false; mBox.querySelector('[data-c="' + n + '"]').classList.remove('flip'); });
        mem.lock = false;
      }, 850);
    }
  }
  function memEnd() {
    clearInterval(mem.tick);
    var sec = Math.floor((Date.now() - mem.t0) / 1000), key = 'morizo-mem-best-' + mem.pairs, best = +store(key) || 0, isBest = !best || mem.moves < best;
    if (isBest) store(key, mem.moves);
    window.mzTrack && mzTrack('memory_finish', { pairs: mem.pairs, moves: mem.moves, seconds: sec });
    var perfect = mem.moves === mem.pairs;
    mBox.innerHTML = '<p class="mg-kicker">CLEAR!</p><h2>' + (perfect ? '🌟 パーフェクト!' : 'ぜんぶそろった!') + '</h2>' +
      '<p class="mg-big">' + mem.moves + ' 手 ／ ' + sec + ' 秒</p>' +
      (isBest ? '<p class="mg-best">🎉 ベスト記録!</p>' : '<p class="mg-best">ベスト ' + best + ' 手</p>') +
      '<div class="mg-btns"><button class="btn btn-primary" type="button" data-m="' + mem.pairs + '">もう一度</button>' +
      '<button class="btn btn-ghost" type="button" data-m="' + (mem.pairs === 6 ? 8 : 6) + '">' + (mem.pairs === 6 ? 'ふつう(8ペア)に挑戦' : 'かんたん(6ペア)') + '</button>' +
      '<button class="btn btn-ghost" type="button" data-go="quiz">❓ クイズであそぶ</button></div>';
  }
  mBox.addEventListener('click', function (e) {
    var c = e.target.closest('[data-c]'), m = e.target.closest('[data-m]');
    if (c) memFlip(+c.getAttribute('data-c'));
    else if (m) memStart(+m.getAttribute('data-m'));
  });

  // URL の #quiz / #memory から直接ひらける
  var h = (location.hash || '').slice(1);
  if (h === 'quiz' || h === 'memory') show(h);
})();
