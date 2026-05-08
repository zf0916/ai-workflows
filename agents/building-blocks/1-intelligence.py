"""
Intelligence: The "brain" that processes information and makes decisions using LLMs.
This component handles context understanding, instruction following, and response generation.

More info: https://platform.openai.com/docs/guides/text?api-mode=responses
"""

from utils.llm_config import get_llm_client

# LLM Selection
PROVIDER = "lmstudio"
client, model = get_llm_client(PROVIDER)


def basic_intelligence(prompt: str) -> str:
    # client
    response = client.responses.create(model=model, input=prompt)
    return response.output_text


if __name__ == "__main__":
    result = basic_intelligence(prompt="What is artificial intelligence?")
    print("Basic Intelligence Output:")
    print(result)
