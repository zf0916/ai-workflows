"""
Recovery: Manages failures and exceptions gracefully in agent workflows.
This component implements retry logic, fallback processes, and error handling to ensure system resilience.
"""

from utils.llm_config import get_llm_client
from utils.llm_parse import response_parse

from typing import Optional
from pydantic import BaseModel


PROVIDER = "lmstudio"
client, model = get_llm_client(PROVIDER)


class UserInfo(BaseModel):
    name: str
    email: str
    age: Optional[int] = None  # Optional field


def resilient_intelligence(prompt: str) -> str:

    # Get structured output
    input = [
        {"role": "system", "content": "Extract user information from the text."},
        {"role": "user", "content": prompt},
    ]

    response = response_parse(
        PROVIDER, client, model, input, text_format=UserInfo, temperature=0.0
    )

    user_data = response.model_dump()

    try:
        # Try to access age field and check if it's valid
        age = user_data["age"]
        if age is None:
            raise ValueError("Age is None")
        age_info = f"User is {age} years old"
        return age_info

    except (KeyError, TypeError, ValueError):
        print("❌ Age not available, using fallback info...")

        # Fallback to available information
        return f"User {user_data['name']} has email {user_data['email']}"


if __name__ == "__main__":
    result = resilient_intelligence(
        "My name is John Smith and my email is john@example.com"
    )
    print("Recovery Output:")
    print(result)
