from unittest.mock import MagicMock
import pytest
from src.Application.Interfaces.video_analyzer import IVideoAnalyzer
from src.Application.UseCases.extract_layout_specification import (
    ExtractLayoutSpecificationUseCase,
)
from src.Domain.Entities.motion_timeline import MotionTimeline


def test_extract_layout_specification_success():
    # Mock analyzer implementing IVideoAnalyzer
    mock_analyzer = MagicMock(spec=IVideoAnalyzer)
    expected_timeline = MotionTimeline(
        timeline_id="extracted-1",
        name="Extracted Screen Recording Motion",
        duration_ms=4000,
    )
    mock_analyzer.analyze_video.return_value = expected_timeline

    use_case = ExtractLayoutSpecificationUseCase(analyzer=mock_analyzer)
    result = use_case.execute(video_path="/path/to/demo_video.mp4")

    assert result == expected_timeline
    mock_analyzer.analyze_video.assert_called_once_with("/path/to/demo_video.mp4")


def test_extract_layout_specification_invalid_analyzer():
    with pytest.raises(TypeError, match="must implement IVideoAnalyzer"):
        ExtractLayoutSpecificationUseCase(analyzer="not_an_analyzer")  # type: ignore


def test_extract_layout_specification_empty_path():
    mock_analyzer = MagicMock(spec=IVideoAnalyzer)
    use_case = ExtractLayoutSpecificationUseCase(analyzer=mock_analyzer)

    with pytest.raises(ValueError, match="video_path cannot be empty"):
        use_case.execute(video_path="")
