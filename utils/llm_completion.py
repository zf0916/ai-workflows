def get_completion(provider, client, model, messages, tools=None, response_format=None):
    # --------------------------------------------------------------
    # 1. Logic for Standard Text (No Structure Required)
    # --------------------------------------------------------------
    if not response_format:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        return completion.choices[0].message.content

    # --------------------------------------------------------------
    # 2. Logic for Structured Output
    # --------------------------------------------------------------
    if provider == "openai":
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            tools=tools,
            response_format=response_format,
        )
        # Returns the actual Pydantic object
        return completion.choices[0].message.parsed

    else:
        # Local models: tools are usually omitted during the final structured turn
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_output",
                    "schema": response_format.model_json_schema(),
                    "strict": True,
                },
            },
        )
        # Manually validate the string into a Pydantic object
        return response_format.model_validate_json(
            completion.choices[0].message.content
        )


# --- Asynchronous Version (For your parallel/agent scripts) ---
async def get_completion_async(
    provider, client, model, messages, tools=None, response_format=None
):
    if not response_format:
        completion = await client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
        return completion.choices[0].message.content

    if provider == "openai":
        completion = await client.beta.chat.completions.parse(
            model=model, messages=messages, response_format=response_format
        )
        return completion.choices[0].message.parsed
    else:
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "out",
                    "schema": response_format.model_json_schema(),
                    "strict": True,
                },
            },
        )
        return response_format.model_validate_json(
            completion.choices[0].message.content
        )
