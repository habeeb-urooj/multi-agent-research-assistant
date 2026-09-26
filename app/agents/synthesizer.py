from langchain_openrouter import ChatOpenRouter

from app.config.settings import (
    OPENROUTER_API_KEY,
    SYNTHESIZER_MODEL,
)


class SynthesizerAgent:

    def __init__(self):
        self.llm = ChatOpenRouter(
            model=SYNTHESIZER_MODEL,
            temperature=0.2,
            api_key=OPENROUTER_API_KEY,
            max_tokens=1500,
        )

    def synthesize(self, query: str, research_results: list[dict]) -> str:

        findings = []

        for item in research_results:

            research_text = item.get("result", "")
            critique_text = item.get("critique", "")

            # Protect the OpenRouter budget from unexpectedly large context
            research_text = research_text[:1800]
            critique_text = critique_text[:800]

            findings.append(
                f"""
RESEARCH TASK:
{item.get("task", "")}

RESEARCH FINDING:
{research_text}

CRITIC EVALUATION:
{critique_text}
"""
            )

        combined_findings = "\n".join(findings)

        prompt = f"""
You are the Synthesizer Agent in a multi-agent research assistant.

USER RESEARCH QUESTION:
{query}

Below are research findings and their critic evaluations.

RESEARCH MATERIAL:
{combined_findings}

Your job is to produce a reliable final answer to the user's research question.

Requirements:

1. Synthesize the strongest supported findings.
2. Give priority to claims supported by the research evidence.
3. Respect warnings and failures identified by the Critic Agent.
4. Do not invent facts, statistics, sources, or citations.
5. Do not treat unsupported claims as facts.
6. Mention uncertainty where appropriate.
7. Resolve contradictions carefully. If they cannot be resolved, state the disagreement.
8. Include relevant source URLs from the research material.
9. Do not mention internal agents, prompts, token limits, or the pipeline.
10. Write a clear, professional answer that directly addresses the user's question.

Structure the answer with:

- A concise overview
- Key findings
- Important considerations or limitations
- Sources

Do not simply copy the research findings.
Synthesize them into a coherent final response.
"""

        response = self.llm.invoke(prompt)

        return response.content
