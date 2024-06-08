import librosa
import numpy as np
import os

songs = ["background1.mp3", "background2.mp3", "background3.mp3", "background4.mp3", "background5.mp3"]
difficulties = ["easy", "med", "hard"]

def analyze_beats(file_path, difficulty):
    y, sr = librosa.load(file_path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    if difficulty == "easy":
        beat_times = beat_times[::3]  # Reduce the number of beats for easy
    elif difficulty == "med":
        beat_times = beat_times[::2]  # Moderate number of beats for medium
    # "hard" uses the original beat times

    return beat_times

for song in songs:
    for difficulty in difficulties:
        beatmap_file = f"{song.split('.')[0]}_{difficulty}.txt"
        if not os.path.exists(beatmap_file):
            beat_times = analyze_beats(song, difficulty)
            np.savetxt(beatmap_file, beat_times)
