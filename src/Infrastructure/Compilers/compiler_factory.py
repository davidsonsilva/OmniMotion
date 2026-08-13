from typing import Type
from src.Application.Interfaces.artifact_compiler import IArtifactCompiler
from src.Infrastructure.Compilers.mp4_compiler import MP4VideoCompiler
from src.Infrastructure.Compilers.astro_compiler import AstroComponentCompiler


class CompilerFactory:
    """
    Factory using Strategy Pattern to instantiate compilers for different output targets.
    Respects Open-Closed Principle (OCP) by allowing dynamic registration of new compilers.
    """

    def __init__(self) -> None:
        self._registry: dict[str, Type[IArtifactCompiler] | IArtifactCompiler] = {}
        # Default registrations
        self.register_compiler("mp4", MP4VideoCompiler)
        self.register_compiler("video", MP4VideoCompiler)
        self.register_compiler("astro", AstroComponentCompiler)
        self.register_compiler("ui", AstroComponentCompiler)

    def register_compiler(
        self, target_type: str, compiler: Type[IArtifactCompiler] | IArtifactCompiler
    ) -> None:
        normalized = target_type.strip().lower()
        self._registry[normalized] = compiler

    def get_compiler(self, target_type: str) -> IArtifactCompiler:
        normalized = target_type.strip().lower()
        if normalized not in self._registry:
            valid_targets = ", ".join(sorted(self._registry.keys()))
            raise ValueError(
                f"Unsupported compilation target '{target_type}'. Supported targets: [{valid_targets}]"
            )

        item = self._registry[normalized]
        if isinstance(item, type):
            return item()
        return item
