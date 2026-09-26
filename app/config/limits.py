# Application safety limits

# Maximum characters allowed in a research query
MAX_QUERY_LENGTH = 1000

# Maximum number of research tasks generated
MAX_RESEARCH_TASKS = 3

# LLM output token limits
PLANNER_MAX_TOKENS = 500
RESEARCHER_MAX_TOKENS = 1200
CRITIC_MAX_TOKENS = 1000
SYNTHESIZER_MAX_TOKENS = 1500

# API protection
RATE_LIMIT_PER_MINUTE = 10
DAILY_REQUEST_LIMIT = 100

# Maximum simultaneous research pipelines
MAX_CONCURRENT_REQUESTS = 2

# Emergency kill switch
PIPELINE_ENABLED = True
