from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .pipe import Pipe


class PipeExtractor:
    attr: str

    def __call__(self, pipe: "Pipe") -> Any:
        return getattr(pipe, self.attr)


class Stdout(PipeExtractor):
    attr = "stdout"


class Stderr(PipeExtractor):
    attr = "stderr"


class Stdin(PipeExtractor):
    attr = "stdin"


stdout = Stdout()
stderr = Stderr()
stdin = Stdin()
