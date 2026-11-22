// 네이버 클립 게시물 카드 렌더러: node render.js <post.json> <outDir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FONT_DIR = process.env.FONT_DIR;
const font = (w, f) => `@font-face{font-family:P;font-weight:${w};src:url(data:font/otf;base64,${fs.readFileSync(`${FONT_DIR}/Pretendard-${f}.otf`).toString('base64')}) format("opentype")}`;

// 편마다 돌아가며 쓰는 강조색 (표지·제목 띠)
const ACCENTS = ['#FF4B2B', '#2D5BFF', '#00A86B', '#7B3FF2', '#FF2E7E', '#0096C7', '#F26B00'];
const YELLOW = '#FFE14D';

const CSS = `
${font(500, 'Medium')}${font(700, 'Bold')}${font(800, 'ExtraBold')}${font(900, 'Black')}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1440px;font-family:P;background:#FFFFFF;color:#111;overflow:hidden}
.card{position:relative;width:100%;height:100%}
.top{position:absolute;top:56px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;font-size:32px;font-weight:800;z-index:2}
.top .brand{display:flex;align-items:center;gap:14px}
.top .dot{width:22px;height:22px;border-radius:50%;background:var(--a)}
.top .pg{background:#111;color:#fff;padding:8px 22px;border-radius:999px;font-size:28px}
.foot{position:absolute;bottom:56px;left:80px;right:80px;font-size:30px;font-weight:700;color:#999;text-align:center}
mark{background:linear-gradient(transparent 52%, ${YELLOW} 52%);color:inherit;padding:0 6px}

/* 표지 */
.cover{background:var(--a);color:#fff}
.cover .top,.cover .foot{color:rgba(255,255,255,.85)}
.cover .top .dot{background:${YELLOW}}
.cover .top .pg{background:rgba(0,0,0,.25)}
.cover .wrap{position:absolute;left:80px;right:80px;top:250px}
.sticker{display:inline-block;background:${YELLOW};color:#111;font-size:44px;font-weight:900;padding:18px 36px;border-radius:20px;transform:rotate(-4deg);box-shadow:8px 8px 0 #111;margin-bottom:70px}
.cover h1{font-size:132px;font-weight:900;line-height:1.14;letter-spacing:-5px}
.cover h1 em{font-style:normal;color:#111;background:${YELLOW};padding:0 14px;border-radius:12px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.cover .sub{margin-top:60px;font-size:48px;font-weight:700;line-height:1.45;color:rgba(255,255,255,.92)}
.swipe{position:absolute;right:80px;bottom:150px;background:#111;color:#fff;font-size:40px;font-weight:900;padding:24px 40px;border-radius:999px}
.cover .foot{color:rgba(255,255,255,.75)}

/* 본문 카드 */
.band{background:var(--a);color:#fff;padding:140px 80px 54px}
.band .num{display:inline-block;background:${YELLOW};color:#111;font-size:40px;font-weight:900;padding:6px 22px;border-radius:12px;margin-bottom:24px}
.band .title{font-size:92px;font-weight:900;letter-spacing:-3px;line-height:1.15}
.item .top,.list .top{color:#fff}
.item .top .dot,.list .top .dot{background:${YELLOW}}
.item .top .pg,.list .top .pg{background:rgba(0,0,0,.25)}
.body{padding:56px 80px 0}
.row{display:flex;align-items:center;gap:28px;border-radius:28px;padding:26px 36px;margin-bottom:20px;border:5px solid}
.mark{flex:none;width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:900;color:#fff}
.o{background:#E8F8EF;border-color:#00A86B}.o .mark{background:#00A86B}
.x{background:#FFECEC;border-color:#FF3B3B}.x .mark{background:#FF3B3B}
.row .t{font-size:54px;font-weight:800;letter-spacing:-1px;line-height:1.25}
.x .t{color:#C23030;text-decoration:line-through;text-decoration-thickness:6px;text-decoration-color:#FF3B3B}
.tip{margin-top:34px;background:#111;color:#fff;border-radius:28px;padding:38px 44px;font-size:41px;font-weight:700;line-height:1.55}
.tip b{color:${YELLOW};font-weight:900}

/* 요약 */
.list .row{background:#F5F5F7;border-color:#F5F5F7;padding:26px 36px}
.list .mark{width:80px;height:80px;font-size:46px;background:#00A86B}
.list .row .t{font-size:52px}
.list .row .s{margin-left:auto;font-size:36px;font-weight:800;color:#fff;background:var(--a);padding:10px 22px;border-radius:14px;white-space:nowrap}

/* 퀴즈 */
.quiz{background:#111;color:#fff}
.quiz .top{color:#fff}.quiz .top .dot{background:${YELLOW}}.quiz .top .pg{background:#333}
.quiz .wrap{position:absolute;left:80px;right:80px;top:200px}
.quiz .qbadge{display:inline-block;background:var(--a);color:#fff;font-size:42px;font-weight:900;padding:14px 32px;border-radius:999px;margin-bottom:36px}
.quiz .qtitle{font-size:110px;font-weight:900;letter-spacing:-4px;margin-bottom:60px}
.quiz .qtitle{color:${YELLOW}}
.quiz .row{background:#fff;border-color:#fff;color:#111}
.abc{flex:none;width:88px;height:88px;border-radius:22px;background:${YELLOW};color:#111;display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:900}
.quiz .tip{background:${YELLOW};color:#111}
.quiz .tip b{color:var(--a)}
.quiz .foot{color:#777}
/* 뉴스: 사실 정리 */
.stat{font-size:96px;font-weight:900;color:var(--a);letter-spacing:-3px;margin-bottom:30px;line-height:1.15}
.pt{display:flex;gap:24px;align-items:flex-start;background:#F5F5F7;border-radius:24px;padding:28px 34px;margin-bottom:18px;font-size:46px;font-weight:700;line-height:1.4}
.pt .dot2{flex:none;width:20px;height:20px;border-radius:50%;background:var(--a);margin-top:22px}
.src{font-size:38px;font-weight:700;color:#555;line-height:1.6;background:#F5F5F7;border-radius:24px;padding:36px 40px}
.fact .top,.sources .top{color:#fff}.fact .top .dot,.sources .top .dot{background:${YELLOW}}.fact .top .pg,.sources .top .pg{background:rgba(0,0,0,.25)}
`;


// 디자인 테마: post.json의 "theme" 또는 THEME 환경변수 (bold 기본)
const THEMES = {
  dark: `
body.t-dark{background:#0E0E10;color:#fff}
.t-dark .cover{background:#0E0E10}
.t-dark .cover h1{color:#fff}.t-dark .cover h1 em{background:#C6FF00;color:#0E0E10;border-radius:6px}
.t-dark .cover .sub{color:#B8B8C0}
.t-dark .sticker{background:transparent;color:#C6FF00;border:4px solid #C6FF00;box-shadow:none;transform:none;border-radius:8px}
.t-dark .swipe{background:#C6FF00;color:#0E0E10}
.t-dark .top,.t-dark .item .top,.t-dark .list .top,.t-dark .fact .top,.t-dark .sources .top{color:#fff}
.t-dark .top .dot{background:#C6FF00!important}.t-dark .top .pg{background:#26262B!important}
.t-dark .band{background:#0E0E10;border-bottom:6px solid #C6FF00}
.t-dark .band .num{background:#C6FF00}
.t-dark .pt,.t-dark .list .row,.t-dark .src{background:#1C1C21;border-color:#1C1C21;color:#EDEDF2}
.t-dark .pt .dot2{background:#C6FF00}.t-dark .stat{color:#C6FF00}
.t-dark .o{background:#10241A;border-color:#2ECC71;color:#fff}.t-dark .x{background:#2A1414;border-color:#FF5A5A}
.t-dark .x .t{color:#FF8A8A}
.t-dark .tip{background:#1C1C21;border-left:10px solid #C6FF00}.t-dark .tip b{color:#C6FF00}
.t-dark .list .row .s{background:#C6FF00;color:#0E0E10}
.t-dark .quiz{background:#0E0E10}.t-dark .quiz .qtitle{color:#C6FF00}.t-dark .quiz .qbadge{background:#26262B}
.t-dark .quiz .row{background:#1C1C21;border-color:#33333A;color:#fff}.t-dark .abc{background:#C6FF00}
.t-dark .quiz .tip{background:#C6FF00;color:#0E0E10;border:none}.t-dark .quiz .tip b{color:#0E0E10;text-decoration:underline}
.t-dark .foot{color:#55555E}.t-dark .cover .foot{color:#55555E}`,
  breaking: `
body.t-breaking{background:#fff;color:#111}
.t-breaking .cover{background:#fff;color:#111;border-top:40px solid #E60012}
.t-breaking .cover h1 em{background:#E60012;color:#fff;border-radius:0}
.t-breaking .cover .sub{color:#333}
.t-breaking .sticker{background:#E60012;color:#fff;box-shadow:none;transform:none;border-radius:0;letter-spacing:4px}
.t-breaking .swipe{background:#111;border-radius:0}
.t-breaking .top,.t-breaking .item .top,.t-breaking .list .top,.t-breaking .fact .top,.t-breaking .sources .top{color:#111}
.t-breaking .cover .top{top:80px}
.t-breaking .band .title{color:#fff}
.t-breaking .item .top,.t-breaking .list .top,.t-breaking .fact .top,.t-breaking .sources .top{color:#fff}
.t-breaking .top .dot{background:#E60012!important}.t-breaking .top .pg{background:#E60012!important;color:#fff}
.t-breaking .band{background:#111;border-bottom:16px solid #E60012}
.t-breaking .band .num{background:#E60012;color:#fff;border-radius:0}
.t-breaking .pt,.t-breaking .src{background:#fff;border:4px solid #111;border-radius:0}
.t-breaking .pt .dot2{background:#E60012;border-radius:0}.t-breaking .stat{color:#E60012}
.t-breaking .row{border-radius:0}.t-breaking .list .row{background:#fff;border:4px solid #111}
.t-breaking .mark{border-radius:0}
.t-breaking .tip{background:#111;border-radius:0}.t-breaking .tip b{color:#FFD400}
.t-breaking .list .row .s{background:#E60012;border-radius:0}
.t-breaking .quiz{background:#fff;color:#111}.t-breaking .quiz .top{color:#111}
.t-breaking .quiz .qtitle{color:#111;text-decoration:underline;text-decoration-color:#E60012;text-decoration-thickness:12px;text-underline-offset:14px}
.t-breaking .quiz .qbadge{background:#E60012;border-radius:0}
.t-breaking .quiz .row{background:#fff;border:4px solid #111}.t-breaking .abc{background:#E60012;color:#fff;border-radius:0}
.t-breaking .quiz .tip{background:#111;color:#fff}.t-breaking .quiz .tip b{color:#FFD400}
.t-breaking .foot,.t-breaking .cover .foot,.t-breaking .quiz .foot{color:#999}`,
  pastel: `
body.t-pastel{background:#FFF7EE;color:#3A2E39}
.t-pastel .cover{background:#FFE1EA;color:#3A2E39}
.t-pastel .cover h1 em{background:#fff;color:#FF5C8A;border-radius:28px;box-shadow:0 8px 0 #F6B8CB}
.t-pastel .cover .sub{color:#6E5A68}
.t-pastel .sticker{background:#fff;color:#FF5C8A;box-shadow:0 6px 0 #F6B8CB;transform:rotate(-2deg);border-radius:999px}
.t-pastel .swipe{background:#FF5C8A}
.t-pastel .top,.t-pastel .item .top,.t-pastel .list .top,.t-pastel .fact .top,.t-pastel .sources .top{color:#3A2E39}
.t-pastel .top .dot{background:#FF5C8A!important}.t-pastel .top .pg{background:#fff!important;color:#3A2E39}
.t-pastel .band{background:#FFE1EA;color:#3A2E39;border-radius:0 0 60px 60px}
.t-pastel .band .num{background:#fff;color:#FF5C8A;border-radius:999px}
.t-pastel .pt,.t-pastel .src,.t-pastel .list .row{background:#fff;border-color:#fff;border-radius:40px;box-shadow:0 6px 0 #F3DCCB}
.t-pastel .pt .dot2{background:#FF5C8A}.t-pastel .stat{color:#FF5C8A}
.t-pastel .row{border-radius:40px}.t-pastel .o{background:#E9F8EF;border-color:#A6DDBA}.t-pastel .x{background:#FFECEC;border-color:#F5B0B0}
.t-pastel .tip{background:#fff;color:#3A2E39;border:5px dashed #FF9DB8;border-radius:40px}.t-pastel .tip b{color:#FF5C8A}
.t-pastel .list .row .s{background:#FF5C8A;border-radius:999px}
.t-pastel .quiz{background:#E9EDFF;color:#3A2E39}.t-pastel .quiz .top{color:#3A2E39}
.t-pastel .quiz .qtitle{color:#5B6CFF}.t-pastel .quiz .qbadge{background:#5B6CFF;border-radius:999px}
.t-pastel .quiz .row{background:#fff;border-color:#fff;color:#3A2E39;box-shadow:0 6px 0 #CDD4FF}
.t-pastel .abc{background:#5B6CFF;color:#fff;border-radius:50%}
.t-pastel .quiz .tip{background:#fff;border-color:#9DA8FF}.t-pastel .quiz .tip b{color:#5B6CFF}
.t-pastel .foot,.t-pastel .cover .foot,.t-pastel .quiz .foot{color:#B39FAE}`,
};

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const rich = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');

function body(post, c, i, total) {
  const top = `<div class="top"><span class="brand"><span class="dot"></span>${esc(post.series)}</span><span class="pg">${i + 1} / ${total}</span></div>`;
  const foot = post.handle ? `<div class="foot">${esc(post.handle)}</div>` : '';
  let cls = c.type, inner = '';
  if (c.type === 'cover') {
    inner = `<div class="wrap"><span class="sticker">${esc(c.badge)}</span>
      <h1>${esc(c.title).replace(/\[(.+?)\]/g, '<em>$1</em>').replace(/\n/g, '<br>')}</h1>
      <p class="sub">${rich(c.sub)}</p></div><div class="swipe">넘겨 보기 →</div>`;
  } else if (c.type === 'item') {
    inner = `<div class="band"><div class="num">${esc(c.num)}</div><div class="title">${esc(c.title)}</div></div><div class="body">
      ${c.o.map(t => `<div class="row o"><div class="mark">O</div><div class="t">${esc(t)}</div></div>`).join('')}
      ${c.x.map(t => `<div class="row x"><div class="mark">X</div><div class="t">${esc(t)}</div></div>`).join('')}
      <div class="tip">${rich(c.tip)}</div></div>`;
  } else if (c.type === 'list') {
    inner = `<div class="band"><div class="title">${esc(c.title)}</div></div><div class="body">
      ${c.rows.map(r => `<div class="row"><div class="mark">O</div><div class="t">${esc(r[0])}</div><div class="s">${esc(r[1])}</div></div>`).join('')}</div>`;
  } else if (c.type === 'fact') {
    inner = `<div class="band"><div class="num">${esc(c.num)}</div><div class="title">${esc(c.title)}</div></div><div class="body">
      ${c.stat ? `<div class="stat">${esc(c.stat)}</div>` : ''}
      ${c.lines.map(t => `<div class="pt"><span class="dot2"></span><span>${rich(t)}</span></div>`).join('')}
      ${c.tip ? `<div class="tip">${rich(c.tip)}</div>` : ''}</div>`;
  } else if (c.type === 'sources') {
    inner = `<div class="band"><div class="title">${esc(c.title)}</div></div><div class="body"><div class="src">${rich(c.text)}</div></div>`;
  } else if (c.type === 'quiz') {
    inner = `<div class="wrap"><span class="qbadge">${esc(c.badge)}</span><div class="qtitle">${esc(c.title)}</div>
      ${c.options.map((t, k) => `<div class="row"><div class="abc">${'ABCD'[k]}</div><div class="t">${esc(t)}</div></div>`).join('')}
      <div class="tip">${rich(c.tip)}</div></div>`;
  }
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}${THEMES[post.theme] || ''}</style></head>
    <body class="t-${post.theme || 'bold'}" style="--a:${post.accent}"><div class="card ${cls}">${top}${inner}${foot}</div></body></html>`;
}

(async () => {
  const [postFile, outDir] = process.argv.slice(2);
  const post = JSON.parse(fs.readFileSync(postFile, 'utf8'));
  const n = parseInt((path.basename(path.dirname(path.resolve(postFile))).match(/\d+/) || ['1'])[0], 10);
  post.theme = process.env.THEME || post.theme;
  post.accent = post.accent || ACCENTS[(n - 1) % ACCENTS.length];
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
  for (let i = 0; i < post.cards.length; i++) {
    await page.setContent(body(post, post.cards[i], i, post.cards.length), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const over = await page.evaluate(() => {
      const foot = document.querySelector('.foot');
      const lim = foot ? foot.getBoundingClientRect().top - 10 : 1440;
      return Math.max(...[...document.querySelectorAll('.row,.tip,.sub,.pt,.src,.stat')].map(e => e.getBoundingClientRect().bottom)) > lim;
    });
    if (over) console.error(`OVERFLOW ${postFile} card ${i + 1}`);
    const f = path.join(outDir, `${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: f });
    console.log(f);
  }
  await browser.close();
})();
