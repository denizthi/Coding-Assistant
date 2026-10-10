# Coding Assistant

A simple but functional coding assistant built with [Pydantic AI](https://github.com/pydantic/pydantic-ai).  
It runs in your terminal, accepts natural‑language Python questions, and can read/write files in a sandboxed
directory, adjust its reasoning effort, and load extensible “skills” from Markdown files.

## Features

- 💬 **Conversational coding helper** – multi‑turn chat with memory using Pydantic AI.
- 📂 **Sandboxed file tools** – read, write, search, and delete files under a local `sandbox/` directory.
- 🧠 **Reasoning control** – switch reasoning effort with inline tags: `@low`, `@high` (default is `medium`).
- 🧩 **Extensible skills** – load additional instructions from Markdown files in the `skills/` folder.

## Prerequisites

- Python (see `pyproject.toml` for the exact supported version)
- An [OpenRouter](https://openrouter.ai/) API key

Set your API key (and optionally a custom base URL) as environment variables:

```bash
export OPENROUTER_API_KEY="sk-..."
# optional:
# export OPENROUTER_API_BASE="https://openrouter.ai/api/v1"
```

## Installation

Clone the repository:

```bash
git clone https://github.com/denizthi/Coding-Assistant.git
cd Coding-Assistant
```

Install the project (pick one):

```bash
# Using uv (recommended if you have it installed)
uv sync

# Or using pip
pip install -e .
```

## Usage

Run the assistant from your shell:

```bash
coding-assistant
```

You’ll be prompted in the terminal, for example:

```text
I am a Python coding agent, how can I help you?
> Write a Python function that merges two sorted lists. @low
```

Type your questions and press Enter. To exit, type one of:

```text
quit
thanks
exit
no
```


### Skills

You can extend the assistant with Markdown‑based skills in the `skills/` folder.  
Each `.md` file can define metadata (name, description) and content the agent can load at runtime.

