#!/usr/bin/env bash
# Audio for the full-interview cut (v5 = v4 + HOLD). The film's beats before T0 and after T1 keep
# their v4 timing, offset by the hold: the score plays to T0, a soft two-bar bed from its intro
# loops under the mayor (bar-aligned, ducked well below his voice), then the score resumes at T1
# so the hit still lands on 서희함. The sound design is split the same way; the mayor's voice comes
# from his clip from MAYOR_START.
#   HOLD=37.4 MAYOR=mayor/greeting.mp4 MAYOR_START=0.8 tools/mix_gold5.sh
#   OUT=music-gold5v-mix.mp3 HOLD=10.8 MAYOR=mayor/greeting-highlight.mp4 tools/mix_gold5.sh
set -euo pipefail
cd "$(dirname "$0")/../shared/assets"
HOLD=${HOLD:?set HOLD}; MAYOR=${MAYOR:?set MAYOR}; MAYOR_START=${MAYOR_START:-0}; OUT=${OUT:-music-gold5-mix.mp3}
T0=15.4; T1=17.4
calc() { python3 -c "print(round($1, 3))"; }
END=$(calc "$T0 + $HOLD")                 # film resumes 1:1 here (real time)
REAL=$(calc "37.5 + $HOLD - ($T1 - $T0)")
TALK=$(calc "$END + 0.6 - 13.5")          # clip audio length: through the circle closing
ms() { python3 -c "print(int(round(($1) * 1000)))"; }
ffmpeg -v error -y -ss 4.9 -t 4.8 -i music-gold3.mp3 -ar 44100 -ac 2 bed-bar2.wav
ffmpeg -v error -y -i music-gold3.mp3 -i bed-bar2.wav -i sfx-gold2.wav -i "$MAYOR" -filter_complex "
[0]atrim=0:$(calc "$T0 + 0.5"),afade=t=out:st=$T0:d=0.5[p1];
[1]aloop=loop=-1:size=211680,atrim=0:$(calc "$HOLD + 0.4"),afade=t=in:d=0.6,afade=t=out:st=$(calc "$HOLD - 0.2"):d=0.6,volume=0.8,adelay=$(ms "$T0 - 0.2")|$(ms "$T0 - 0.2")[bed];
[0]atrim=start=$(calc "$T1 - 0.3"),asetpts=PTS-STARTPTS,afade=t=in:d=0.5,adelay=$(ms "$END - 0.3")|$(ms "$END - 0.3")[p2];
[p1][bed][p2]amix=inputs=3:normalize=0,volume='1-0.72*(clip((t-13.2)/0.5,0,1)-clip((t-$(calc "$END - 0.6"))/0.8,0,1))':eval=frame[m];
[2]atrim=0:$T0,volume=0.9[s1];
[2]atrim=start=$T1,asetpts=PTS-STARTPTS,volume=0.9,adelay=$(ms "$END")|$(ms "$END")[s2];
[3:a]atrim=$MAYOR_START:$(calc "$MAYOR_START + $TALK"),asetpts=PTS-STARTPTS,afade=t=out:st=$(calc "$TALK - 0.3"):d=0.3,loudnorm=I=-16:TP=-2,adelay=13500|13500,volume=1.5[mv];
[m][s1][s2][mv]amix=inputs=4:normalize=0" -t "$REAL" -ar 44100 "$OUT.pre.wav"
# two-pass linear loudness normalisation keeps the score's dynamics (the hit) intact
M=$(ffmpeg -i "$OUT.pre.wav" -af loudnorm=I=-14:TP=-1.5:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$M" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i "$OUT.pre.wav" -af "loudnorm=I=-14:TP=-1.5:linear=true:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset)" -ar 44100 -b:a 192k "$OUT"
rm -f "$OUT.pre.wav"
echo "length $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") (film $REAL)"
ffmpeg -i "$OUT" -af ebur128 -f null - 2>&1 | grep "I:" | tail -1
