# AI-Workflows
- Scripts fork from https://github.com/daveebbelaar/ai-cookbook/tree/main/patterns/workflows
- Learn AI workflows described in https://www.anthropic.com/engineering/building-effective-agents


# AI Agents
- Added scripts for building blocks of agent, forked from https://github.com/daveebbelaar/ai-cookbook/tree/main/agents/building-blocks

## Local LLM support
- Created utils\llm_config.py to consolidate LLM API call, local model name to specified in .env
- Created utils\llm_parse.py to handle structured output for both openai and local models

## Model tried
- **Served with LM Studio**
- gemma4:e4b - hallucinated on details, sometimes cant extract required info
- qwen3.5-9b - non-thinking (toggle in LM Studio) perform better than thinking mode
- qwen3-coder-30b-a3b - best performance for 16GB VRAM

# Setup
- Guide on uv: https://python.datalumina.com/tools/dependencies/virtual-env
```
pip install uv

uv init

uv sync
```

## Findings
1. Local LLM supports text only ouput from most API call (no response_format)
2. Local LLM does not support structured output in these condition
    - cannot be parsed correctly with `chat.completion.parsed` or `response.parsed`
    - cannot be parsed correctly with both tools and response_format parameter existing in `chat.completion.create`
3. Workaround for local LLM structured output:
    - strictly use only `chat.completion.create`
    - manually pass the pydantic schema with custom list and `.model_json_schema()`
    - validate output against the pydantic schema using `.model_validate_json`