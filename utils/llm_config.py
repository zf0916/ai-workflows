import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI  # <--- Add AsyncOpenAI

# Load variables once when the module is imported
load_dotenv(override=True)


def get_llm_client(provider="openai", is_async=False):  # <--- Added is_async flag
    """
    Returns an OpenAI (or AsyncOpenAI) client and model name.
    """
    prefix = provider.upper()

    api_key = os.getenv(f"{prefix}_API_KEY")
    base_url = os.getenv(f"{prefix}_BASE_URL")
    model = os.getenv(f"{prefix}_MODEL")

    if not api_key:
        raise ValueError(f"API Key for {prefix} not found in environment variables.")

    # Logic to switch between Sync and Async
    if is_async:
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=api_key, base_url=base_url)

    return client, model
