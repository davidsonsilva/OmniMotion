from typing import Any, Callable
from src.Application.Interfaces.artifact_compiler import IArtifactCompiler
from src.Domain.Entities.motion_timeline import MotionTimeline


class CompileArtifactUseCase:
    def __init__(
        self,
        compiler_resolver: Callable[[str], IArtifactCompiler] | None = None,
        default_compiler: IArtifactCompiler | None = None,
    ) -> None:
        self._compiler_resolver = compiler_resolver
        self._default_compiler = default_compiler

    def execute(
        self,
        timeline: MotionTimeline,
        target_type: str,
        output_path: str,
        config: dict[str, Any] | None = None,
    ) -> str:
        if not isinstance(timeline, MotionTimeline):
            raise TypeError("timeline must be an instance of MotionTimeline.")
        if not target_type or not target_type.strip():
            raise ValueError("target_type cannot be empty.")
        if not output_path or not output_path.strip():
            raise ValueError("output_path cannot be empty.")

        compiler: IArtifactCompiler | None = None
        if self._compiler_resolver:
            compiler = self._compiler_resolver(target_type)
        elif self._default_compiler:
            compiler = self._default_compiler

        if not compiler:
            raise ValueError(f"No compiler found for target type: '{target_type}'")

        return compiler.compile(timeline=timeline, output_path=output_path, config=config)
