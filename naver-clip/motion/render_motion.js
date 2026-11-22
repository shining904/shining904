// 장면 HTML을 프레임 단위로 캡처해 MP4로 만든다: node render_motion.js <scene.html> <out.mp4> [fps]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

(async () => {
  const [html, out, fpsArg] = process.argv.slice(2);
  const fps = parseInt(fpsArg || '30', 10);
  const FONT_DIR = process.env.FONT_DIR;
  const fontCss = ['Medium:500', 'Bold:700', 'ExtraBold:800', 'Black:900'].map(s => {
    const [f, w] = s.split(':');
    const b64 = fs.readFileSync(`${FONT_DIR}/Pretendard-${f}.otf`).toString('base64');
    return `@font-face{font-family:P;font-weight:${w};src:url(data:font/otf;base64,${b64}) format("opentype")}`;
  }).join('');
  let src = fs.readFileSync(html, 'utf8').replace('/*FONTS*/', fontCss);
  src = src.replace('<script src="engine.js"></script>', `<script>${fs.readFileSync(path.join(__dirname, 'engine.js'), 'utf8')}</script>`);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.setContent(src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const T = await page.evaluate(() => window.T);
  const total = Math.ceil(T * fps);

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.frame(t), i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(out, `${T}s`, `${total} frames`);
})();
