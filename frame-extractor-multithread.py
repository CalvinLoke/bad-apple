import cv2
import sys
import time
import os
from queue import Queue
from threading import Thread


# Multi-threaded frame extraction
class ExtractFrames(Thread):
    def __init__(self, video_path, start_frame, number_of_frames, threadID):
        Thread.__init__(self)
        self.video_path = video_path
        self.start_frame = start_frame
        self.number_of_frames = number_of_frames
        self.threadID = threadID

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        cap.set(1, self.start_frame)  # Points cap to target frame
        current_frame = self.start_frame
        frame_count = 1
        ret, frame = cap.read()
        while ret and frame_count < self.number_of_frames:
            ret, frame = cap.read()
            frame_name = r"ExtractedFrames/" + "BadApple_" + str(current_frame) + ".jpg"
            # status_string = "Thread " + str(self.threadID) + " currently on frame " + str(current_frame)
            # print(status_string)
            try:
                cv2.imwrite(frame_name, frame)
            except:
                continue
            frame_count += 1  # increases internal frame counter
            current_frame += 1  # increases global frame counter
        cap.release()


def extract_frames_one_threads(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_thread = int(total_frames / 1)

    # 2 threaded operation
    thread1_end_frame = frames_per_thread

    thread1 = ExtractFrames(path_to_video, 0, thread1_end_frame, 1)

    thread1.start()
    thread1.join()


def extract_frames_two_threads(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_thread = int(total_frames / 2)

    # 2 threaded operation
    thread1_end_frame = frames_per_thread
    thread2_start_frame = thread1_end_frame + 1
    thread2_end_frame = total_frames

    thread1 = ExtractFrames(path_to_video, 0, thread1_end_frame, 1)
    thread2 = ExtractFrames(path_to_video, thread2_start_frame, thread2_end_frame, 2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def extract_frames_three_threads(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_thread = int(total_frames / 3)

    # 3 threaded operation
    thread1_end_frame = frames_per_thread
    thread2_start_frame = thread1_end_frame + 1
    thread2_end_frame = thread2_start_frame + frames_per_thread
    thread3_start_frame = thread2_end_frame + 1
    thread3_end_frame = total_frames

    thread1 = ExtractFrames(path_to_video, 0, thread1_end_frame, 1)
    thread2 = ExtractFrames(path_to_video, thread2_start_frame, thread2_end_frame, 2)
    thread3 = ExtractFrames(path_to_video, thread3_start_frame, thread3_end_frame, 3)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


def extract_frames_four_threads(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_thread = int(total_frames / 4)

    # 4 threaded operation
    thread1_end_frame = frames_per_thread
    thread2_start_frame = thread1_end_frame + 1
    thread2_end_frame = thread2_start_frame + frames_per_thread
    thread3_start_frame = thread2_end_frame + 1
    thread3_end_frame = thread3_start_frame + frames_per_thread
    thread4_start_frame = thread3_end_frame + 1
    thread4_end_frame = total_frames

    # print(total_frames)
    # print(frames_per_thread)
    # print(1, thread1_end_frame)
    # print(thread2_start_frame, thread2_end_frame)
    # print(thread3_start_frame, thread3_end_frame)
    # print(thread4_start_frame, thread4_end_frame)

    thread1 = ExtractFrames(path_to_video, 0, thread1_end_frame, 1)
    thread2 = ExtractFrames(path_to_video, thread2_start_frame, thread2_end_frame, 2)
    thread3 = ExtractFrames(path_to_video, thread3_start_frame, thread3_end_frame, 3)
    thread4 = ExtractFrames(path_to_video, thread4_start_frame, thread4_end_frame, 4)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


# Single threaded frame extraction
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 1
    while frame_count < number_of_frames:
        ret, frame = cap.read()
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(frame_count) + ".jpg"
        cv2.imwrite(frame_name, frame)
        frame_count += 1
    cap.release()


def extract_frames_old(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 1
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # gets the total number of frames
    print("Video frame extraction, total number of frames")
    while frame_count < total_frames:
        ret, frame = cap.read()
        frame_name = r"ExtractedFrames/" + "BadApple_" + str(frame_count) + ".jpg"
        cv2.imwrite(frame_name, frame)
        frame_count += 1
    cap.release()
    sys.stdout.write("\rVideo frame extraction completed")


path_to_video = 'BadApple.mp4'
start_time = time.time()
extract_frames_two_threads(path_to_video)
# extract_frames(path_to_video, 6571)
end_time = time.time()

execution_time = end_time - start_time
print(execution_time)
