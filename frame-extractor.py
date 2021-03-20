import cv2
import sys


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
    frame_count = 1
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # gets the total number of frames
    print("Video frame extraction, total number of frames")
    while frame_count < total_frames:
        ret, frame = cap.read()
        # sys.stdout.write("\rExtracting " + str(frame_count) + " of " + str(total_frames) + " frames")
        progress_bar(frame_count, total_frames)
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(frame_count) + ".jpg"
        cv2.imwrite(frame_name, frame)
        frame_count += 1
    cap.release()
    sys.stdout.write("\rVideo frame extraction completed")


extract_frames("BadApple.mp4")
