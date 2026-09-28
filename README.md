![뉴스레터 미리보기](https://private-user-images.githubusercontent.com/215607788/453352077-8737bc64-370e-4db4-8116-4f2ebb775a66.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDk1NDQ0MTEsIm5iZiI6MTc0OTU0NDExMSwicGF0aCI6Ii8yMTU2MDc3ODgvNDUzMzUyMDc3LTg3MzdiYzY0LTM3MGUtNGRiNC04MTE2LTRmMmViYjc3NWE2Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxMFQwODI4MzFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zMDkzMWI4NWZlZmY0N2Q0OTRlOWM0M2FjOGE3NjdjZWU3MDQ2ODIzZmRmMTI4ZWE3Nzc5OWMzYmE5MjQ3NGFlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.a9ESSPMpYzXvIaLIp0Q0GU3npQapUubWPbn7sHc-Rqs)

## 🎬 영상 만들기 (HyperFrames + Remotion)

| 폴더 | 도구 | 영상을 만드는 방법 |
|---|---|---|
| `hyperframes/` | [HyperFrames](https://hyperframes.heygen.com) (HeyGen) | HTML + CSS + GSAP 애니메이션 → MP4 |
| `remotion/` | [Remotion](https://www.remotion.dev) | React 컴포넌트 → MP4 |

필요한 것: Node.js 22 이상, FFmpeg (HyperFrames 렌더링용)

```bash
# HyperFrames
cd hyperframes && npm install
npm run dev      # 브라우저에서 미리보기 (Studio)
npm run render   # renders/ 폴더에 MP4 생성

# Remotion
cd remotion && npm install
npm run dev              # 브라우저에서 미리보기 (Remotion Studio)
npx remotion render      # out/ 폴더에 MP4 생성
```

`.claude/skills/`에는 Claude Code가 HyperFrames·Remotion 영상을 잘 만들도록 돕는 스킬이 들어 있습니다.
`.claude/hooks/session-start.sh`는 Claude Code 웹 세션이 시작될 때 FFmpeg, npm 패키지, 렌더링용 Chrome, 음성 합성(Kokoro TTS)을 자동으로 설치합니다.

선택 기능 (내 PC에서 쓸 때):
- 음성 합성: `pip install kokoro-onnx soundfile` → `npx hyperframes tts "문장"` (한국어 음성은 아직 없음)
- 자막용 받아쓰기: `npx hyperframes models install parakeet` → `npx hyperframes transcribe 파일.mp3`
- 배경음악 생성: `pip install transformers torch soundfile numpy`
Remotion은 개인·3인 이하 팀은 무료이고, 그 이상 회사는 유료 라이선스가 필요합니다.
