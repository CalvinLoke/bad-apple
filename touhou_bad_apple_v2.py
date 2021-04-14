from PIL import Image
import cv2
import sys
import time
import playsound
import os
import logging

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# frame_interval = 0.0329
frame_interval = 1 / 31
frame_size = 150


def play_audio():
    playsound.playsound("bad-apple-audio.mp3", block=False)


def play_video():
    for frame_number in range(1, 6571):
        start_time = time.time()
        file_name = r"TextFiles/" + "bad_apple" + str(frame_number) + ".txt"
        with open(file_name, 'r') as f:
            sys.stdout.write("\r" + f.read())
        compute_delay = float(time.time() - start_time)
        # delay_duration = frame_interval * (- 0.05 / 9000 + 1.02) - compute_delay # (golden value)
        # modifier = (-0.04/7500) * frame_number + 1.02
        delay_duration = frame_interval - compute_delay
        logging.info(str(delay_duration))
        # print(modifier)
        # print(str(delay_duration))
        if delay_duration < 0:
            delay_duration = 0
        time.sleep(delay_duration)


# Progress bar code is courtesy of StackOverflow user: Aravind Voggu.
# Link to thread: https://stackoverflow.com/questions/6169217/replace-console-output-in-python
def progress_bar(current, total, barLength=25):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))


# Extract frames from video
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    current_frame = 1
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # gets the total number of frames
    print("Video frame extraction, total number of frames")
    while current_frame < total_frames:
        ret, frame = cap.read()
        # sys.stdout.write("\rExtracting " + str(frame_count) + " of " + str(total_frames) + " frames")
        progress_bar(current_frame, total_frames - 1)
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(current_frame) + ".jpg"
        cv2.imwrite(frame_name, frame)
        current_frame += 1
    cap.release()
    sys.stdout.write("\nVideo frame extraction completed\n")

# A little note of acknowledgement to AlexRohwer. The following code of converting image frames into ASCII characters is not original, and is
# based off the code from https://github.com/kiteco/python-youtube-code/blob/master/ascii/ascii_convert.py. As this code repository gains more 
# traction, I feel that I need to properly source the code. 

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
def ascii_generator(image_frame, index):
    resized_image = resize_image(image_frame)  # resize the image
    greyscale_image = greyscale(resized_image)  # convert to greyscale
    ascii_characters = pixels_to_ascii(greyscale_image)  # get ascii characters
    pixel_count = len(ascii_characters)
    ascii_image = "\n".join(
        [ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])
    file_name = r"TextFiles/" + "bad_apple" + str(index) + ".txt"
    with open(file_name, "w") as f:
        f.write(ascii_image)


# Check if frames have been extracted
def check_frames():
    if not os.path.exists('ExtractedFrames'):
            os.makedirs('ExtractedFrames')

    sys.stdout.write("Checking if frames have been extracted...\n")
    verified_frames = 1
    for frame_count in range(1, 6572):
        path_to_file = r'ExtractedFrames/' + 'BadApple_' + str(frame_count) + '.jpg'
        if os.path.isfile(path_to_file):
            sys.stdout.write("\r" + path_to_file + " located")
            verified_frames += 1
            # sys.stdout.write("\r" + str(verified_frames))
    if verified_frames > 6000:
        sys.stdout.write("\rFrames found, proceeding to next step\n")
    else:
        sys.stdout.write("\rNot all frames found, extracting frames now\n")
        extract_frames('BadApple.mp4')


# Check if .txt files exist
def check_txt():
    if not os.path.exists('TextFiles'):
        os.makedirs('TextFiles')
    sys.stdout.write("Checking if .txt files have been created...\n")
    verified_frames = 1
    for frame_count in range(1, 6572):
        path_to_file = r'TextFiles/' + 'bad_apple' + str(frame_count) + '.txt'
        if os.path.isfile(path_to_file):
            verified_frames += 1
    if verified_frames > 6000:
        sys.stdout.write("\r.txt files located, proceeding to animation\n")
    else:
        sys.stdout.write("Converting frames to .txt...\n")
        for frame_count in range(1, 6572):
            path_to_file = r'ExtractedFrames/' + 'BadApple_' + str(frame_count) + '.jpg'
            image = Image.open(path_to_file)
            ascii_generator(image, frame_count)
            progress_bar(frame_count, 6571)
        sys.stdout.write('.txt files created, proceeding to animation')


# Delete extracted frames and .txt files
def delete_assets():
    for index in range(1, 6572):
        # sys.stdout.write("Deleting frames...")
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(index) + ".jpg"
        # print(frame_name)
        try:
            os.remove(frame_name)
        except:
            continue

    for index in range(1, 6572):
        # sys.stdout.write("Deleting .txt files...")
        file_name = r"TextFiles/" + "bad_apple" + str(index) + ".txt"
        try:
            os.remove(file_name)
        except:
            continue


# Main function
def main():
    while True:
        logging.basicConfig(filename='compute_delay.log', level=logging.INFO)
        sys.stdout.write('==============================================================\n')
        sys.stdout.write('Select option: \n')
        sys.stdout.write('1) Play\n')
        sys.stdout.write('2) Delete assets\n')
        sys.stdout.write('3) Exit\n')
        sys.stdout.write('==============================================================\n')

        user_input = input("Your option: ")
        user_input.strip()  # removes trailing whitespaces

        if user_input == '1':
            check_frames()  # Check if image frames have been extracted, extract if necessary
            check_txt()  # Check if .txt files have been created, create if necessary
            os.system('color F0')
            play_audio()
            logging.info('Started')
            play_video()
            logging.info('Stopped')
            os.system('color 07')
            continue
        elif user_input == '2':
            sys.stdout.write('Deleting assets...\n')
            delete_assets()
            sys.stdout.write('Assets deleted\n')
            continue
        elif user_input == '3':
            exit()
            continue
        else:
            sys.stdout.write('Unknown input!\n')
            continue


if __name__ == "__main__":
    main()
