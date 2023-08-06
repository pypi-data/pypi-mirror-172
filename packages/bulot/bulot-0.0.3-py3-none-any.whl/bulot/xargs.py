from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Any, Iterable, TYPE_CHECKING


from ._types import not_set, NotSet, RunPipeCmd

if TYPE_CHECKING:
    from .shell import Shell


class XArgsMeta(type):
    def __sub__(self, cmd: RunPipeCmd) -> "XArgs":
        return self(execute=cmd)

    def __call__(self, *args, **kwargs) -> "XArgs":
        return super().__call__(*args, **kwargs)


@dataclass
class XArgs(metaclass=XArgsMeta):
    stdin: Any = not_set
    execute: RunPipeCmd | NotSet = not_set

    def __str__(self) -> str:
        return str(self.stdin)

    def __call__(self, stdin) -> XArgs:
        self.stdin = stdin
        return self

    def __sub__(self, cmd: RunPipeCmd) -> XArgs:
        ex = self.execute
        if ex is not_set:
            ex = cmd
        else:

            def chain(cmd, ex, *args, **kwargs) -> Any:
                return cmd(ex(*args, **kwargs))

            ex = partial(chain, cmd, ex)

        self.execute = ex
        return self

    def iter_stdin(self) -> Iterable:
        stdin = self.stdin
        if isinstance(stdin, str):
            return stdin.split()
        elif isinstance(stdin, list):
            return stdin
        else:
            raise NotImplementedError(f"XArgs is not implemented for {type(stdin)}")

    def run(self, cmd: RunPipeCmd, shell: Shell) -> list:
        it = self.iter_stdin()

        execute = self.execute
        if isinstance(execute, NotSet):
            stdout = [shell.run_pipe(cmd, input=stdin).stdout for stdin in it]
        else:
            if isinstance(execute, str):
                execute = execute.format
                stdout = [shell.run_pipe(execute(stdin)).stdout for stdin in it]
            else:
                stdout = [execute(stdin) for stdin in it]

        return stdout


xargs = XArgs
