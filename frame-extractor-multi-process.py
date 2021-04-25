import cv2
import time
import sys
import os
from multiprocessing import Process


# Progress bar code is courtesy of StackOverflow user: Aravind Voggu.
# Link to thread: https://stackoverflow.com/questions/6169217/replace-console-output-in-python
def progress_bar(total_frames):
    path = 'ExtractedFrames'
    verified_frames = len([name for name in os.listdir(path)])
    current = verified_frames
    total = total_frames
    barLength = 25
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))
    sys.stdout.flush()


def current_progress():
    path = 'ExtractedFrames'
    verified_frames = len([name for name in os.listdir(path)])
    return verified_frames


# Extract frames from video
def extract_frames(video_path, start_frame, number_of_frames=1000):
    capture = cv2.VideoCapture(video_path)
    capture.set(1, start_frame)  # Points cap to target frame
    current_frame = start_frame
    frame_count = 1
    ret, frame = capture.read()
    while ret and frame_count < number_of_frames:
        ret, frame = capture.read()
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(current_frame) + ".jpg"
        try:
            cv2.imwrite(frame_name, frame)
        except:
            continue
        frame_count += 1  # increases internal frame counter
        current_frame += 1  # increases global frame counter
    capture.release()


def main():
    video_path = 'BadApple.mp4'

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_process = int(total_frames / 3)

    process1_end_frame = frames_per_process
    process2_start_frame = process1_end_frame + 1
    process2_end_frame = total_frames
    # process2_end_frame = process2_start_frame + frames_per_process
    # process3_start_frame = process2_end_frame + 1
    # process3_end_frame = total_frames
    # process4_start_frame = process3_end_frame + 1
    # process4_end_frame = total_frames

    p1 = Process(target=extract_frames, args=(video_path, 1, process1_end_frame))
    p2 = Process(target=extract_frames, args=(video_path, process2_start_frame, process2_end_frame))
    # p3 = Process(target=extract_frames, args=(video_path, process3_start_frame, process3_end_frame))
    # p4 = Process(target=current_progress, args=(total_frames, ))

    # current = current_progress()
    # while current != total_frames:
    #     sys.stdout.write('\r' + str(current))
    #     current = current_progress()

    p1.start()
    p2.start()
    # p3.start()
    # p4.start()

    p1.join()
    p2.join()
    # p3.join()
    # p4.join()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print("\nTotal execution time: ", execution_time)
