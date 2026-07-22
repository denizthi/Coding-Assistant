from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic_ai import RunContext
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.messages import ToolCallPart
from pydantic_ai.tools import ToolDefinition
from pydantic_ai.toolsets import FunctionToolset

#from coding_assistant.deps import AgentDeps


def _path_sandbox(path: str) -> Path:
    return Path("sandbox") / Path(path)


# 1. Implement the read_file tool
def read_file(path: str) -> str:
    """
    Read a UTF-8 text file from disk and return its contents.

    Args:
        path: Relative or absolute path to the file.

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the path points to a directory.
        UnicodeDecodeError: If the file is not valid UTF-8 text.
    """
    file_path = _path_sandbox(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    return file_path.read_text(encoding="utf-8")

# 2. Implement the write_file tool
def write_file(path: str, content: str):
    """
    Writes a UTF-8 text file from disk and return its contents.

    Args:
        path: Relative or absolute path to the file.
        content: Content to be written.

    Returns:
        Writes the contents to the file
    """  
    file_path = _path_sandbox(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path.write_text(content, encoding="utf-8")
    


def search_files(pattern: str) -> list[str]:
    """Search for files matching a glob pattern.

    Parameters
    ----------
    patters : str
        The glob patterns to match files (e.g., "**/*.py", "test_*.py)

    Returns
    -------
    list[str]
        A list of relative file paths matching the pattern.

    """
    sandbox_root = _path_sandbox("")
    matches = sandbox_root.glob(pattern)

    return [str(p.relative_to(sandbox_root)) for p in matches]

def delete_file(path: str) -> None:
    """Deletes the file from disk
    
    Parameters
    ----------
    path: Relative or absolute path to the file.
    
    """
    _path_sandbox(path).unlink()
    
# 3. Implement the FileOperations capability. Override the get_toolset() method.
class FileOperations(AbstractCapability[Any]):
    def get_toolset(self) -> FunctionToolset:
        toolset = FunctionToolset()
        toolset.add_function(read_file)
        toolset.add_function(write_file)
        toolset.add_function(search_files)
        toolset.add_function(delete_file)
        return toolset

    async def before_tool_execute(
        self,
        ctx: RunContext[Any],
        *,
        call: ToolCallPart,
        tool_def: ToolDefinition,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        if call.tool_name == "search_files":
            ctx.deps.console.log(f"Searching: {args.get('pattern')}")
        elif call.toolname == "read_file":
            ctx.deps.console.log(f"Reading: {args.get('path')}")
        elif call.toolname == "write_file":
            ctx.deps.console.log(f"Editing: {args.get('path')}")

        return args
    
