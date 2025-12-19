#!/usr/bin/env bash

INPUT="$1"
CUTS="cuts.txt"
BASENAME="$(basename "$INPUT" .mp4)"
OUT="${BASENAME}_cut.mp4"
AUDIO="${BASENAME}_cut_audio.wav"

if [ -z "$INPUT" ] || [ ! -f "$CUTS" ]; then
  echo "Usage: cutvid.sh input.mp4 (requires cuts.txt)"
  exit 1
fi

PARTS=()
i=1

while read -r START END; do
  OUTPART="part$i.mp4"
  echo "Cutting $OUTPART ($START → $END)"
  ffmpeg -nostdin -ss "$START" -to "$END" -i "$INPUT" -c copy "$OUTPART"
  PARTS+=("$OUTPART")
  i=$((i+1))
done < "$CUTS"

echo "Concatenating..."
> list.txt
for p in "${PARTS[@]}"; do
  echo "file '$p'" >> list.txt
done

ffmpeg -nostdin -f concat -safe 0 -i list.txt -c copy "$OUT"

echo "Extracting audio..."
ffmpeg -nostdin -i "$OUT" -vn -acodec pcm_s16le -ar 44100 -ac 2 "$AUDIO"

echo "Cleaning up..."
rm part*.mp4 list.txt

echo "Done → $OUT + $AUDIO"
