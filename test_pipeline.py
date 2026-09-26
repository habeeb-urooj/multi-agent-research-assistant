from app.pipeline.research_pipeline import ResearchPipeline


query = "How are multi-agent AI systems being used to automate software development?"

pipeline = ResearchPipeline()

print("\n===== STARTING RESEARCH PIPELINE =====\n")

result = pipeline.run(query)

print("\n===== RESEARCH PLAN =====\n")

for i, task in enumerate(result["tasks"], start=1):
    print(f"{i}. {task}")

print("\n===== RESEARCH RESULTS =====\n")

for i, item in enumerate(result["results"], start=1):
    print(f"\n--- Research Result {i} ---")
    print(item["result"])

print("\n===== FINAL SYNTHESIZED ANSWER =====\n")

print(result["final_answer"])

print("\n===== PIPELINE COMPLETE =====\n")
