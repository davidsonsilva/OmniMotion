from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRole:
    name: str
    role: str
    goal: str
    backstory: str


@dataclass
class MotionAgentPack:
    """
    CrewAI / Multi-Agent Pack for OmniMotion.
    Structures specialized AI agents to analyze video motion, synthesize timeline data,
    and integrate with UI design systems.
    """

    vision_agent: AgentRole = field(
        default_factory=lambda: AgentRole(
            name="Vision Agent",
            role="Computer Vision & Motion Frame Analyst",
            goal="Extract frame layout, spatial coordinates, webcam overlays, and animation keyframes from video input.",
            backstory="Expert computer vision specialist trained on video frame analysis, optical flow, and bounding box detection.",
        )
    )

    data_structuralist: AgentRole = field(
        default_factory=lambda: AgentRole(
            name="Data Structuralist",
            role="Motion Timeline Synthesizer",
            goal="Convert raw visual metadata into mathematical Domain MotionTimeline Aggregate Roots and Bézier curves.",
            backstory="Mathematical modeling specialist ensuring clean data representations, accurate timing in milliseconds, and zero domain leakage.",
        )
    )

    ui_integrator: AgentRole = field(
        default_factory=lambda: AgentRole(
            name="UI Integrator",
            role="Design System & Code Compiler",
            goal="Cross-reference extracted motion specs with target Design Systems and trigger artifact compilers.",
            backstory="Frontend design system architect fluent in Astro, Tailwind CSS, Motion primitives, and Picture-in-Picture video layouts.",
        )
    )

    def get_all_agents(self) -> list[AgentRole]:
        return [self.vision_agent, self.data_structuralist, self.ui_integrator]

    def create_crewai_agents(self, llm: Any = None) -> list[Any]:
        """
        Factory method to instantiate official CrewAI Agent objects when crewai library is initialized.
        Gracefully handles environments where crewai is imported or mocked.
        """
        try:
            from crewai import Agent

            agents = []
            for agent_role in self.get_all_agents():
                agent_kwargs = {
                    "role": agent_role.role,
                    "goal": agent_role.goal,
                    "backstory": agent_role.backstory,
                    "verbose": True,
                }
                if llm:
                    agent_kwargs["llm"] = llm
                agents.append(Agent(**agent_kwargs))
            return agents
        except (ImportError, Exception):
            # Fallback for lightweight testing or stub environments
            return self.get_all_agents()
