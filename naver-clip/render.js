// 네이버 클립 게시물 카드 렌더러: node render.js <post.json> <outDir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FONT_DIR = process.env.FONT_DIR;
const font = (w, f) => `@font-face{font-family:P;font-weight:${w};src:url(data:font/otf;base64,${fs.readFileSync(`${FONT_DIR}/Pretendard-${f}.otf`).toString('base64')}) format("opentype")}`;

const CSS = `
${font(500, 'Medium')}${font(700, 'Bold')}${font(800, 'ExtraBold')}${font(900, 'Black')}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1440px;font-family:P;background:#FFF8EC;color:#1E1E24;overflow:hidden}
.card{position:relative;width:100%;height:100%;padding:110px 96px}
.top{position:absolute;top:64px;left:96px;right:96px;display:flex;justify-content:space-between;font-size:34px;font-weight:700;color:#8A7F70}
.brand{color:#E8553D}
.foot{position:absolute;bottom:64px;left:96px;right:96px;font-size:30px;font-weight:500;color:#8A7F70;text-align:center}
.center{height:100%;display:flex;flex-direction:column;justify-content:center}
h1{font-size:118px;font-weight:900;line-height:1.18;letter-spacing:-4px}
h1 em{font-style:normal;color:#E8553D}
.sub{margin-top:48px;font-size:46px;font-weight:700;color:#5A5348;line-height:1.45}
.badge{display:inline-block;align-self:flex-start;background:#1E1E24;color:#FFF8EC;font-size:38px;font-weight:800;padding:14px 30px;border-radius:999px;margin-bottom:48px}
.num{font-size:44px;font-weight:800;color:#E8553D;margin-bottom:20px}
.title{font-size:84px;font-weight:900;letter-spacing:-3px;line-height:1.2;margin-bottom:56px}
.row{display:flex;align-items:center;gap:32px;background:#fff;border-radius:32px;padding:36px 44px;margin-bottom:24px;box-shadow:0 6px 0 #EADFCB}
.mark{flex:none;width:92px;height:92px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:900;color:#fff}
.o .mark{background:#2E9E6A}.x .mark{background:#C9C2B6}
.row .t{font-size:60px;font-weight:800;letter-spacing:-1px}
.x .t{color:#9A9286;text-decoration:line-through;text-decoration-thickness:5px}
.tip{margin-top:44px;background:#FFE3D6;border-radius:32px;padding:40px 44px;font-size:42px;font-weight:700;line-height:1.5}
.tip b{color:#E8553D;font-weight:900}
.list .row{padding:28px 40px}
.list .row .t{font-size:50px}
.list .row .s{margin-left:auto;font-size:36px;font-weight:700;color:#8A7F70}
.quiz .row .t{font-size:56px}
.abc{flex:none;width:80px;height:80px;border-radius:24px;background:#1E1E24;color:#FFF8EC;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:900}
`;

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const rich = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');

function body(post, c, i, total) {
  const top = `<div class="top"><span class="brand">${esc(post.series)}</span><span>${i + 1} / ${total}</span></div>`;
  const foot = post.handle ? `<div class="foot">${esc(post.handle)}</div>` : '';
  let inner = '';
  if (c.type === 'cover') {
    inner = `<div class="center"><span class="badge">${esc(c.badge)}</span><h1>${esc(c.title).replace(/\[(.+?)\]/g, '<em>$1</em>').replace(/\n/g, '<br>')}</h1><p class="sub">${rich(c.sub)}</p></div>`;
  } else if (c.type === 'item') {
    inner = `<div class="center"><div class="num">${esc(c.num)}</div><div class="title">${esc(c.title)}</div>
      ${c.o.map(t => `<div class="row o"><div class="mark">O</div><div class="t">${esc(t)}</div></div>`).join('')}
      ${c.x.map(t => `<div class="row x"><div class="mark">X</div><div class="t">${esc(t)}</div></div>`).join('')}
      <div class="tip">${rich(c.tip)}</div></div>`;
  } else if (c.type === 'list') {
    inner = `<div class="center list"><div class="title">${esc(c.title)}</div>
      ${c.rows.map(r => `<div class="row o"><div class="mark">O</div><div class="t">${esc(r[0])}</div><div class="s">${esc(r[1])}</div></div>`).join('')}</div>`;
  } else if (c.type === 'quiz') {
    inner = `<div class="center quiz"><span class="badge">${esc(c.badge)}</span><div class="title">${esc(c.title)}</div>
      ${c.options.map((t, k) => `<div class="row"><div class="abc">${'ABCD'[k]}</div><div class="t">${esc(t)}</div></div>`).join('')}
      <div class="tip">${rich(c.tip)}</div></div>`;
  }
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body><div class="card">${top}${inner}${foot}</div></body></html>`;
}

(async () => {
  const [postFile, outDir] = process.argv.slice(2);
  const post = JSON.parse(fs.readFileSync(postFile, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
  for (let i = 0; i < post.cards.length; i++) {
    await page.setContent(body(post, post.cards[i], i, post.cards.length), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const f = path.join(outDir, `${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: f });
    console.log(f);
  }
  await browser.close();
})();
