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
  // src="file:경로" → data URI (장면 파일 기준 상대 경로)
  src = src.replace(/src="file:([^"]+)"/g, (_, f) => `src="data:image/png;base64,${fs.readFileSync(path.resolve(path.dirname(html), f)).toString('base64')}"`);
  src = src.replace('<script src="engine.js"></script>', `<script>${fs.readFileSync(path.join(__dirname, 'engine.js'), 'utf8')}</script>`);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.setContent(src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const T = await page.evaluate(() => window.T);
  // WARP: 장면 경계 [디자인 시간들], [실제 시간들]. 장면 안에서는 원래 속도로 재생하고,
  // 남는 시간은 멈춰 있다가 마지막 0.3초(퇴장)만 실제 끝에 맞춘다.
  const warp = process.env.WARP ? JSON.parse(fs.readFileSync(process.env.WARP, 'utf8')) : null;
  const TR = warp ? warp.real[warp.real.length - 1] : T;
  const toDesign = tr => {
    if (!warp) return tr;
    const { design: D, real: R } = warp;
    for (let k = 0; k < R.length - 1; k++) {
      if (tr < R[k + 1] || k === R.length - 2) {
        const u = tr - R[k], dD = D[k + 1] - D[k], dR = R[k + 1] - R[k], ex = Math.min(0.3, dD);
        if (u < dR - ex) return D[k] + Math.min(u, dD - ex);
        return D[k] + (dD - ex) + Math.min(ex, u - (dR - ex));
      }
    }
    return tr;
  };
  await page.evaluate(v => (window.TR = v), TR);
  const total = Math.ceil(TR * fps);
  const audio = process.env.AUDIO;

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    ...(audio ? ['-i', audio, '-c:a', 'aac', '-b:a', '160k', '-shortest'] : []),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < total; i++) {
    await page.evaluate(([t, tr]) => window.frame(t, tr), [toDesign(i / fps), i / fps]);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(out, `${TR.toFixed(1)}s`, `${total} frames`);
})();
