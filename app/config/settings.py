import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

PLANNER_MODEL = os.getenv(
    "PLANNER_MODEL",
    "google/gemma-4-26b-a4b-it"
)

RESEARCHER_MODEL = os.getenv(
    "RESEARCHER_MODEL",
    "google/gemma-4-26b-a4b-it"
)

CRITIC_MODEL = os.getenv(
    "CRITIC_MODEL",
    "google/gemma-4-26b-a4b-it"
)

SYNTHESIZER_MODEL = os.getenv(
    "SYNTHESIZER_MODEL",
    "google/gemma-4-26b-a4b-it"
)

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set.")
