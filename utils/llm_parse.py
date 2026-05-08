# Completion API
def completion_parse(
    provider,
    client,
    model,
    messages,
    tools=None,
    response_format=None,
    temperature=None,
):

    if provider == "openai":
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            tools=tools,
            response_format=response_format,
            temperature=temperature,
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
            temperature=temperature,
        )
        # Manually validate the string into a Pydantic object
        return response_format.model_validate_json(
            completion.choices[0].message.content
        )


# --- Asynchronous Version (For your parallel/agent scripts) ---
async def completion_parse_async(
    provider,
    client,
    model,
    messages,
    tools=None,
    response_format=None,
    temperature=None,
):

    if provider == "openai":
        completion = await client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            tools=tools,
            response_format=response_format,
            temperature=temperature,
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
            temperature=temperature,
        )
        return response_format.model_validate_json(
            completion.choices[0].message.content
        )


# Response API
def response_parse(
    provider,
    client,
    model,
    input,
    tools=None,
    text_format=None,
    instructions="",
    temperature=None,
):

    if provider == "openai":
        # Uses the high-level parse method
        response = client.responses.parse(
            model=model,
            instructions=instructions,
            input=input,
            tools=tools,
            text_format=text_format,
            temperature=temperature,
        )
        return response.output_parsed

    else:
        # Local model fallback to completions.create API
        completion = client.chat.completions.create(
            model=model,
            messages=input,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_output",
                    "schema": text_format.model_json_schema(),
                    "strict": True,
                },
            },
            temperature=temperature,
        )
        # Manually validate the string into a Pydantic object
        return text_format.model_validate_json(completion.choices[0].message.content)


# --- Asynchronous Version ---
async def response_parse_async(
    provider,
    client,
    model,
    input,
    tools=None,
    text_format=None,
    instructions="",
    temperature=None,
):

    if provider == "openai":
        response = await client.responses.parse(
            model=model,
            instructions=instructions,
            input=input,
            tools=tools,
            text_format=text_format,
            temperature=temperature,
        )
        return response.output_parsed
    else:
        completion = await client.chat.completions.create(
            model=model,
            messages=input,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_output",
                    "schema": text_format.model_json_schema(),
                    "strict": True,
                },
            },
            temperature=temperature,
        )
        # Manually validate the string into a Pydantic object
        return text_format.model_validate_json(completion.choices[0].message.content)
