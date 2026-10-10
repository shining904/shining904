#!/bin/bash
# 숫자 검수: 영상 하나의 목표 숫자(밝기, 컷 길이, 움직임 양, 음량, 음악-목소리 차이)를 잰다.
# usage: guides/measure.sh video.mp4
set -euo pipefail
V="$1"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
# 평균 밝기(0-255)와 프레임 간 차이(움직임 양), 2fps 샘플
read -r yavg ydif < <(ffmpeg -v error -i "$V" -vf "fps=2,scale=270:480,signalstats,metadata=print:file=-" -f null - \
  | awk -F= '/YAVG/{y+=$2;n++} /YDIF/{d+=$2;m++} END{printf "%.0f %.1f\n", y/n, d/m}')
# 장면 전환(컷) 수: 화면이 크게 바뀌는 지점
# (0.6초 안에 연달아 잡힌 것은 플래시 효과로 보고 한 번으로 센다)
cuts=$(ffmpeg -v error -i "$V" -vf "scale=270:480,select='gt(scene,0.25)',metadata=print:file=-" -f null - \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | awk 'BEGIN{last=-9} {if ($1-last>0.6) {printf "%.1f ", $1} last=$1}')
lufs=$(ffmpeg -i "$V" -af ebur128 -f null - 2>&1 | grep -E '^\s+I:' | tail -1 | awk '{print $2}')
lra=$(ffmpeg -i "$V" -af ebur128 -f null - 2>&1 | grep -E '^\s+LRA:' | tail -1 | awk '{print $2}')
python3 - "$V" "$dur" "$yavg" "$ydif" "$cuts" "$lufs" "$lra" <<'PY'
import sys
v,dur,y,d,c,l,lra=sys.argv[1:]
dur=float(dur); times=c.split(); c=len(times)
print(f"{v}")
print(f"  길이 {dur:.1f}초 | 평균 밝기 {y}/255 | 움직임 양 {d} | 장면 전환 {c}회 (평균 {dur/(c+1):.1f}초마다: {' '.join(times)})")
print(f"  음량 {l} LUFS (릴스 목표 -14~-15) | 음량 변화폭 {lra} LU")
PY
