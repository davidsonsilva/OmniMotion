from unittest.mock import MagicMock
import pytest
from src.Application.Interfaces.artifact_compiler import IArtifactCompiler
from src.Domain.Entities.motion_timeline import MotionTimeline
from src.Infrastructure.Compilers.compiler_factory import CompilerFactory
from src.Infrastructure.Compilers.mp4_compiler import MP4VideoCompiler
from src.Infrastructure.Compilers.astro_compiler import AstroComponentCompiler


def test_compiler_factory_default_registrations():
    factory = CompilerFactory()

    mp4_compiler = factory.get_compiler("mp4")
    assert isinstance(mp4_compiler, MP4VideoCompiler)

    astro_compiler = factory.get_compiler("astro")
    assert isinstance(astro_compiler, AstroComponentCompiler)


def test_compiler_factory_unsupported_target():
    factory = CompilerFactory()
    with pytest.raises(ValueError, match="Unsupported compilation target"):
        factory.get_compiler("invalid_target")


def test_compiler_factory_dynamic_registration_ocp():
    factory = CompilerFactory()

    class CustomGifCompiler(IArtifactCompiler):
        def compile(self, timeline, output_path, config=None):
            return f"GIF:{output_path}"

    factory.register_compiler("gif", CustomGifCompiler)
    gif_compiler = factory.get_compiler("gif")

    assert isinstance(gif_compiler, CustomGifCompiler)

    timeline = MotionTimeline(timeline_id="t1", name="Test", duration_ms=1000)
    result = gif_compiler.compile(timeline, "/output/demo.gif")
    assert result == "GIF:/output/demo.gif"
