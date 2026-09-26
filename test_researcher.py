from app.agents.researcher import ResearchAgent


agent = ResearchAgent()

result = agent.research(
    "Explain how large language models are used in AI research assistants."
)

print("\n===== RESEARCH RESULT =====\n")
print(result)
