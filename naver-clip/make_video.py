# 카드 이미지를 9:16 세로 영상(MP4)으로 변환: python3 make_video.py <postNN> [FONT_DIR]
# 음악은 넣지 않아요. 클립 앱에서 제공하는 음원을 고르면 저작권 문제가 없어요.
import glob, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ACCENTS = ['#FF4B2B', '#2D5BFF', '#00A86B', '#7B3FF2', '#FF2E7E', '#0096C7', '#F26B00']
W, H = 1080, 1920
post_dir = sys.argv[1].rstrip('/')
font_dir = sys.argv[2] if len(sys.argv) > 2 else os.environ['FONT_DIR']
n = int(''.join(c for c in os.path.basename(post_dir) if c.isdigit()))
accent = ACCENTS[(n - 1) % len(ACCENTS)]
post = json.load(open(f'{post_dir}/post.json'))
cards = sorted(glob.glob(f'{post_dir}/cards/*.png'))
F = lambda w, s: ImageFont.truetype(f'{font_dir}/Pretendard-{w}.otf', s)

# 카드 종류별 노출 시간(초)
DUR = {'cover': 2.2, 'item': 3.2, 'list': 3.0, 'quiz': 4.0}
durs = [DUR[c['type']] for c in post['cards']]

frames_dir = f'{post_dir}/video_frames'
os.makedirs(frames_dir, exist_ok=True)
frames = []
for i, path in enumerate(cards):
    bg = Image.new('RGB', (W, H), accent)
    d = ImageDraw.Draw(bg)
    # 위: 시리즈 이름 + 저장 유도
    pill = f"{post['series']}  ·  {n}편"
    f1 = F('Black', 52)
    tw = d.textlength(pill, font=f1)
    d.rounded_rectangle([(W - tw) / 2 - 36, 150, (W + tw) / 2 + 36, 250], 50, fill='#FFE14D')
    d.text((W / 2, 200), pill, font=f1, fill='#111', anchor='mm')
    # 가운데: 카드
    card = Image.open(path).resize((1000, 1333), Image.LANCZOS)
    mask = Image.new('L', card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, *card.size], 40, fill=255)
    bg.paste(card, (40, 300), mask)
    # 아래: 진행 바
    total = len(cards)
    r, g, b = (int(accent[j:j + 2], 16) for j in (1, 3, 5))
    mix = tuple(int(c + (255 - c) * 0.35) for c in (r, g, b))
    seg = (W - 160 - (total - 1) * 12) / total
    for k in range(total):
        x = 80 + k * (seg + 12)
        d.rounded_rectangle([x, 1700, x + seg, 1716], 8, fill='#FFFFFF' if k <= i else mix)
    d.text((W / 2, 1790), '끝까지 보고 퀴즈 맞혀 보세요!', font=F('Bold', 44), fill='white', anchor='mm')
    f = f'{frames_dir}/{i + 1:02d}.png'
    bg.save(f)
    frames.append(f)

# ffmpeg: 옆으로 넘기는 전환
T = 0.35
args = ['ffmpeg', '-y', '-loglevel', 'error']
for f, du in zip(frames, durs):
    args += ['-loop', '1', '-t', str(du + T), '-i', f]
fc, prev, offset = [], None, 0.0
for i, du in enumerate(durs):
    fc.append(f"[{i}:v]fps=30,setsar=1,format=yuv420p[v{i}]")
for i in range(1, len(durs)):
    offset += durs[i - 1]
    a = 'v0' if i == 1 else f'x{i - 1}'
    fc.append(f"[{a}][v{i}]xfade=transition=slideleft:duration={T}:offset={offset:.2f}[x{i}]")
out_label = f'x{len(durs) - 1}'
os.makedirs(f'{post_dir}/video', exist_ok=True)
out = f'{post_dir}/video/{n:02d}편_영상.mp4'
args += ['-filter_complex', ';'.join(fc), '-map', f'[{out_label}]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
subprocess.run(args, check=True)
for f in frames:
    os.remove(f)
os.rmdir(frames_dir)
print(out, f'{sum(durs) + T:.1f}s')
