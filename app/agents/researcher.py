from langchain_openrouter import ChatOpenRouter

from app.config.settings import (
    OPENROUTER_API_KEY,
    RESEARCHER_MODEL,
)

from app.tools.web_search import SearXNGSearch


class ResearchAgent:

    def __init__(self):
        self.llm = ChatOpenRouter(
            api_key=OPENROUTER_API_KEY,
            model=RESEARCHER_MODEL,
            temperature=0.2,
            max_tokens=1500,
        )

        self.search = SearXNGSearch()

    def research(self, task: str) -> str:

        # Step 1: Search the web
        search_results = self.search.search(
            query=task,
            max_results=5,
        )

        # Step 2: Handle unavailable web evidence
        if not search_results:
            return (
                "WEB SEARCH FAILURE\n\n"
                "No web evidence could be retrieved for this "
                "research task because the search service was "
                "temporarily unavailable.\n\n"
                "Do not treat this task as researched. "
                "The Synthesizer should not present unsupported "
                "claims as factual."
            )

        # Step 3: Format retrieved evidence
        sources = []

        for result in search_results:
            sources.append(
                f"""
Title: {result.get('title', '')}
URL: {result.get('url', '')}
Content: {result.get('content', '')}
"""
            )

        evidence = "\n".join(sources)

        # Step 4: Ask the LLM to analyze the evidence
        prompt = f"""
You are the Research Agent in a multi-agent research assistant.

Research task:
{task}

Below are web search results retrieved from SearXNG.

WEB SOURCES:
{evidence}

Your job is to analyze these sources and produce a reliable research finding.

Requirements:
- Base your response primarily on the provided web sources.
- Clearly distinguish facts from assumptions.
- Do not invent facts or sources.
- Do not claim something is true if the provided evidence does not support it.
- Identify important information relevant to the research task.
- Keep the response concise but meaningful.
- Include the source URL when making an important factual claim.
- If the sources are insufficient to support a claim, explicitly say so.
"""

        response = self.llm.invoke(prompt)

        return response.content
