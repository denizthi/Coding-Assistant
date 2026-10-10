import asyncio

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.models.openrouter import OpenRouterModel
from rich.console import Console
from rich.markdown import Markdown

import typer

from coding_assistant.capabilities.file_operations import FileOperations
from coding_assistant.capabilities.reasoning_effort import ReasoningEffort
from coding_assistant.capabilities.skills import Skills
from coding_assistant.deps import AgentDeps
from coding_assistant.utils import get_env


async def run_agent() -> None:
    console = Console()
    deps = AgentDeps(console=console)

    # 1. Configure the provider
    provider = OpenRouterProvider(
        api_key=get_env("OPENROUTER_API_KEY"),
        # base_url=get_env("OPENROUTER_API_BASE")
    )
    # 2. Configure the model
    model = OpenRouterModel(
        model_name="openai/gpt-5.1-codex-mini",
        provider=provider
    )

    # 3. Create the agent. Attach the model and instructions
    agent = Agent(
        model=model,
        instructions=(
            "You are a Python coding agent. "
            "Return clear, correct, and minimal Python code. "
            "Prefer the standard library. "
            "Explain only what is non-obvious, in a few sentences. "
            "If the task is ambiguous, ask one short clarifying question before coding."
            "Ask a follow-up question after answering"),
        capabilities=[FileOperations(), ReasoningEffort(), Skills()]
    )
    # 4. Prompt the user for input, run the agent, and print the output
    message_history = None
    while True:
        if message_history is None:
            question_1 = console.input(
                "I am a Python coding agent, how can I help you?")
        else:
            question_1 = console.input()
            if question_1 in ["quit", "thanks", "exit", "no"]:
                break
        result = await agent.run(question_1, message_history=message_history, deps=deps)
        console.print(Markdown(result.output))
        message_history = result.all_messages()
        #    Tip: use console.print(Markdown(result.output))


app = typer.Typer()


@app.command()
def main() -> None:
    try:
        asyncio.run(run_agent())
    except EOFError, KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app()
