from abc import ABC, abstractmethod
from src.Domain.Entities.motion_timeline import MotionTimeline


class IVideoAnalyzer(ABC):
    @abstractmethod
    def analyze_video(self, video_path: str) -> MotionTimeline:
        """
        Analyzes a input video file and extracts its motion timeline and layout specification.
        """
        pass
