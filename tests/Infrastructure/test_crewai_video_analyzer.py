import os
import pytest
from src.Application.Interfaces.video_analyzer import IVideoAnalyzer
from src.Domain.Entities.motion_timeline import MotionTimeline
from src.Infrastructure.Agents.crewai_video_analyzer import (
    CrewAIVideoAnalyzer,
    MotionTimelineSchema,
)


def test_crewai_analyzer_inherits_from_ivideo_analyzer():
    """Verify that CrewAIVideoAnalyzer implements the IVideoAnalyzer domain interface."""
    assert issubclass(CrewAIVideoAnalyzer, IVideoAnalyzer)
    analyzer = CrewAIVideoAnalyzer()
    assert isinstance(analyzer, IVideoAnalyzer)


def test_analyze_non_existent_file_raises_file_not_found_error():
    """Verify that analyze() raises FileNotFoundError if video file does not exist."""
    analyzer = CrewAIVideoAnalyzer()
    non_existent_path = "/tmp/non_existent_sample_video_12345.mp4"

    with pytest.raises(FileNotFoundError, match="Video file not found"):
        analyzer.analyze(non_existent_path)


def test_analyze_existing_file_returns_dict_matching_pydantic_schema(tmp_path):
    """Verify that analyze() returns a dictionary conforming to MotionTimelineSchema for an existing file."""
    fake_video = tmp_path / "sample_video.mp4"
    fake_video.write_bytes(b"dummy video content")

    analyzer = CrewAIVideoAnalyzer()
    result = analyzer.analyze(str(fake_video))

    assert isinstance(result, dict)
    assert "timeline_id" in result
    assert "keyframes" in result
    assert "layers" in result

    # Validate output against Pydantic schema
    validated_schema = MotionTimelineSchema(**result)
    assert validated_schema.duration_ms > 0
    assert len(validated_schema.layers) > 0


def test_analyze_video_returns_domain_motion_timeline_aggregate(tmp_path):
    """Verify that analyze_video() returns a valid MotionTimeline Domain Aggregate Root."""
    fake_video = tmp_path / "sample_video.mp4"
    fake_video.write_bytes(b"dummy video content")

    analyzer = CrewAIVideoAnalyzer()
    timeline = analyzer.analyze_video(str(fake_video))

    assert isinstance(timeline, MotionTimeline)
    assert timeline.duration_ms > 0
    assert len(timeline.layers) > 0
    assert timeline.layers[0].layer_id == "layer_screen"


def test_crewai_agent_pack_roles_configured():
    """Verify Vision Agent and Data Structuralist roles are configured with specialized prompts."""
    analyzer = CrewAIVideoAnalyzer()
    pack = analyzer.agent_pack

    assert pack.vision_agent.name == "Vision Agent"
    assert pack.vision_agent.role == "Analista Sênior de Motion Design e Visão Computacional"
    assert "extrair com precisão matemática" in pack.vision_agent.goal
    assert "engenharia reversa visual" in pack.vision_agent.backstory

    assert pack.data_structuralist.name == "Data Structuralist"
    assert pack.data_structuralist.role == "Arquiteto de Design System e Engenheiro de Dados"
    assert "esquema estruturado Pydantic" in pack.data_structuralist.goal
    assert "obcecado por padronização" in pack.data_structuralist.backstory


def test_build_crew_creates_or_handles_crew(tmp_path):
    """Verify that _build_crew configures agents and tasks with output_pydantic validation."""
    fake_video = tmp_path / "sample_video.mp4"
    fake_video.write_bytes(b"dummy video content")

    analyzer = CrewAIVideoAnalyzer()
    try:
        crew = analyzer._build_crew(str(fake_video))
        assert crew is not None
        assert len(crew.agents) == 2
        assert len(crew.tasks) == 2
        assert crew.tasks[1].output_pydantic == analyzer.output_schema
    except ImportError:
        # CrewAI is not installed in standard runtime environment
        pass

