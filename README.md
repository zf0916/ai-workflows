# AI-Workflows (Local LLM)
- Scripts fork from https://github.com/daveebbelaar/ai-cookbook/tree/main/patterns/workflows
- Learn AI workflows described in https://www.anthropic.com/engineering/building-effective-agents
- Add support for local LLM

## Local LLM feature
- Created utils\llm_config.py to consolidate LLM API call, local model name to specified in .env
- Added local llm support for tool call and validation

## Model tried
- gemma4:e4b - hallucinated on details, sometimes cant extract required info
- qwen3.5-9b - non-thinking (toggle in LM Studio) oerform better than thinking mode
- qwen3-coder-30b-a3b - best performance for 16GB VRAM

# Setup
- Guide on uv: https://python.datalumina.com/tools/dependencies/virtual-env
```
pip install uv

uv init

uv sync
```