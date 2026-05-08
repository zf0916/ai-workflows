"""
Validation: Ensures LLM outputs match predefined data schemas.
This component provides schema validation and structured data parsing to guarantee consistent data formats for downstream code.

More info: https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses
"""

from utils.llm_config import get_llm_client
from utils.llm_parse import response_parse

from pydantic import BaseModel

PROVIDER = "lmstudio"
client, model = get_llm_client(PROVIDER)


class TaskResult(BaseModel):
    """
    More info: https://docs.pydantic.dev
    """

    task: str
    completed: bool
    priority: int


def structured_intelligence(prompt: str) -> TaskResult:
    # client = OpenAI()

    input = [
        {
            "role": "system",
            "content": "Extract task information from the user input.",
        },
        {"role": "user", "content": prompt},
    ]

    response = response_parse(PROVIDER, client, model, input, text_format=TaskResult)

    return response


if __name__ == "__main__":
    result = structured_intelligence(
        "I need to complete the project presentation by Friday, it's high priority"
    )
    print("Structured Output:")
    print(result.model_dump_json(indent=2))
    print(f"Extracted task: {result.task}")
