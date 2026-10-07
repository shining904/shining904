#!/bin/bash
# Builds mix.mp3 (62 s) for the cinematic film: narration raw1-raw8 on
# their cues, natural sound from each live-action clip, the orchestral
# score in two sections (build, then climax) ducked under the voice,
# and soft impacts on the big title reveals.
set -euo pipefail
cd "$(dirname "$0")"
LEN=62

# narration: file start(s) speech-length(s)
NARR=("raw1.mp3 0.8 4.95" "raw2.mp3 8.5 4.85" "raw3.mp3 14.8 6.9" "raw4.mp3 23.2 3.85"
      "raw5.mp3 30.4 7.15" "raw6.mp3 38.3 4.25" "raw7.mp3 46.0 3.55" "raw8.mp3 53.0 4.62")
# clip natural sound: file start(s) length(s) volume
CLIPS=("../clips/dawn.mp4 0 8.0 0.5" "../clips/race.mp4 7.7 6.8 0.45" "../clips/family.mp4 22.3 7.8 0.3"
       "../clips/farm.mp4 29.9 8.0 0.3" "../clips/aerial.mp4 44.2 8.0 0.3")
IMPACT=(5.9 9.0 49.6 52.6)

ms() { python3 -c "print(int($1*1000))"; }
inputs=(-i music.mp3 -i music.mp3)
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=28:60,asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st=30:d=2[mA];"
filters+="[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=102:134,asetpts=PTS-STARTPTS,afade=t=in:d=2,afade=t=out:st=29.5:d=2.5,adelay=30000|30000[mB];"
filters+="[mA][mB]amix=inputs=2:normalize=0,volume=0.63[mus];"
idx=2
labels=""
for n in "${NARR[@]}"; do
  read -r file start len <<<"$n"
  inputs+=(-i "$file")
  d=$(ms "$start")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.08)"):d=0.08,adelay=$d|$d[v$idx];"
  labels+="[v$idx]"
  idx=$((idx + 1))
done
filters+="${labels}amix=inputs=${#NARR[@]}:normalize=0,apad,asplit[narr][key];"
filters+="[mus][key]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=500:makeup=1[bed];"

fx=""
for c in "${CLIPS[@]}"; do
  read -r file start len vol <<<"$c"
  inputs+=(-i "$file")
  d=$(ms "$start")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=in:d=0.2,afade=t=out:st=$(python3 -c "print($len-0.4)"):d=0.4,volume=$vol,adelay=$d|$d[f$idx];"
  fx+="[f$idx]"
  idx=$((idx + 1))
done
for t in "${IMPACT[@]}"; do
  inputs+=(-i impact.mp3)
  d=$(ms "$t")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.06,adelay=$d|$d[f$idx];"
  fx+="[f$idx]"
  idx=$((idx + 1))
done

count=$((2 + ${#CLIPS[@]} + ${#IMPACT[@]}))
filters+="[bed][narr]${fx}amix=inputs=$count:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
