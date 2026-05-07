from pydantic import BaseModel
from utils.llm_config import get_llm_client
from utils.llm_completion import get_completion

# LLM Selection
PROVIDER = "lmstudio"
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

messages = [
    {"role": "system", "content": "Extract the event information."},
    {
        "role": "user",
        "content": "Alice and Bob are going to a science fair on Friday.",
    },
]


event = get_completion(PROVIDER, client, model, messages, response_format=CalendarEvent)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------

event.name
event.date
event.participants
