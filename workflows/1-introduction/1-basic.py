from utils.llm_config import get_llm_client

# LLM Selection
PROVIDER = "lmstudio"
client, model = get_llm_client(PROVIDER)

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "Write a limerick about the Python programming language.",
        },
    ],
)

response = completion.choices[0].message.content
print(response)
