from src.Application.Interfaces.video_analyzer import IVideoAnalyzer
from src.Domain.Entities.motion_timeline import MotionTimeline


class ExtractLayoutSpecificationUseCase:
    def __init__(self, analyzer: IVideoAnalyzer) -> None:
        if not isinstance(analyzer, IVideoAnalyzer):
            raise TypeError("analyzer must implement IVideoAnalyzer interface.")
        self._analyzer = analyzer

    def execute(self, video_path: str) -> MotionTimeline:
        if not video_path or not video_path.strip():
            raise ValueError("video_path cannot be empty.")
        return self._analyzer.analyze_video(video_path)
