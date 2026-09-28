#!/bin/bash
# Installs everything the HyperFrames and Remotion projects need in a Claude Code on the web session.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# FFmpeg / FFprobe: encoding and media probing
if ! command -v ffmpeg >/dev/null 2>&1; then
  (apt-get install -y -qq ffmpeg || (apt-get update -qq && apt-get install -y -qq ffmpeg)) >/dev/null
fi

# Node dependencies
(cd hyperframes && npm install --no-audit --no-fund)
(cd remotion && npm install --no-audit --no-fund)

# Chrome headless shell for HyperFrames rendering (optional if the download is blocked)
(cd hyperframes && npx hyperframes browser ensure) || echo "hyperframes browser ensure failed; set HYPERFRAMES_BROWSER_PATH"

# Local text-to-speech for `hyperframes tts` (optional)
pip install -q kokoro-onnx soundfile 2>/dev/null || echo "kokoro-onnx install failed; TTS unavailable"

# Remotion can't download its own Chrome here; point it at the pre-installed one
SHELL_BIN=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
if [ -x "$SHELL_BIN" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export REMOTION_BROWSER_EXECUTABLE=$SHELL_BIN" >> "$CLAUDE_ENV_FILE"
fi
