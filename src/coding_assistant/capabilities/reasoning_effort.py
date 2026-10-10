from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic_ai import RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.settings import ModelSettings


# 1. Implement the ReasoningEffort capability.
#    Override the get_model_settings() method.
class ReasoningEffort(AbstractCapability[Any]):
    def get_model_settings(self) -> Callable[[RunContext[Any]], ModelSettings]:
        def _set_reasoning_effort(
            ctx: RunContext[Any]
        ) -> ModelSettings:
            if ctx.prompt.find("@low") != -1:
                thinking_set = "low"
            elif ctx.prompt.find("@high") != -1:
                thinking_set = "high"
            else: 
                thinking_set = "medium"    

            return ModelSettings(
                thinking=thinking_set
            )

        return _set_reasoning_effort

