import cv2
import time
import sys
from PIL import Image
from multiprocessing import Process
import shutil
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
frame_size = 150
frame_interval = 1.0 / 30.5


def play_audio():
    # path_to_file = 'bad-apple-audio.mp3'
    # pygame.init()
    # pygame.mixer.pre_init(44100, -16, 2, 2048)
    # pygame.mixer.init()
    # pygame.mixer.music.load(path_to_file)
    # pygame.mixer.music.play()

    path_to_file = 'alstroemeria_records_bad_apple.mid'

    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(path_to_file)
    pygame.mixer.music.play()


def play_video():
    os.system('color F0')
    os.system('mode 150, 500')

    for frame_number in range(30, 6570):
        start_time = time.time()
        file_name = r"TextFiles/" + "bad_apple" + str(frame_number) + ".txt"
        with open(file_name, 'r') as f:
            sys.stdout.write("\r" + f.read())
        compute_delay = float(time.time() - start_time)
        delay_duration = frame_interval - compute_delay
        if delay_duration < 0:
            delay_duration = 0
        time.sleep(delay_duration)

    os.system('color 07')


# Extract frames from video
def extract_frames(video_path, start_frame, number_of_frames=1000):
    capture = cv2.VideoCapture(video_path)
    capture.set(1, start_frame)  # Points cap to target frame
    current_frame = start_frame
    frame_count = 1
    ret, frame = capture.read()
    while ret and frame_count <= number_of_frames:
        ret, frame = capture.read()
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(current_frame) + ".jpg"
        try:
            cv2.imwrite(frame_name, frame)
        except:
            continue
        frame_count += 1  # increases internal frame counter
        current_frame += 1  # increases global frame counter
    capture.release()


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
    # resized_image = resize_image(image_frame)  # resize the image
    # greyscale_image = greyscale(resized_image)  # convert to greyscale
    # ascii_characters = pixels_to_ascii(greyscale_image)  # get ascii characters

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


def preflight_checks():
    path = 'ExtractedFrames'
    if not os.path.exists('ExtractedFrames'):
        os.makedirs('ExtractedFrames')
    sys.stdout.write("Checking if frames have been extracted...\n")

    video_path = 'BadApple.mp4'
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_process = int(total_frames / 4)

    process1_end_frame = frames_per_process
    process2_start_frame = process1_end_frame + 1
    process2_end_frame = process2_start_frame + frames_per_process
    process3_start_frame = process2_end_frame + 1
    process3_end_frame = process3_start_frame + frames_per_process
    process4_start_frame = process3_end_frame + 1
    process4_end_frame = total_frames - 1

    print(1, process1_end_frame)
    print(process2_start_frame, process2_end_frame)
    print(process3_start_frame, process3_end_frame)
    print(process4_start_frame, process4_end_frame)

    verified_frames = len([name for name in os.listdir(path)])

    if verified_frames >= (total_frames - 5):
        sys.stdout.write("\rFrames found, proceeding to next step\n")
    else:
        print('Beginning frame extraction...')

        p1 = Process(target=extract_frames, args=(video_path, 1, process1_end_frame))
        p2 = Process(target=extract_frames, args=(video_path, process2_start_frame, process2_end_frame))
        p3 = Process(target=extract_frames, args=(video_path, process3_start_frame, process3_end_frame))
        p4 = Process(target=extract_frames, args=(video_path, process4_start_frame, process4_end_frame))

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()

        p1.close()
        p2.close()
        p3.close()
        p4.close()

        sys.stdout.write('\rFrame extraction completed\n')

    if not os.path.exists('TextFiles'):
        os.makedirs('TextFiles')
    sys.stdout.write("Checking if .txt files have been created...\n")
    path = 'TextFiles'
    verified_frames = len([name for name in os.listdir(path)])

    if verified_frames >= (total_frames - 5):
        sys.stdout.write("\r.txt files located, proceeding to animation\n")
    else:
        sys.stdout.write('Beginning ASCII generation...\n')

        image_path = r'ExtractedFrames'

        p1 = Process(target=ascii_generator, args=(image_path, 1, process1_end_frame))
        p2 = Process(target=ascii_generator, args=(image_path, process2_start_frame, process2_end_frame))
        p3 = Process(target=ascii_generator, args=(image_path, process3_start_frame, process3_end_frame))
        p4 = Process(target=ascii_generator, args=(image_path, process4_start_frame, process4_end_frame))

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()

        p1.close()
        p2.close()
        p3.close()
        p4.close()

        sys.stdout.write('ASCII generation completed\n')


def main():
    preflight_checks()
    play_audio()
    play_video()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Total execution time: ", execution_time)
