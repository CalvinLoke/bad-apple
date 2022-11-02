import os
import cv2
import click
import time
import sys
from PIL import Image
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import fpstimer
import moviepy.editor as mp
from typing import List, Union, Tuple, Literal
from rich.console import Console
from rich.progress import Progress


# ! Объявление констант
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
C = Console()

# ! Функции
def play_audio(path: str):
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def play_video(frames: List[str]):
    os.system('mode 150, 500')
    timer = fpstimer.FPSTimer(30)
    for frame in frames:
        sys.stdout.write(frame)
        timer.sleep()

def resize_image(image_frame: Image.Image, frame_size: int=150) -> Image.Image:
    return image_frame.resize((frame_size, int((image_frame.size[1] / float(image_frame.size[0] * 2.5)) * frame_size)))

def greyscale(image_frame: Image.Image):
    return image_frame.convert("L")

def pixels_to_ascii(image_frame: Image.Image):
    return "".join([ASCII_CHARS[pixel // 25] for pixel in image_frame.getdata()])

def etg(video_path: str, start_frame: int, frames: int=1000, *, frame_size: int=150) -> List[str]:
    capture, al = cv2.VideoCapture(video_path), []
    capture.set(1, start_frame)

    current_frame, frame_count = start_frame, 1
    ret, image_frame = capture.read()

    with Progress() as pgbar:
        t = pgbar.add_task("ASCII Generation", total=frames)
        while ret and frame_count <= frames:
            pgbar.update(t, total=frames, completed=frame_count)
            ret, image_frame = capture.read()
            try:
                ascii_characters = pixels_to_ascii(greyscale(resize_image(Image.fromarray(image_frame))))  # get ascii characters
                ascii_image = "\n".join(
                    [ascii_characters[index:(index + frame_size)] for index in range(0, len(ascii_characters), frame_size)]
                )
                al.append(ascii_image)
            except Exception as error:
                continue
            frame_count += 1  # increases internal frame counter
            current_frame += 1  # increases global frame counter


    capture.release()
    return al

def preflight_operations(
    path: str,
    *,
    frame_size: int=150
) -> Union[Tuple[int, List[str]], Tuple[Literal[-1], None]]:
    if os.path.exists(path):
        path = path.strip()
        cap = cv2.VideoCapture(path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        mp.VideoFileClip(path).audio.write_audiofile('audio.mp3')

        frames_per_process = int(total_frames / 4)

        process1_end_frame = frames_per_process
        process2_start_frame = process1_end_frame + 1
        process2_end_frame = process2_start_frame + frames_per_process
        process3_start_frame = process2_end_frame + 1
        process3_end_frame = process3_start_frame + frames_per_process
        process4_start_frame = process3_end_frame + 1
        process4_end_frame = total_frames - 1

        start_time = time.time()
        al = etg(path, 1, process4_end_frame, frame_size=frame_size)
        execution_time = time.time() - start_time
        sys.stdout.write('ASCII generation completed! ASCII generation time: ' + str(execution_time))
        return total_frames, al
    else:
        sys.stdout.write('Warning file not found!\n')
        return -1, None

@click.command()
@click.argument(
    "video_path",
    type=str
)
@click.option(
    "-w", "--width",
    type=int
)
def main(video_path: str, width: int):
    total_frames, al = preflight_operations(video_path, frame_size=width)
    if total_frames == -1:
        raise Exception("The video file does not exist!")
    else:
        play_audio('audio.mp3')
        play_video(al)

if __name__ == '__main__':
    main()