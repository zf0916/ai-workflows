from utils.llm_config import get_llm_client
from utils.llm_completion import get_completion

# LLM Selection
PROVIDER = "lmstudio"
client, model = get_llm_client(PROVIDER)

messages = [
    {"role": "system", "content": "Respond directly. No reasoning."},
    {"role": "user", "content": "Write a limerick about Python."},
]

# Execution
response = get_completion(PROVIDER, client, model, messages)

print(f"--- Response from {PROVIDER} ({model}) ---")
print(response)
