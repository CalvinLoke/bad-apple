import os
import cv2
import moviepy.editor as mp
import soundfile as sf
from PIL import Image
from typing import Literal
from io import BufferedReader, BytesIO
from tempfile import NamedTemporaryFile
from .units import ASCII_CHARS

class AVP:
    def __init__(self, fp) -> None:
        if isinstance(fp, str):
            self.path = os.path.abspath(fp)
        elif isinstance(fp, bytes):
            with NamedTemporaryFile("wb", delete=False) as tempfile:
                tempfile.write(fp)
                self.path = os.path.abspath(tempfile.name)
        elif isinstance(fp, BufferedReader):
            self.path = os.path.abspath(fp.name)
        else:
            raise TypeError(f"The variable type 'fp' does not accept the type {type(fp)}")
    
    def get_frames_count(self):
        cap = cv2.VideoCapture(self.path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        cap.release()
        return total_frames
    
    def get_audio(self, tp: Literal["file", "bytes", "array"], filepath=None):
        if tp == "file":
            filepath = filepath or os.path.abspath("audio.mp3")
            mp.VideoFileClip(self.path).audio.write_audiofile(filepath)
            return filepath
        elif (tp == "bytes") or (tp == "array"):
            array = mp.VideoFileClip(self.path).audio.to_soundarray(fps=44100, nbytes=4)
            if tp == "array":
                return array
            else:
                bio = BytesIO()
                sf.write(bio, array, 44100, subtype="PCM_32", format="WAV")
                return bio.read()
    
    @staticmethod
    def _callback(complited, total): ...

    def get_ascii_frames(self, frame_size, callback=_callback):
        capture, al = cv2.VideoCapture(self.path), []
        capture.set(1, 1)

        frames_count = self.get_frames_count()

        for i in range(1, frames_count):
            callback(i, frames_count)
            ret, image_frame = capture.read()
            image_frame = Image.fromarray(image_frame)
            if ret:
                ac = "".join([ASCII_CHARS[pixel // 25] for pixel in image_frame.convert("L").resize(frame_size).getdata()])
                al.append("\n".join([ac[index:(index+frame_size[0])] for index in range(0, len(ac), frame_size[0])]))
            else:
                break
        
        return al
