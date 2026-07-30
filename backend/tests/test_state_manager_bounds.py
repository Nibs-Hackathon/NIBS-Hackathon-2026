from mao.core.state_manager import StateManager


def test_agent_memory_is_bounded():
    state = StateManager()

    for index in range(1200):
        state.add_memory({"index": index})

    assert len(state.get_memory()) == 1000
    assert state.get_memory()[0] == {"index": 200}
