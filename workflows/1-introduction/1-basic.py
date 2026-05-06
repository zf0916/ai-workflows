import sys
from pathlib import Path

# root path for helper import
root_path = str(Path(__file__).parent.parent.parent)

if root_path not in sys.path:
    sys.path.append(root_path)

from utils.llm_config import get_llm_client

# LLM Selection
PROVIDER = "lmstudio"

# Initialize
client, model = get_llm_client(PROVIDER)

# Execution

if PROVIDER == "openai":
    # openai model response
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Respond directly. No reasoning."},
            {"role": "user", "content": "Write a limerick about Python."},
        ],
    )
else:
    # local model response
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Respond directly. No reasoning."},
            {"role": "user", "content": "Write a limerick about Python."},
        ],
    )


print(f"--- Response from {PROVIDER} ({model}) ---")
print(completion.choices[0].message.content)
