import numpy as np
import random
from pprint import pprint
from moviepy.editor import AudioFileClip, VideoFileClip, CompositeAudioClip

# TODO
# - argomenti da riga di comando
# - distribuzione delle posizioni custom


def main():
    nOcc = 10
    distibution = "uniform"
    cut = 0.5

    tracks = ["gnome.mp3", "boom.m4a"]

    gnomes = genGnomes(nOcc, distibution, cut, tracks)
    videoClip = VideoFileClip("videoCut.mp4")

    video = editVideo(videoClip, gnomes)

    pprint(sorted(gnomes, key=lambda gnome: gnome["position"]))

    video.write_videofile("output.mp4")


def genGnomes(nOcc, distibution, cut, tracks):
    gnomes = []

    for i in range(nOcc):
        gnome = {}
        number = np.random.exponential(scale=1 / 0.5)

        gnome["position"] = round(random.random(), 3)
        gnome["duration"] = round(number / (number + 1), 3)
        gnome["track"] = random.choice(tracks)

        gnomes.append(gnome)

    return gnomes


def cutAudio(track, duration):
    audioClip = AudioFileClip(track)
    audioClip = audioClip.subclip(0, duration * audioClip.duration)

    return audioClip


def editVideo(videoClip, gnomes):
    audioClips = []
    videoLenght = videoClip.duration

    for gnome in gnomes:
        audioClip = cutAudio(gnome["track"], gnome["duration"])
        audioClip = audioClip.set_start(gnome["position"] * videoLenght)
        audioClips.append(audioClip)

    finalAudio = CompositeAudioClip([videoClip.audio] + audioClips)
    finalClip = videoClip.set_audio(finalAudio)
    return finalClip


if __name__ == "__main__":
    main()
