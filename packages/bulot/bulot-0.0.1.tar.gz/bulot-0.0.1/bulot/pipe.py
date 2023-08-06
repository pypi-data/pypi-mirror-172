from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING


from .command import Command
from .file_operations import write_file
from .utils import PipeExtractor
from .xargs import XArgs, XArgsMeta
from ._types import PipeCmd, FileType

if TYPE_CHECKING:
    from .shell import Shell


@dataclass
class Pipe:
    sh: Shell
    stdout: Any
    stderr: Any | None = None
    return_code: int = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(stdout={repr(self.stdout)})"

    def __or__(self, cmd: PipeCmd | PipeExtractor) -> "Pipe" | Any:
        stdin = self.stdout
        stdout: Any

        if isinstance(cmd, PipeExtractor):
            return cmd(self)
        elif isinstance(cmd, XArgsMeta):
            stdout = cmd(stdin=stdin)
        elif isinstance(stdin, XArgs):
            stdout = stdin.run(cmd, shell=self.sh)
        elif isinstance(cmd, XArgs):
            cmd = cmd(stdin=stdin)
            stdout = cmd.run(stdin, shell=self.sh)
        else:
            result = self.sh.run_pipe(cmd, input=stdin)
            if isinstance(result, Command):
                return Pipe(
                    sh=self.sh,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    return_code=result.return_code,
                )
            else:
                stdout = result

        return Pipe(sh=self.sh, stdout=stdout)

    def __gt__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "w", fake=self.sh.fake)
        return self.stdout

    def __rshift__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "a+", fake=self.sh.fake)
        return self.stdout
