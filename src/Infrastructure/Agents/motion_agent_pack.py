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
            role="Analista Sênior de Motion Design e Visão Computacional",
            goal="Analisar os frames do vídeo fornecido e extrair com precisão matemática a física, a estrutura de camadas e a linha do tempo do movimento.",
            backstory="Você é um engenheiro especialista em engenharia reversa visual. Sua habilidade é analisar vídeos de interfaces digitais e rastrear elementos. Você deve identificar camadas sobrepostas (como overlays de webcam/Picture-in-Picture), capturar cantos arredondados (border-radius), opacidade, e mapear os tempos exatos em milissegundos de cada animação, estimando as curvas Bézier (Ease-in, Ease-out, etc.).",
        )
    )

    data_structuralist: AgentRole = field(
        default_factory=lambda: AgentRole(
            name="Data Structuralist",
            role="Arquiteto de Design System e Engenheiro de Dados",
            goal="Traduzir a análise bruta de movimento do Vision Agent em um esquema estruturado Pydantic que alimentará a nossa entidade 'MotionTimeline'.",
            backstory="Você é obcecado por padronização e tokens de design. Sua tarefa é pegar os metadados brutos gerados pelo especialista de movimento e envelopá-los estritamente nas classes Pydantic que representam nossas entidades do Domain (MediaLayer, Dimensions, MotionTimeline), ignorando qualquer ruído visual e gerando o JSON final perfeitamente limpo.",
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
