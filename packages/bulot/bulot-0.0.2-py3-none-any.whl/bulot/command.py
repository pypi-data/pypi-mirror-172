from __future__ import annotations

import subprocess as sp
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .file_operations import write_file
from ._types import FileType


@dataclass
class Command:
    value: str
    cwd: Path
    start: float
    end: float
    return_code: int
    result: None | sp.CalledProcessError | sp.CompletedProcess
    fake: bool = False

    @property
    def stdout(self) -> str:
        if self.result is None:
            return ""
        else:
            stdout = self.result.stdout.decode("utf-8")
            return Command._remove_trailling_new_line(stdout)

    @property
    def stderr(self) -> str:
        if self.result is None:
            return ""
        else:
            stderr = self.result.stderr.decode("utf-8")
            return Command._remove_trailling_new_line(stderr)

    @staticmethod
    def _remove_trailling_new_line(value: str) -> str:
        if value.endswith("\n"):
            return value[:-1]
        else:
            return value

    def __gt__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "w", self.fake)
        return self.stdout

    def __rshift__(self, file: FileType) -> Any:
        write_file(self.stdout, file, "a+", self.fake)
        return self.stdout
