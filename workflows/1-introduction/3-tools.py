import json
import sys
from pathlib import Path

import requests
from pydantic import BaseModel, Field

# root path for helper import
root_path = str(Path(__file__).parent.parent.parent)

if root_path not in sys.path:
    sys.path.append(root_path)

from utils.llm_config import get_llm_client

# LLM Selection
PROVIDER = "lmstudio"

# Initialize
client, model = get_llm_client(PROVIDER)

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

# --------------------------------------------------------------
# Define the tool (function) that we want to call
# --------------------------------------------------------------


def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]


# --------------------------------------------------------------
# Step 1: Call model with get_weather tool defined
# --------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": "What's the weather like in Paris today?",
        # "content": "What's the weather like in Paris today? (Note: Paris is at lat 48.85, long 2.35)",
    },
]

completion = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
)

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

completion.model_dump()

# --------------------------------------------------------------
# Step 3: Execute get_weather function
# --------------------------------------------------------------


def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)


# # Check if the model actually wants to call a tool (for local models)
# tool_calls = completion.choices[0].message.tool_calls

# if tool_calls:
#     for tool_call in tool_calls:
#         name = tool_call.function.name
#         args = json.loads(tool_call.function.arguments)

#         # Append the assistant's call to the conversation
#         messages.append(completion.choices[0].message)

#         result = call_function(name, args)

#         # Append the tool result
#         messages.append(
#             {
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": json.dumps(result),
#             }
#         )
# else:
#     # Handle the case where the model just replied with text
#     print("The model did not call a tool. Response:")
#     print(completion.choices[0].message.content)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------


class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


completion_2 = client.beta.chat.completions.parse(
    model=model,
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)

# --------------------------------------------------------------
# Step 5: Check model response
# --------------------------------------------------------------

final_response = completion_2.choices[0].message.parsed
final_response.temperature
final_response.response
