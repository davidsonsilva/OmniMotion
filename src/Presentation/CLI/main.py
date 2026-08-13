import argparse
import json
import os
import sys
from typing import Any

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.Application.UseCases.extract_layout_specification import (
    ExtractLayoutSpecificationUseCase,
)
from src.Infrastructure.Agents.crewai_video_analyzer import CrewAIVideoAnalyzer


def format_timeline_dict(timeline: Any) -> dict[str, Any]:
    """Helper to convert MotionTimeline domain entity into a clean formatted dict."""
    return {
        "timeline_id": timeline.timeline_id,
        "name": timeline.name,
        "duration_ms": timeline.duration_ms,
        "delay_ms": timeline.delay_ms,
        "keyframes": [
            {
                "time_ms": kf.time_ms,
                "properties": kf.properties,
                "easing": kf.easing,
            }
            for kf in timeline.keyframes
        ],
        "layers": [
            {
                "layer_id": layer.layer_id,
                "name": layer.name,
                "x": layer.x,
                "y": layer.y,
                "width": layer.dimensions.width,
                "height": layer.dimensions.height,
                "z_index": layer.z_index,
                "visible": layer.visible,
                "opacity": layer.opacity,
            }
            for layer in timeline.layers
        ],
    }


def main(args_list: list[str] | None = None) -> dict[str, Any]:
    parser = argparse.ArgumentParser(
        description="OmniMotion CLI - Motion Design Video Extraction Pipeline"
    )
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Path to the input video file for motion analysis.",
    )

    args = parser.parse_args(args_list)

    api_key = os.getenv("GEMINI_API_KEY")

    # Instantiate Clean Architecture dependency tree
    analyzer = CrewAIVideoAnalyzer(llm=api_key)
    use_case = ExtractLayoutSpecificationUseCase(analyzer=analyzer)

    # Execute extraction Use Case
    timeline = use_case.execute(args.video)
    result_dict = format_timeline_dict(timeline)

    # Output formatted result
    print(json.dumps(result_dict, indent=2, ensure_ascii=False))
    return result_dict


if __name__ == "__main__":
    main()
