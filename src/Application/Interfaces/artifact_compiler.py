from abc import ABC, abstractmethod
from typing import Any
from src.Domain.Entities.motion_timeline import MotionTimeline


class IArtifactCompiler(ABC):
    @abstractmethod
    def compile(
        self,
        timeline: MotionTimeline,
        output_path: str,
        config: dict[str, Any] | None = None,
    ) -> str:
        """
        Compiles a MotionTimeline into a target output artifact (e.g. MP4 video, Astro component code).
        Returns the path to the compiled artifact or generated code content.
        """
        pass
