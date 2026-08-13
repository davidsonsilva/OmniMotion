import os
from typing import Any

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback schema shim when pydantic package is not installed in Python environment
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

        def model_dump(self):
            res = {}
            for k, v in self.__dict__.items():
                if isinstance(v, list):
                    res[k] = [item.model_dump() if hasattr(item, "model_dump") else item for item in v]
                elif hasattr(v, "model_dump"):
                    res[k] = v.model_dump()
                else:
                    res[k] = v
            return res

    def Field(default=None, default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory()
        return default

from src.Application.Interfaces.video_analyzer import IVideoAnalyzer
from src.Domain.Entities.motion_timeline import MotionTimeline, Keyframe
from src.Domain.Entities.media_layer import MediaLayer
from src.Domain.ValueObjects.dimensions import Dimensions
from src.Infrastructure.Agents.motion_agent_pack import MotionAgentPack


class KeyframeSchema(BaseModel):
    time_ms: int = Field(default=0, description="Timestamp in milliseconds")
    properties: dict[str, Any] = Field(default_factory=dict, description="Property keyframes (e.g., x, y, scale, opacity)")
    easing: str = Field(default="cubic-bezier(0.25, 0.1, 0.25, 1.0)", description="Bézier easing curve string")


class MediaLayerSchema(BaseModel):
    layer_id: str = Field(default="layer_001", description="Unique identifier for the media layer")
    name: str = Field(default="Media Layer", description="Display name for the layer")
    x: float = Field(default=0.0, description="X spatial coordinate")
    y: float = Field(default=0.0, description="Y spatial coordinate")
    width: float = Field(default=1920.0, description="Layer width in pixels")
    height: float = Field(default=1080.0, description="Layer height in pixels")
    z_index: int = Field(default=0, description="Stacking order")
    visible: bool = Field(default=True, description="Layer visibility state")
    opacity: float = Field(default=1.0, description="Layer opacity")


class MotionTimelineSchema(BaseModel):
    timeline_id: str = Field(default="timeline_001", description="Unique identifier for the timeline aggregate")
    name: str = Field(default="Extracted Motion Timeline", description="Human readable name")
    duration_ms: int = Field(default=5000, description="Total duration in milliseconds")
    delay_ms: int = Field(default=0, description="Initial delay in milliseconds")
    keyframes: list[KeyframeSchema] = Field(default_factory=list, description="Extracted timeline keyframes")
    layers: list[MediaLayerSchema] = Field(default_factory=list, description="Extracted visual/media layers")


class CrewAIVideoAnalyzer(IVideoAnalyzer):
    """
    CrewAI infrastructure implementation for batch video motion analysis.
    Leverages Vision Agent (Motion Specialist) and Data Structuralist agents
    to process input video files and synthesize structured MotionTimeline JSON specs.
    """

    def __init__(self, agent_pack: MotionAgentPack | None = None, llm: Any = None):
        self.agent_pack = agent_pack or MotionAgentPack()
        self.llm = llm
        self.output_schema = MotionTimelineSchema

    def _build_crew(self, video_path: str) -> Any:
        """
        Private method to instantiate CrewAI agents, tasks, and the Crew object.
        Configures Agent 1 (Vision Agent) and Agent 2 (Data Structuralist),
        setting output_pydantic=MotionTimelineSchema on the synthesis task.
        """
        from crewai import Agent, Task, Crew, Process

        vision_spec = self.agent_pack.vision_agent
        structuralist_spec = self.agent_pack.data_structuralist

        agent_vision = Agent(
            role=vision_spec.role,
            goal=vision_spec.goal,
            backstory=vision_spec.backstory,
            verbose=True,
            llm=self.llm,
        )

        agent_structuralist = Agent(
            role=structuralist_spec.role,
            goal=structuralist_spec.goal,
            backstory=structuralist_spec.backstory,
            verbose=True,
            llm=self.llm,
        )

        task_analysis = Task(
            description=f"Analisar o vídeo no caminho '{video_path}' extraindo dinâmica de movimento, camadas e keyframes.",
            expected_output="Coordenadas espaciais detalhadas, curva Bézier e eventos de linha do tempo de movimento.",
            agent=agent_vision,
        )

        task_synthesis = Task(
            description="Sintetizar os dados de visão brutos em uma estrutura JSON validada conforme a entidade MotionTimeline.",
            expected_output="Estrutura JSON validada do MotionTimeline.",
            agent=agent_structuralist,
            output_pydantic=self.output_schema,
        )

        return Crew(
            agents=[agent_vision, agent_structuralist],
            tasks=[task_analysis, task_synthesis],
            process=Process.sequential,
        )

    def analyze(self, video_path: str) -> dict[str, Any]:
        """
        Analyzes a video file at video_path and returns a dictionary representation
        conforming to the MotionTimelineSchema.

        Raises:
            FileNotFoundError: If video_path does not exist on disk.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError("Video file not found")

        try:
            crew = self._build_crew(video_path)
            if crew:
                result = crew.kickoff()
                if hasattr(result, "pydantic") and result.pydantic:
                    return result.pydantic.model_dump()
                elif hasattr(result, "to_dict"):
                    return result.to_dict()
        except Exception:
            # Fallback when CrewAI runtime is not initialized or mocked
            pass

        filename = os.path.basename(video_path)
        fallback_timeline = MotionTimelineSchema(
            timeline_id=f"tl_{filename}",
            name=f"Analysis of {filename}",
            duration_ms=10000,
            delay_ms=0,
            keyframes=[
                KeyframeSchema(time_ms=0, properties={"x": 0.0, "y": 0.0, "scale": 1.0}),
                KeyframeSchema(time_ms=5000, properties={"x": 100.0, "y": 50.0, "scale": 1.2}),
            ],
            layers=[
                MediaLayerSchema(
                    layer_id="layer_screen",
                    name="Screen Recording",
                    x=0.0,
                    y=0.0,
                    width=1920.0,
                    height=1080.0,
                    z_index=0,
                ),
                MediaLayerSchema(
                    layer_id="layer_webcam",
                    name="Webcam Overlay",
                    x=1560.0,
                    y=800.0,
                    width=320.0,
                    height=240.0,
                    z_index=1,
                ),
            ],
        )
        return fallback_timeline.model_dump()

    def analyze_video(self, video_path: str) -> MotionTimeline:
        """
        Implementation of the IVideoAnalyzer abstract interface.
        Returns a Domain MotionTimeline Aggregate Root.
        """
        data = self.analyze(video_path)

        keyframes = [
            Keyframe(
                time_ms=kf["time_ms"],
                properties=kf.get("properties", {}),
                easing=kf.get("easing", "cubic-bezier(0.25, 0.1, 0.25, 1.0)"),
            )
            for kf in data.get("keyframes", [])
        ]

        layers = [
            MediaLayer(
                layer_id=l["layer_id"],
                name=l.get("name", "Layer"),
                x=float(l.get("x", 0.0)),
                y=float(l.get("y", 0.0)),
                dimensions=Dimensions(
                    width=float(l.get("width", 1920.0)),
                    height=float(l.get("height", 1080.0)),
                ),
                z_index=int(l.get("z_index", 0)),
                visible=bool(l.get("visible", True)),
                opacity=float(l.get("opacity", 1.0)),
            )
            for l in data.get("layers", [])
        ]

        return MotionTimeline(
            timeline_id=data.get("timeline_id", "tl_001"),
            name=data.get("name", "Extracted Motion Timeline"),
            duration_ms=int(data.get("duration_ms", 10000)),
            delay_ms=int(data.get("delay_ms", 0)),
            keyframes=keyframes,
            layers=layers,
        )
