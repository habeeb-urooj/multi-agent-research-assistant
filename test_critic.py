from app.agents.critic import CriticAgent


critic = CriticAgent()

task = """
Identify how multi-agent AI systems are being used to automate
software development.
"""

research_result = """
Multi-agent AI systems are increasingly being used for software
development tasks such as code generation, debugging, testing,
documentation, and software planning.

Some systems use specialized agents where one agent plans the task,
another writes code, another tests it, and another reviews the result.

Source:
https://example.com/research
"""

print("\n===== CRITIC TEST =====\n")

result = critic.critique(
    task=task,
    research_result=research_result
)

print(result)

print("\n===== CRITIC TEST COMPLETE =====\n")
