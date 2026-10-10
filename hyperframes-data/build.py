# ③ Data story: "숫자로 보는 이천" — count-ups, a rice-field tile grid, a donut and a dot grid.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import comp, index
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B0, BEAT = 0.08, 0.5457
def b(k): return round(B0 + BEAT * k, 3)
S = [0, b(3), b(8), b(13), b(18), b(23), 15]  # scene boundaries on beats
NAVY, GOLD, CEL, RED, INK = "#14244a", "#a8740f", "#3f7a66", "#d0503a", "#2b3445"
css = f'''        #root {{ background: #f6f2ea; font-family: "Noto Sans KR", sans-serif; }}
        .ds-scene {{ position: absolute; inset: 0; opacity: 0; }}
        .ds-kick {{ position: absolute; left: 90px; top: 300px; font-size: 44px; font-weight: 800; color: {GOLD}; letter-spacing: 4px; }}
        .ds-num {{ position: absolute; left: 80px; top: 380px; font-family: "Black Han Sans", sans-serif; font-size: 250px; line-height: 1; color: {NAVY}; }}
        .ds-num small {{ font-size: 110px; margin-left: 10px; }}
        .ds-label {{ position: absolute; left: 90px; top: 660px; font-size: 60px; font-weight: 800; color: {INK}; }}
        .ds-src {{ position: absolute; left: 90px; right: 90px; bottom: 170px; font-size: 28px; font-weight: 500; color: #8a8478; }}
        .ds-vis {{ position: absolute; left: 90px; right: 90px; top: 820px; height: 820px; }}
        .ds-dot {{ position: absolute; border-radius: 50%; }}
        .ds-tile {{ position: absolute; width: 58px; height: 58px; border-radius: 8px; background: {GOLD}; }}
        #ds-title1 {{ position: absolute; left: 90px; top: 640px; font-family: "Black Han Sans", sans-serif; font-size: 170px; line-height: 1.05; color: {NAVY}; }}
        #ds-title1 em {{ font-style: normal; color: {GOLD}; }}
        #ds-rule {{ position: absolute; left: 90px; top: 1060px; width: 900px; height: 14px; background: {NAVY}; transform-origin: left center; }}
        .ds-note {{ position: absolute; left: 90px; top: 1120px; font-size: 48px; font-weight: 800; color: {INK}; }}
        #ds-donut {{ position: absolute; left: 50%; top: 40px; width: 720px; height: 720px; margin-left: -360px; }}
        #ds-donut-txt {{ position: absolute; left: 0; right: 0; top: 300px; text-align: center; font-family: "Black Han Sans", sans-serif; font-size: 150px; color: {CEL}; }}
        #ds-end1 {{ position: absolute; left: 0; right: 0; top: 720px; text-align: center; font-family: "Black Han Sans", sans-serif; font-size: 140px; line-height: 1.15; color: {NAVY}; }}
        #ds-end2 {{ position: absolute; left: 0; right: 0; top: 1270px; text-align: center; font-size: 46px; font-weight: 800; color: {INK}; }}
'''
# scene 2 people dots, scene 3 tiles, scene 5 kiln dots
people = "".join(f'          <div class="ds-dot ds-p" style="left:{(i % 15) * 60}px;top:{(i // 15) * 60 + 80}px;width:40px;height:40px;background:{NAVY if i % 7 else GOLD}"></div>\n' for i in range(150))
tiles = "".join(f'          <div class="ds-tile" style="left:{(i % 13) * 69}px;top:{(i // 13) * 69 + 40}px;opacity:{0.55 + 0.45 * ((i * 37) % 10) / 10:.2f}"></div>\n' for i in range(117))
kilns = "".join(f'          <div class="ds-dot ds-k" style="left:{(i % 16) * 56}px;top:{(i // 16) * 56 + 60}px;width:38px;height:38px;background:{RED if i % 5 else GOLD}"></div>\n' for i in range(240))
body = f'''        <div id="ds-s0" class="ds-scene">
          <div class="ds-kick">ICHEON IN NUMBERS</div>
          <div id="ds-title1">숫자로<br />보는 <em>이천</em></div>
          <div id="ds-rule"></div>
          <div class="ds-note">2026 데이터 스토리</div>
        </div>
        <div id="ds-s1" class="ds-scene">
          <div class="ds-kick">POPULATION</div>
          <div class="ds-num"><span id="ds-n1">0</span><small>만 명</small></div>
          <div class="ds-label">함께 사는 이천 시민</div>
          <div class="ds-vis">
{people}          </div>
          <div class="ds-src">2026년 8월 주민등록인구 기준 (약 22만 7천 명)</div>
        </div>
        <div id="ds-s2" class="ds-scene">
          <div class="ds-kick">RICE FIELDS</div>
          <div class="ds-num"><span id="ds-n2">0</span><small>ha+</small></div>
          <div class="ds-label">이천쌀 논 · 축구장 약 9,800개</div>
          <div class="ds-vis">
{tiles}          </div>
          <div class="ds-src">2022년 언론 보도 기준 (축구장 1개 ≈ 0.714ha로 환산)</div>
        </div>
        <div id="ds-s3" class="ds-scene">
          <div class="ds-kick">OUR VARIETIES</div>
          <div class="ds-vis" style="top: 380px">
            <svg id="ds-donut" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="80" fill="none" stroke="#e4ddd0" stroke-width="26" />
              <circle id="ds-arc" cx="100" cy="100" r="80" fill="none" stroke="{CEL}" stroke-width="26" stroke-linecap="round"
                stroke-dasharray="502.65" stroke-dashoffset="502.65" transform="rotate(-90 100 100)" />
            </svg>
            <div id="ds-donut-txt"><span id="ds-n3">0</span>%</div>
          </div>
          <div class="ds-label" style="top: 1180px">우리 품종 '해들·알찬미'로 바꾼 논</div>
          <div class="ds-src">2022년 언론 보도 기준 (관내 논 면적 대비)</div>
        </div>
        <div id="ds-s4" class="ds-scene">
          <div class="ds-kick">CERAMICS</div>
          <div class="ds-num"><span id="ds-n4">0</span><small>여 곳</small></div>
          <div class="ds-label">도자기축제에 참여한 도예 공방</div>
          <div class="ds-vis">
{kilns}          </div>
          <div class="ds-src">2026 이천도자기축제 소개 기준</div>
        </div>
        <div id="ds-s5" class="ds-scene">
          <div id="ds-end1">숫자 너머,<br />사람이 사는<br />이천</div>
          <div id="ds-end2">올해로 25번째, 이천쌀문화축제</div>
          <div class="ds-src" style="text-align:center">자료: 주민등록인구(2026.8), 언론 보도(2022), 축제 소개(2026)</div>
        </div>
'''
js = "        const tl = gsap.timeline({ paused: true });\n"
for i in range(6):
    a, e = S[i], S[i + 1]
    js += f'        tl.set("#ds-s{i}", {{ opacity: 1 }}, {a});\n'
    js += f'        tl.fromTo("#ds-s{i}", {{ y: {0 if i == 0 else 260} }}, {{ y: 0, duration: 0.35, ease: "power3.out" }}, {a});\n'
    if i < 5:
        js += f'        tl.to("#ds-s{i}", {{ y: -260, opacity: 0, duration: 0.3, ease: "power2.in" }}, {round(e - 0.3, 3)});\n'
    js += f'        tl.fromTo("#ds-s{i} .ds-kick, #ds-s{i} .ds-label, #ds-s{i} .ds-src", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.12 }}, {round(a + 0.15, 3)});\n'
def count(sel, target, a, dur, dec=0, comma=True):
    fmt = f'v.toFixed({dec})' if dec else ('Math.round(v).toLocaleString("en-US")' if comma else 'Math.round(v)')
    return (f'        {{ const o = {{ v: 0 }}; tl.to(o, {{ v: {target}, duration: {dur}, ease: "power2.out", onUpdate: () => {{ const v = o.v; document.querySelector("{sel}").textContent = {fmt}; }} }}, {a}); }}\n')
js += f'        tl.fromTo("#ds-title1", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 0.1);\n'
js += f'        tl.fromTo("#ds-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power2.inOut" }}, 0.4);\n'
js += f'        tl.fromTo(".ds-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.8);\n'
js += count("#ds-n1", 22.7, S[1] + 0.2, 1.4, dec=1)
js += f'        tl.fromTo(".ds-p", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, ease: "back.out(2)", stagger: 0.009 }}, {round(S[1] + 0.3, 3)});\n'
js += count("#ds-n2", 7000, S[2] + 0.2, 1.4)
js += f'        tl.fromTo(".ds-tile", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.22, ease: "back.out(1.8)", stagger: 0.011 }}, {round(S[2] + 0.3, 3)});\n'
js += count("#ds-n3", 93, S[3] + 0.2, 1.5, comma=False)
js += f'        tl.to("#ds-arc", {{ attr: {{ "stroke-dashoffset": {502.65 * 0.07:.2f} }}, duration: 1.5, ease: "power2.out" }}, {round(S[3] + 0.2, 3)});\n'
js += count("#ds-n4", 240, S[4] + 0.2, 1.4, comma=False)
js += f'        tl.fromTo(".ds-k", {{ scale: 0, y: -30 }}, {{ scale: 1, y: 0, duration: 0.18, ease: "back.out(2)", stagger: 0.0055 }}, {round(S[4] + 0.3, 3)});\n'
js += f'        tl.fromTo("#ds-end1", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, {round(S[5] + 0.1, 3)});\n'
js += f'        tl.fromTo("#ds-end2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {round(S[5] + 0.7, 3)});\n'
js += '        window.__timelines["data"] = tl;\n'
open("compositions/data.html", "w").write(comp("data", ["bhs", "noto"], css, body, js))
open("index.html", "w").write(index("숫자로 보는 이천", "data", 15, "Data story test: scenes switch on beats of the 110 BPM bed. Figures: resident registration (2026.8), press reports (2022), festival notice (2026). Music: Magnific Google Lyria, original track.", "#f6f2ea"))
