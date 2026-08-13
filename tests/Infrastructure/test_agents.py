from src.Infrastructure.Agents.motion_agent_pack import MotionAgentPack, AgentRole


def test_motion_agent_pack_roles():
    pack = MotionAgentPack()
    agents = pack.get_all_agents()

    assert len(agents) == 3
    assert agents[0].name == "Vision Agent"
    assert agents[1].name == "Data Structuralist"
    assert agents[2].name == "UI Integrator"


def test_motion_agent_pack_creation():
    pack = MotionAgentPack()
    agents = pack.create_crewai_agents()

    assert len(agents) == 3
    for agent in agents:
        if isinstance(agent, AgentRole):
            assert hasattr(agent, "role")
            assert hasattr(agent, "goal")
            assert hasattr(agent, "backstory")
