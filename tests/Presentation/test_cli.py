import os
import json
import pytest
from src.Presentation.CLI.main import main, format_timeline_dict
from src.Domain.Entities.motion_timeline import MotionTimeline, Keyframe
from src.Domain.Entities.media_layer import MediaLayer
from src.Domain.ValueObjects.dimensions import Dimensions


def test_cli_missing_video_argument_raises_system_exit():
    """Verify that CLI raises SystemExit when --video argument is omitted."""
    with pytest.raises(SystemExit):
        main([])


def test_cli_non_existent_video_file_raises_file_not_found():
    """Verify that CLI raises FileNotFoundError for non-existent video path."""
    with pytest.raises(FileNotFoundError, match="Video file not found"):
        main(["--video", "/tmp/non_existent_test_video_9999.mp4"])


def test_cli_valid_video_executes_use_case_and_outputs_dict(tmp_path, capsys):
    """Verify that CLI runs successfully with valid video input and prints JSON output."""
    dummy_video = tmp_path / "input_demo.mp4"
    dummy_video.write_bytes(b"mock video data")

    os.environ["GEMINI_API_KEY"] = "mock_gemini_key_for_testing"

    result = main(["--video", str(dummy_video)])

    captured = capsys.readouterr()
    assert captured.out != ""
    
    # Parse output to confirm it's valid JSON
    json_output = json.loads(captured.out)
    assert "timeline_id" in json_output
    assert "layers" in json_output
    assert "keyframes" in json_output
    assert result["timeline_id"] == json_output["timeline_id"]


def test_format_timeline_dict_structure():
    """Verify format_timeline_dict maps MotionTimeline domain entities accurately."""
    timeline = MotionTimeline(
        timeline_id="tl_test_001",
        name="Test Timeline",
        duration_ms=5000,
        delay_ms=100,
        keyframes=[Keyframe(time_ms=0, properties={"scale": 1.0})],
        layers=[
            MediaLayer(
                layer_id="layer_01",
                name="Main Screen",
                x=10.0,
                y=20.0,
                dimensions=Dimensions(width=1920.0, height=1080.0),
            )
        ],
    )

    formatted = format_timeline_dict(timeline)

    assert formatted["timeline_id"] == "tl_test_001"
    assert formatted["name"] == "Test Timeline"
    assert formatted["duration_ms"] == 5000
    assert formatted["delay_ms"] == 100
    assert len(formatted["keyframes"]) == 1
    assert formatted["keyframes"][0]["properties"]["scale"] == 1.0
    assert len(formatted["layers"]) == 1
    assert formatted["layers"][0]["layer_id"] == "layer_01"
    assert formatted["layers"][0]["width"] == 1920.0
    assert formatted["layers"][0]["height"] == 1080.0
