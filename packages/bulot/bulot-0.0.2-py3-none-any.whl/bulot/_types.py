from __future__ import annotations

from io import StringIO, BytesIO
from pathlib import Path
from typing import Callable, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from .xargs import XArgs, XArgsMeta


class NotSet:
    pass


RunPipeCmd = Union[str, Callable]
PipeCmd = Union[str, Callable, "XArgs", "XArgsMeta"]
not_set = NotSet()

# if PY >= "3.10":
#     FileData = str | bytes
#     FileType = str | Path | StringIO | BytesIO
FileData = Union[str, bytes]
FileType = Union[str, Path, StringIO, BytesIO]
