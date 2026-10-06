#!/bin/bash
# Builds mix.mp3 (30 s): narration n1-n6 on their scene cues, music ducked
# under the voice, whoosh on every wipe, impact on the big title slams.
set -euo pipefail
cd "$(dirname "$0")"

# narration: file start(s) speech-length(s)
NARR=("n1.mp3 0.25 2.30" "n2.mp3 3.15 3.32" "n3.mp3 6.75 6.25" "n4.mp3 13.30 2.95" "n5.mp3 18.05 3.65" "n6.mp3 24.40 3.80")
WHOOSH=(2.67 6.27 12.77 17.57 23.67)
IMPACT=(1.05 13.30 18.45 22.10 25.00)

inputs=(-i music.wav)
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:30,afade=t=in:d=0.3,afade=t=out:st=28:d=2,volume=0.85[mus];"
idx=1
narr_labels=""
for n in "${NARR[@]}"; do
  read -r file start len <<<"$n"
  inputs+=(-i "$file")
  ms=$(python3 -c "print(int($start*1000))")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.08)"):d=0.08,adelay=$ms|$ms[v$idx];"
  narr_labels+="[v$idx]"
  idx=$((idx + 1))
done
filters+="${narr_labels}amix=inputs=${#NARR[@]}:normalize=0,asplit[narr][key];"
filters+="[mus][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=400:makeup=1[bed];"

fx_labels=""
add_fx() {
  local file=$1 vol=$2; shift 2
  for t in "$@"; do
    inputs+=(-i "$file")
    ms=$(python3 -c "print(int($t*1000))")
    filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$vol,adelay=$ms|$ms[f$idx];"
    fx_labels+="[f$idx]"
    idx=$((idx + 1))
  done
}
add_fx whoosh.mp3 0.15 "${WHOOSH[@]}"
add_fx impact.mp3 0.07 "${IMPACT[@]}"

count=$((2 + ${#WHOOSH[@]} + ${#IMPACT[@]}))
filters+="[bed][narr]${fx_labels}amix=inputs=$count:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur=30,atrim=0:30[out]"

ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
