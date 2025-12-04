class BaseAgent:
    def __init__(self, **kwargs):
        self.ctx = kwargs

    def run(self, state: dict) -> dict:
        return state
