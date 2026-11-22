// 모션그래픽 엔진: 시간 t(초)를 받아 화면 상태를 계산하는 순수 함수 구조.
// 장면 파일에서 tw()로 애니메이션을 등록하고, window.frame(t)로 특정 시점을 그린다.
(function () {
  const ease = {
    linear: p => p,
    outCubic: p => 1 - Math.pow(1 - p, 3),
    outExpo: p => (p === 1 ? 1 : 1 - Math.pow(2, -10 * p)),
    inOutCubic: p => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    outBack: p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
    inCubic: p => p * p * p,
  };
  const DEF = { o: 0, x: 0, y: 0, s: 1, r: 0, blur: 0, clip: 100, sh: 0 };
  const tweens = [];   // {sel, t0, dur, props:{k:[from,to]}, e}
  const counters = []; // {sel, t0, dur, from, to, fmt, e}
  const loops = [];    // (t) => void
  window.tw = (sel, t0, dur, props, e = 'outCubic') => tweens.push({ sel, t0, dur, props, e });
  window.count = (sel, t0, dur, from, to, fmt = v => Math.round(v).toLocaleString('en-US'), e = 'outExpo') =>
    counters.push({ sel, t0, dur, from, to, fmt, e });
  window.loop = fn => loops.push(fn);
  // 등장/퇴장 단축 함수
  window.pop = (sel, t0, d = 0.35, from = 0.6) => tw(sel, t0, d, { o: [0, 1], s: [from, 1] }, 'outBack');
  window.up = (sel, t0, d = 0.45, dy = 60) => tw(sel, t0, d, { o: [0, 1], y: [dy, 0] }, 'outExpo');
  window.slideX = (sel, t0, d = 0.45, dx = 120) => tw(sel, t0, d, { o: [0, 1], x: [dx, 0] }, 'outExpo');
  window.out = (sel, t0, d = 0.3) => tw(sel, t0, d, { o: [1, 0], y: [0, -70], blur: [0, 8] }, 'inCubic');
  window.wipe = (sel, t0, d = 0.4) => tw(sel, t0, d, { o: [1, 1], clip: [0, 100] }, 'outExpo');
  window.shake = (sel, t0, d = 0.3, amp = 14) => tw(sel, t0, d, { sh: [amp, 0] }, 'linear');

  window.frame = t => {
    const state = new Map();
    const els = new Set(tweens.map(w => w.sel));
    els.forEach(sel => state.set(sel, { ...DEF }));
    tweens.slice().sort((a, b) => a.t0 - b.t0).forEach(w => {
      if (t < w.t0) return;
      const p = ease[w.e](Math.min(1, (t - w.t0) / w.dur));
      const st = state.get(w.sel);
      for (const k in w.props) { const [a, b] = w.props[k]; st[k] = a + (b - a) * p; }
    });
    state.forEach((st, sel) => document.querySelectorAll(sel).forEach(el => {
      const jx = st.sh ? Math.sin(t * 90) * st.sh : 0, jy = st.sh ? Math.cos(t * 77) * st.sh * 0.6 : 0;
      el.style.opacity = st.o;
      el.style.transform = `translate(${st.x + jx}px, ${st.y + jy}px) scale(${st.s}) rotate(${st.r}deg)`;
      el.style.filter = st.blur > 0.05 ? `blur(${st.blur}px)` : 'none';
      el.style.clipPath = st.clip < 100 ? `inset(0 ${100 - st.clip}% 0 0)` : 'none';
    }));
    counters.forEach(c => {
      const p = t < c.t0 ? 0 : ease[c.e](Math.min(1, (t - c.t0) / c.dur));
      document.querySelectorAll(c.sel).forEach(el => (el.textContent = c.fmt(c.from + (c.to - c.from) * p)));
    });
    loops.forEach(fn => fn(t));
  };
})();
