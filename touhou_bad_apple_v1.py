from PIL import Image
import sys
import time
import playsound
import threading
import os

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

frame_size = 100

class AudioThread(threading.Thread):
    def run(self):
        playsound.playsound("bad-apple-audio.mp3")


class VideoThread(threading.Thread):
    def run(self):
        while 1:
            for index in range(1, 6571):
                path_to_image = 'frames/BadApple_' + str(index) + ".jpg"
                image = Image.open(path_to_image, 'r')
                frame = ascii_generator(image)
                sys.stdout.write("\r" + frame)
                # os.system("cls")
                sys.stdout.flush()
                # sys.stdout.write("\r" + path_to_image.format(index))
                delay_duration = (-0.001 / 6571) * index + 0.030
                time.sleep(delay_duration)


# Resize image
def resize_image(image_frame):
    width, height = image_frame.size
    aspect_ratio = (height / float(width * 2.5))
    new_height = int(aspect_ratio * frame_size)
    resized_image = image_frame.resize((frame_size, new_height))
    # print('Aspect ratio: %f' % aspect_ratio)
    # print('New dimensions %d %d' % resized_image.size)
    return resized_image


# Greyscale
def greyscale(image_frame):
    return image_frame.convert("L")


# Convert pixels tp ascii
def pixels_to_ascii(image_frame):
    pixels = image_frame.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters


# Open image => Resize => Greyscale => Convert => Print
def ascii_generator(image_frame):
    resized_image = resize_image(image_frame)  # resize the image
    greyscale_image = greyscale(resized_image)  # convert to greyscale
    ascii_characters = pixels_to_ascii(greyscale_image)  # get ascii characters
    pixel_count = len(ascii_characters)
    ascii_image = "\n".join([ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, 100)])
    return ascii_image


audio_thread = AudioThread(name="Audio Thread")
video_thread = VideoThread(name="Video Thread")
audio_thread.start()
video_thread.start()

# Old code
# while 1:
#     for index in range(1, 6571):
#         path_to_image = 'frames/BadApple_' + str(index) + ".jpg"
#         image = Image.open(path_to_image, 'r')
#         frame = ascii_generator(image)
#         sys.stdout.write("\r" + frame)
#         sys.stdout.flush()
#         delay_duration = (-0.001 / 6571) * index + 0.030
#         # sys.stdout.write("\r" + path_to_image.format(index))
#         # sys.stdout.write("\r" + str(delay_duration))
#         time.sleep(delay_duration)
#         # os.system("cls")