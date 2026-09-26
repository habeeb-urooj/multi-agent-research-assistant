from langchain_openrouter import ChatOpenRouter

from app.config.settings import (
    OPENROUTER_API_KEY,
    PLANNER_MODEL,
)


class PlannerAgent:
    """
    Responsible for breaking a user's research query
    into smaller research tasks.
    """

    def __init__(self):
        self.llm = ChatOpenRouter(
            model=PLANNER_MODEL,
            temperature=0,
            api_key=OPENROUTER_API_KEY,
            max_tokens=800,
        )

    def plan(self, query: str) -> list[str]:

        prompt = f"""
You are the Planning Agent in a multi-agent research assistant.

Break the user's research question into exactly 3 clear,
specific and independently researchable tasks.

Research question:
{query}

Return ONLY the tasks, one task per line.

Do not number them.
Do not add explanations.
"""

        response = self.llm.invoke(prompt)

        tasks = [
            line.strip()
            for line in response.content.splitlines()
            if line.strip()
        ]

        return tasks[:3]
