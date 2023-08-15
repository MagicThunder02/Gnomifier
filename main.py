import numpy as np
from scipy.stats import truncnorm
import random
import argparse
from pprint import pprint
from moviepy.editor import AudioFileClip, VideoFileClip, CompositeAudioClip

# TODO
# - argomenti da riga di comando
# - distribuzione delle posizioni custom


def main_():
    nOcc = 10
    distibution = "uniform"
    cut = 0.5

    tracks = ["gnome.mp3", "boom.m4a"]

    gnomes = genGnomes(nOcc, distibution, cut, tracks)
    videoClip = VideoFileClip("videoCut.mp4")

    video = editVideo(videoClip, gnomes)

    pprint(sorted(gnomes, key=lambda gnome: gnome["position"]))

    video.write_videofile("output.mp4")


def main():
    parser = argparse.ArgumentParser(
        prog="gnomifier", description="I'm a gnome, you've been gnomed"
    )

    parser.add_argument(
        "-i", "--input_video", help="specify the video to gnomify", required=True
    )
    parser.add_argument("-g", "--gnomes", help="gnome sounds", required="True")
    parser.add_argument(
        "-o", "--output", help="specify the name of the output file", required=True
    )
    parser.add_argument(
        "-n",
        "--occurences",
        help="number of gnome occurences per video",
        required=False,
        type=int,
        default=5,
    )
    parser.add_argument(
        "-d",
        "--distribution",
        help="distribution of the gnomes over the video length",
        required=False,
        default="uniform",
    )
    parser.add_argument(
        "-c",
        "--cut",
        help="distribution of suond cut length",
        required=False,
        default="logistic",
    )

    args = parser.parse_args()

    tracks = []
    for track in args.gnomes.split(","):
        tracks.append(track.strip())

    gnomifier(
        args.input_video,
        tracks,
        args.output,
        args.occurences,
        args.distribution,
        args.cut,
    )


def gnomifier(input_video, tracks, output, occurrences, distribution, cut):
    gnomes = genGnomes(occurrences, distribution, cut, tracks)
    videoClip = VideoFileClip(input_video)

    video = editVideo(videoClip, gnomes)

    pprint(sorted(gnomes, key=lambda gnome: gnome["position"]))

    video.write_videofile("output.mp4")


def drawFrom(distribution, average=0.5):
    if distribution == "uniform":
        res = random.random()

    elif distribution == "normal":
        res = np.random.normal(0.5, 0.1)
        if res < 0:
            res = 0
        if res > 1:
            res = 1

    elif distribution == "exponential":
        res = np.random.exponential(scale=1 / 0.5)
        res = res / (res + 1)

    else:
        raise Exception(f"{distribution} is not a valid distribution")

    return res


def genGnomes(nOcc, distribution, cut, tracks):
    gnomes = []

    for i in range(nOcc):
        gnome = {}

        gnome["position"] = round(drawFrom(distribution), 3)
        gnome["duration"] = round(drawFrom("exponential"), 3)
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
