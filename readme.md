## Video Editing Workflow

1. Put raw video file to edit in workspace folder
2. Open raw video file and cuts.txt. Define the time intervals of pieces of video to keep
3. Run Bash script cutvid.sh to generate cut video file ready for capcut + .wav audo file
4. Go to https://ws.nelfproject.be/nelf_transcribe/index/ and create a new transcription project. Load in the .wav audio file to generate word timed subtitles. Output is transcription_wordtimings_final_audio.txt
5. Run Python script on transcription_wordtimings_final_audio.txt to generate short sentence subtitles. Output is subs_nl.srt
6. Manually adjust subtitles in Aegisub
7. Export subtitles from Aegisub as .txt file
8. Translate subtitles using ChatGPT. Name file subs_en.srt
9. Import translated subtitles back into Aegisub for final adjustments
10. Put edited video + srt files in capcut folder
11. Finalise editing in capcut
