from unittest.mock import MagicMock
import pytest
from src.Application.Interfaces.artifact_compiler import IArtifactCompiler
from src.Application.UseCases.compile_artifact import CompileArtifactUseCase
from src.Domain.Entities.motion_timeline import MotionTimeline


def test_compile_artifact_with_default_compiler():
    mock_compiler = MagicMock(spec=IArtifactCompiler)
    mock_compiler.compile.return_value = "/output/video.mp4"

    timeline = MotionTimeline(timeline_id="tl-1", name="Demo", duration_ms=2000)
    use_case = CompileArtifactUseCase(default_compiler=mock_compiler)

    result = use_case.execute(
        timeline=timeline,
        target_type="mp4",
        output_path="/output/video.mp4",
        config={"rounded_corners": True},
    )

    assert result == "/output/video.mp4"
    mock_compiler.compile.assert_called_once_with(
        timeline=timeline,
        output_path="/output/video.mp4",
        config={"rounded_corners": True},
    )


def test_compile_artifact_with_compiler_resolver():
    mock_compiler_mp4 = MagicMock(spec=IArtifactCompiler)
    mock_compiler_mp4.compile.return_value = "/output/video.mp4"

    def resolver(target_type: str):
        if target_type == "mp4":
            return mock_compiler_mp4
        return None

    timeline = MotionTimeline(timeline_id="tl-1", name="Demo", duration_ms=2000)
    use_case = CompileArtifactUseCase(compiler_resolver=resolver)

    res = use_case.execute(timeline=timeline, target_type="mp4", output_path="/output/video.mp4")
    assert res == "/output/video.mp4"


def test_compile_artifact_unsupported_target():
    use_case = CompileArtifactUseCase()
    timeline = MotionTimeline(timeline_id="tl-1", name="Demo", duration_ms=2000)

    with pytest.raises(ValueError, match="No compiler found for target type"):
        use_case.execute(timeline=timeline, target_type="unsupported", output_path="/out")


def test_compile_artifact_invalid_inputs():
    use_case = CompileArtifactUseCase()
    timeline = MotionTimeline(timeline_id="tl-1", name="Demo", duration_ms=2000)

    with pytest.raises(TypeError, match="timeline must be an instance of MotionTimeline"):
        use_case.execute(timeline="not_a_timeline", target_type="mp4", output_path="/out")  # type: ignore

    with pytest.raises(ValueError, match="target_type cannot be empty"):
        use_case.execute(timeline=timeline, target_type="", output_path="/out")

    with pytest.raises(ValueError, match="output_path cannot be empty"):
        use_case.execute(timeline=timeline, target_type="mp4", output_path="  ")
