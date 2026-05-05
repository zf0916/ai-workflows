# AI Worfklow with Local LLMs

This project explores the implementation of effective LLM workflows (as defined by Anthropic) using **local LLMs** instead of proprietary APIs. It is a modified fork of Dave Ebbelaar's tutorial on "Building Effective Agents."

### **Reference Material**
*   **Anthropic Blog:** [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
*   **Dave Ebbelaar's Repo:** [AI Cookbook - Workflows](https://github.com/daveebbelaar/ai-cookbook/tree/main/patterns/workflows)
*   **Dave Ebbelaar's YT Tutorial:** [Watch here](https://www.youtube.com/watch?v=bZzyPscbtI8&t=2s)

---

## **Key Changes & Features**
*   **Multi-Provider Support:** Added support for local inference engines via `ollama` and `lmstudio` in addition to `openai`.
*   **Centralized Config:** LLM logic is moved to `utils/llm_config.py` for easier management.
*   **Flexible Switching:** Easily toggle between providers in the main script:
    ```python
    PROVIDER = "lmstudio" # Options: "openai", "ollama", "lmstudio"
    ```
*   **Environment Driven:** Specific local model names are managed via `.env`.

---

## **Local Environment**
*   **GPU:** NVIDIA RTX 5060Ti (16GB VRAM)
*   **Primary Model:** `qwen3-coder-30b-a3b` (Recommended for structured output tasks)

---

## **Exploration & Local Model Findings**

During development, several local models were tested for **Tool Calling** and **Structured Output (Pydantic parsing)**. Below is a summary of the common issues encountered:

### **Common Failure Categories**
1.  **Protocol Mismatch (The "Reasoning Hijack"):** Many reasoning models (e.g., Qwen 3.5/3.6 9B-35B) correctly generate the required JSON but place it in the `reasoning_content` field instead of `content`. This causes the standard OpenAI SDK `.parse()` method to return `None`.
2.  **Sequence Violations (The "Chatty Assistant"):** Models like `Mistral 3-14B Reasoning` often include conversational preambles (e.g., "Sure, let me check that for you...") alongside a tool call. This violates the strict protocol that requires the assistant's content to be empty when a tool is called.
3.  **Context Collapse:** Smaller models (like `Gemma 4B`) may struggle with parameter extraction (knowing coordinates for a city) or fail to generate a final response once the tool data is returned.

### **The "Golden" Local Model**
The **`qwen3-coder-30b-a3b`** model was the most consistent, successfully adhering to both the JSON schema and the API turn-taking protocol without extra conversational filler.

---

### **Setup & Installation**

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable dependency management. 

#### **Quick Start**
If you have `uv` installed, run the following commands to set up your environment:

```bash
# Initialize the project (if starting fresh)
uv init

# Install dependencies from pyproject.toml
uv sync

# Run the weather script
uv run python patterns/workflows/01_standard_done.py
```

#### **Why uv?**
Using `uv` ensures that the `.venv` is created automatically and that all dependencies are locked to the exact versions specified in `uv.lock`. For a detailed guide on using `uv` with this project, check out [Dave Ebbelaar's Guide](https://python.datalumina.com/tools/dependencies/virtual-env).

---

## Project Structure

```text
├── utils
│   └── llm_config.py             # Centralized local/cloud LLM configuration
├── workflows
│   ├── 1-introduction            # Basic building blocks (Dave Ebbelaar's Tutorial)
│   │   ├── 1-basic.py
│   │   ├── 2-structured.py
│   │   ├── 3-tools.py
│   │   ├── 4-retrieval.py
│   │   └── kb.json
│   ├── 2-workflow-patterns       # Advanced orchestration patterns
│   │   ├── 1-prompt-chaining.py
│   │   ├── 3-parallelization.py  # (Renamed for clarity)
│   │   └── 4-orchestrator.py
│   └── README.md                 # Original workflow documentation
├── .env.example                  # Template for local model names/URLs
├── pyproject.toml                # Project dependencies (uv)
├── uv.lock                       # Dependency lockfile
└── main.py                       # Entry point
```