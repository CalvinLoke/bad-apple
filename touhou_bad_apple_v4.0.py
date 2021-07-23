import cv2
import time
import sys
from PIL import Image
from multiprocessing import Process
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import fpstimer
import platform


ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
frame_size = 150
frame_interval = 1.0 / 30.75

ASCII_LIST = []

# Plays audio asychronously using pygame library
def play_audio(path):
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


# Reads ASCII characters and prints them out on screen
def play_video(isMidi, end_frame):

    # Band-aid fix for audio-syncrhonization issues across different platforms. Might need to look into the root cause.
    if platform.system() == 'Windows':
        # Alters CLI interface for Bad Apple!! (only works for Windows)
        os.system('color F0')
        time.sleep(0)

    elif platform.system() == 'Linux':
        time.sleep(0.4)

    timer = fpstimer.FPSTimer(30)

    if isMidi is True:
        start_frame = 30
    else:
        start_frame = 1

    for frame_number in range(start_frame, end_frame-1):
        sys.stdout.write("\r" + ASCII_LIST[frame_number])
        timer.sleep()

    sys.stdout.write('\n')
    os.system('color 07')


# Extract frames from video
def extract_transform_generate(video_path, start_frame, number_of_frames=1000):
    capture = cv2.VideoCapture(video_path)
    capture.set(1, start_frame)  # Points cap to target frame
    current_frame = start_frame
    frame_count = 1
    ret, image_frame = capture.read() # Reads the first frame of the source video

    # Cycles through video frames, extracts them and converts them to ASCII before storing into memory
    while ret and frame_count <= number_of_frames:
        ret, image_frame = capture.read()
        try:
            image = Image.fromarray(image_frame)
            ascii_characters = pixels_to_ascii(greyscale(resize_image(image)))  # get ascii characters
            pixel_count = len(ascii_characters)
            ascii_image = "\n".join(
                [ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])

            ASCII_LIST.append(ascii_image) 

        # Band-aid fix when image is not found for some reason
        except Exception as error:
            continue

        progress_bar(frame_count,number_of_frames)

        frame_count += 1  # increases internal frame counter
        current_frame += 1  # increases global frame counter

    capture.release()


# Progress bar code is courtesy of StackOverflow user: Aravind Voggu.
# Link to thread: https://stackoverflow.com/questions/6169217/replace-console-output-in-python
def progress_bar(current, total, barLength=25):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))


# A little note of acknowledgement to AlexRohwer. The following code of converting image frames into ASCII characters
# is not original, and is based off the code from
# https://github.com/kiteco/python-youtube-code/blob/master/ascii/ascii_convert.py. As this code repository gains
# more traction, I feel that I need to properly source the code.


# Resize image
def resize_image(image_frame):
    width, height = image_frame.size
    aspect_ratio = (height / float(width * 2.5))  # 2.5 modifier to offset vertical scaling on console
    new_height = int(aspect_ratio * frame_size)
    resized_image = image_frame.resize((frame_size, new_height))
    # print('Aspect ratio: %f' % aspect_ratio)
    # print('New dimensions %d %d' % resized_image.size)
    return resized_image


# Greyscale
def greyscale(image_frame):
    return image_frame.convert("L")


# Convert pixels to ascii
def pixels_to_ascii(image_frame):
    pixels = image_frame.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters


# Open image => Resize => Greyscale => Convert to ASCII => Store in text file
def ascii_generator(image_path, start_frame, number_of_frames):
    current_frame = start_frame
    while current_frame <= number_of_frames:
        path_to_image = image_path + '/BadApple_' + str(current_frame) + '.jpg'
        image = Image.open(path_to_image)
        ascii_characters = pixels_to_ascii(greyscale(resize_image(image)))  # get ascii characters
        pixel_count = len(ascii_characters)
        ascii_image = "\n".join(
            [ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])
        file_name = r"TextFiles/" + "bad_apple" + str(current_frame) + ".txt"
        try:
            with open(file_name, "w") as f:
                f.write(ascii_image)
        except FileNotFoundError:
            continue
        current_frame += 1


# Generates ASCII and store it in memory 
def preflight_operations():
    video_path = 'BadApple.mp4'
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    # Checks if ASCII list is empty, only for v4.0 where the only video playback is Bad Apple!!:
    if not ASCII_LIST:
        start_time = time.time()
        sys.stdout.write('Beginning ASCII generation...\n')
        extract_transform_generate(video_path, 0, total_frames)
        execution_time = time.time() - start_time
        sys.stdout.write('\nASCII generation completed! ASCII generation time: ' + str(execution_time))
        time.sleep(2)
    elif ASCII_LIST:
        sys.stdout.write('ASCII assets found in memory, re-using assets\n')
        time.sleep(2)

    return total_frames


# Main running loop
def main():
    while True:
        user_input = input("Please enter your desired frame size (default: 150): ")
        user_input.strip()  # removes trailing whitespaces
        try:
            global frame_size
            frame_size = int(user_input)
        except:
            sys.stdout.write('Invalid frame size!: \n')

        sys.stdout.write('==============================================================\n')
        sys.stdout.write('Select option: \n')
        sys.stdout.write('1) Play\n')
        sys.stdout.write('2) Exit\n')
        sys.stdout.write('==============================================================\n')

        user_input = str(input("Your option: "))
        user_input.strip()  # removes trailing whitespaces

        if user_input == '1':
            sys.stdout.write('Original mp3 (0), Midi (1)\n')
            user_input = str(input("Enter 0 or 1: "))
            user_input.strip()  # removes trailing whitespaces
            if user_input == '0':
                path_to_file = 'bad-apple-audio.mp3'
                total_frames = preflight_operations()
                play_audio(path_to_file)
                play_video(isMidi=False, end_frame=total_frames)
            elif user_input == '1':
                path_to_file = 'alstroemeria_records_bad_apple.mid'
                total_frames = preflight_operations()
                play_audio(path_to_file)
                play_video(isMidi=True, end_frame=total_frames)
            else:
                sys.stdout.write('Unknown input!\n')
            continue
        elif user_input == '2':
            exit()
            continue
        else:
            sys.stdout.write('Unknown input!\n')
            continue


if __name__ == '__main__':
    main()
