from concurrent.futures import ThreadPoolExecutor, as_completed

from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent
from app.agents.critic import CriticAgent
from app.agents.synthesizer import SynthesizerAgent

from app.config.limits import (
    MAX_QUERY_LENGTH,
    MAX_RESEARCH_TASKS,
    PIPELINE_ENABLED,
)


class ResearchPipeline:
    """
    Orchestrates the multi-agent research process.

    Flow:

    User Query
        ↓
    Planner Agent
        ↓
    ┌─────────────────────────────────────┐
    │ Parallel Research + Critic Branches │
    │                                     │
    │ Research 1 → Critic 1               │
    │ Research 2 → Critic 2               │
    │ Research 3 → Critic 3               │
    └─────────────────────────────────────┘
        ↓
    Synthesizer Agent
        ↓
    Final Answer
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.critic = CriticAgent()
        self.synthesizer = SynthesizerAgent()

    def _research_and_critic(
        self,
        task: str,
        index: int,
    ) -> dict:
        """
        Execute one Researcher → Critic branch.
        """

        print(
            f"[RESEARCHER {index}] Researching:"
        )
        print(f"  {task}")

        research_result = self.researcher.research(task)

        print(
            f"[RESEARCHER {index}] "
            f"✓ Research completed"
        )

        print(
            f"[CRITIC {index}] "
            f"Fact-checking research..."
        )

        critique = self.critic.critique(
            task=task,
            research_result=research_result,
        )

        verdict = "UNKNOWN"

        for line in critique.splitlines():
            if line.strip().startswith("VERDICT:"):
                verdict = line.split(":", 1)[1].strip()
                break

        print(
            f"[CRITIC {index}] "
            f"✓ Verdict: {verdict}"
        )

        return {
            "task": task,
            "result": research_result,
            "critique": critique,
        }

    def run(self, query: str):

        # ==========================================
        # SAFETY CHECKS
        # ==========================================

        if not PIPELINE_ENABLED:
            raise RuntimeError(
                "Research pipeline is temporarily disabled."
            )

        if not query or not query.strip():
            raise ValueError(
                "Research query cannot be empty."
            )

        query = query.strip()

        if len(query) > MAX_QUERY_LENGTH:
            raise ValueError(
                f"Research query is too long. "
                f"Maximum allowed length is "
                f"{MAX_QUERY_LENGTH} characters."
            )

        # ==========================================
        # PIPELINE START
        # ==========================================

        print("\n===== STARTING RESEARCH PIPELINE =====\n")

        # ==========================================
        # STEP 1 — PLANNER
        # ==========================================

        print("[PLANNER] Creating research plan...")

        tasks = self.planner.plan(query)

        tasks = tasks[:MAX_RESEARCH_TASKS]

        print(
            f"[PLANNER] ✓ Generated "
            f"{len(tasks)} research tasks\n"
        )

        if not tasks:
            raise ValueError(
                "Planner did not generate any research tasks."
            )

        # ==========================================
        # STEP 2 — PARALLEL RESEARCH + CRITIC
        # ==========================================

        print(
            "[ORCHESTRATOR] Running research branches "
            "in parallel...\n"
        )

        results_by_index = {}

        with ThreadPoolExecutor(
            max_workers=len(tasks)
        ) as executor:

            futures = {
                executor.submit(
                    self._research_and_critic,
                    task,
                    index,
                ): index
                for index, task in enumerate(tasks, start=1)
            }

            for future in as_completed(futures):

                index = futures[future]

                try:
                    results_by_index[index] = future.result()

                except Exception as exc:

                    print(
                        f"[BRANCH {index}] "
                        f"✗ Failed: {exc}"
                    )

                    raise

        # Restore planner order before synthesis
        results = [
            results_by_index[index]
            for index in sorted(results_by_index)
        ]

        print(
            "\n[ORCHESTRATOR] "
            "✓ All research branches completed\n"
        )

        # ==========================================
        # STEP 3 — SYNTHESIZER
        # ==========================================

        print(
            "[SYNTHESIZER] "
            "Combining validated findings..."
        )

        final_answer = self.synthesizer.synthesize(
            query=query,
            research_results=results,
        )

        print(
            "[SYNTHESIZER] "
            "✓ Final report generated\n"
        )

        # ==========================================
        # PIPELINE COMPLETE
        # ==========================================

        print(
            "===== RESEARCH PIPELINE COMPLETE =====\n"
        )

        return {
            "query": query,
            "tasks": tasks,
            "results": results,
            "final_answer": final_answer,
        }
