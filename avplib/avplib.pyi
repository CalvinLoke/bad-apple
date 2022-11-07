from io import BufferedReader
from numpy import ndarray
from typing import overload, List, Tuple, Literal, Any

PATH = str
WAV_FILE_BYTES = bytes

class AVP:
    @overload
    def __init__(self, fp: str) -> None: ...
    @overload
    def __init__(self, fp: bytes) -> None: ...
    @overload
    def __init__(self, fp: BufferedReader) -> None: ...
    def get_frames_count(self) -> int:
        """Returns the number of `frames`"""
        ...
    @staticmethod
    def _callback(complited: int, total: int) -> None: ...
    def get_ascii_frames(self, frame_size: Tuple[int, int], callback=_callback) -> List[str]: ...
    @overload
    def get_audio(self, tp: Literal["file"], filepath: str=None) -> PATH: ...
    @overload
    def get_audio(self, tp: Literal["bytes"]) -> WAV_FILE_BYTES: ...
    @overload
    def get_audio(self, tp: Literal["array"]) -> ndarray: ...
    @overload
    def get_audio(self, tp: Any) -> None: ...