import sys
from pathlib import Path

from pydantic import BaseModel

# root path for helper import
root_path = str(Path(__file__).parent.parent.parent)

if root_path not in sys.path:
    sys.path.append(root_path)

from utils.llm_config import get_llm_client

# LLM Selection
PROVIDER = "lmstudio"

# Initialize
client, model = get_llm_client(PROVIDER)


# --------------------------------------------------------------
# Step 1: Define the response format in a Pydantic model
# --------------------------------------------------------------


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


# --------------------------------------------------------------
# Step 2: Call the model
# --------------------------------------------------------------

if PROVIDER == "openai":
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday.",
            },
        ],
        response_format=CalendarEvent,
    )

    event = completion.choices[0].message.parsed
else:
    calendar_schema = CalendarEvent.model_json_schema()

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday.",
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "calendar_event_schema",
                "schema": calendar_schema,
                "strict": True,
            },
        },
    )

    message = completion.choices[0].message
    # Check if reasoning_content exists in the raw response
    raw_resp = completion.model_dump()
    reasoning = raw_resp["choices"][0]["message"].get("reasoning_content", "")
    content = message.content or ""

    # Use reasoning if content is empty (common in Qwen 3.5 bug)
    final_json = content if content.strip() else reasoning

    if not final_json:
        raise ValueError("Both content and reasoning_content are empty.")

    event = CalendarEvent.model_validate_json(final_json)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------


event.name
event.date
event.participants
