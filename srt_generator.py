import re

def float_to_srt(seconds):
    """Convert float seconds to SRT timestamp string HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def txt_to_srt(txt_file, srt_file, max_words=6, pause_threshold=0.3):
    counter = 1
    grouped_words = []
    time_group_start_seconds = None
    time_group_end_seconds = None

    with open(srt_file, 'w', encoding='utf-8') as output, open(txt_file, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue

            match = re.match(r"\[\s*(\d+:\d+:\d+\.\d+)\s*-->\s*(\d+:\d+:\d+\.\d+)\s*\]\s*(.*)", line)
            if not match:
                continue
            start, end, word = match.groups()

            # Convert timestamps to seconds
            h, m, s = start.split(":")
            start_sec = int(h) * 3600 + int(m) * 60 + float(s)
            h, m, s = end.split(":")
            end_sec = int(h) * 3600 + int(m) * 60 + float(s)

            if not grouped_words:
                time_group_start_seconds = start_sec

            # Check pause between previous word and this word
            if grouped_words:
                prev_end = time_group_end_seconds
                if start_sec - prev_end > pause_threshold or len(grouped_words) >= max_words:
                    # Write current group to SRT
                    output.write(f"{counter}\n")
                    output.write(f"{float_to_srt(time_group_start_seconds)} --> {float_to_srt(time_group_end_seconds)}\n")
                    output.write(" ".join(grouped_words) + "\n\n")
                    counter += 1
                    grouped_words = []
                    time_group_start_seconds = start_sec

            grouped_words.append(word)
            time_group_end_seconds = end_sec

        # Write remaining words
        if grouped_words:
            output.write(f"{counter}\n")
            output.write(f"{float_to_srt(time_group_start_seconds)} --> {float_to_srt(time_group_end_seconds)}\n")
            output.write(" ".join(grouped_words) + "\n\n")

    print(f"SRT file '{srt_file}' created successfully!")

# Example usage:
# txt_to_srt('transcription_wordtimings_final_audio.txt', 'output.srt')

def main():
    txt_to_srt('transcription_wordtimings_final_audio.txt', 'subs_nl.srt')

if __name__ == "__main__":
    main()