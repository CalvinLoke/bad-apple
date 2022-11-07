import os
import sys
import click
import avplib
import pygame
import fpstimer
from rich.console import Console
from rich.progress import Progress
from typing import Tuple, List

# ! Set Environ
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# ! Reinitialize
class Console(Console):
    def set_size(self, size: Tuple[int, int]) -> None:
        os.system(f'mode {size[0]},{size[1]}')

# ! Initialized
console = Console()

# ! Functions
def play_audio(audio_path: str) -> None:
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

def play_video(frames: List[str]) -> None:
    fps = fpstimer.FPSTimer(30)
    for i in frames:
        sys.stdout.write(i)
        fps.sleep()

# ! CLI
@click.command()
@click.argument(
    "video_path",
    type=click.Path(exists=True)
)
@click.option(
    "-r", "--res",
    type=click.Tuple([int, int]),
    default=(150, 40),
    show_default=True
)
def main(video_path: str, res: Tuple[int, int]=(150, 40)):
    console.set_size((res[0]+1, res[1]))

    video = avplib.AVP(video_path)
    audio_path = video.get_audio("file", "temp.mp3")

    with Progress() as pr:
        gaf = pr.add_task("Generation ASCII")
        def update_bar(complited: int, total: int):
            pr.update(gaf, total=total, completed=complited)
        frames = video.get_ascii_frames(res, callback=update_bar)
    play_audio(audio_path)
    play_video(frames)

if __name__ == '__main__':
    main()