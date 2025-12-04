from typing import Optional


class LLMService:
    def __init__(self, provider: str = "none"):
        self.provider = provider

    def explain(self, query: str, title: str) -> Optional[str]:
        return f"Relevant because it matches entities/themes in query '{query}'. Article: {title}."
