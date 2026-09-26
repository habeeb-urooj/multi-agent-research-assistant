from langchain_openrouter import ChatOpenRouter

from app.config.settings import (
    OPENROUTER_API_KEY,
    CRITIC_MODEL,
)


class CriticAgent:

    def __init__(self):
        self.llm = ChatOpenRouter(
            model=CRITIC_MODEL,
            temperature=0.1,
            api_key=OPENROUTER_API_KEY,
            max_tokens=1000,
        )

    def critique(self, task: str, research_result: str) -> str:

        prompt = f"""
You are the Critic / Fact-Checker Agent in a multi-agent research assistant.

CURRENT DATE:
2026-09-25

Your job is to critically evaluate the research produced by another agent.

RESEARCH TASK:
{task}

RESEARCH RESULT:
{research_result}

Evaluate the research carefully.

Check for:

1. Factual support
   - Are important claims supported by the provided evidence?
   - Are there unsupported claims?

2. Source quality
   - Are source URLs present where appropriate?
   - Are claims attributed to identifiable sources?
   - Does the cited source appear relevant to the claim?

3. Publication dates
   - Treat sources dated on or before 2026-09-25 as potentially current.
   - Only identify a source as future-dated if its publication date is actually after 2026-09-25.
   - Do not assume the current date yourself.

4. Contradictions
   - Are there conflicting claims?
   - If so, identify them clearly.

5. Hallucinations
   - Identify claims that appear invented, exaggerated, or unsupported.

6. Completeness
   - Identify important aspects of the research task that were missed.

7. Uncertainty
   - Identify claims that should be presented with uncertainty.

IMPORTANT RULES:
- Do not invent new facts or sources.
- Do not perform additional web searches.
- Only evaluate the research provided above.
- Do not rewrite the entire research result.
- Be specific about problems you identify.
- If the research is well-supported, explicitly say so.
- Clearly separate supported claims from questionable claims.
- Do not call valid 2026 sources future-dated merely because they are dated 2026.

Return your evaluation using this structure:

VERDICT:
[PASS / PASS WITH WARNINGS / FAIL]

SUPPORTED CLAIMS:
- ...

QUESTIONABLE OR UNSUPPORTED CLAIMS:
- ...

SOURCE ISSUES:
- ...

CONTRADICTIONS:
- ...

MISSING INFORMATION:
- ...

RECOMMENDATIONS FOR SYNTHESIZER:
- ...
"""

        response = self.llm.invoke(prompt)

        return response.content
