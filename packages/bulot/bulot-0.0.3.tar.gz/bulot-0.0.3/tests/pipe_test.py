from pathlib import Path
from unittest.mock import Mock

import pytest

from bulot import Pipe, Shell, xargs, XArgs
from .constants import FILE_NAME, ECHO_CMD, ECHO_STDOUT, PIPE_STDOUT, REPLACE_STDOUT


class TestPipe:
    pipe = Pipe(Shell(), PIPE_STDOUT)

    def test__repr__(self):
        assert repr(self.pipe) == f"Pipe(stdout={repr(PIPE_STDOUT)})"

    def test__or__str(self):
        pipe = self.pipe | f"sed 's/{PIPE_STDOUT}/{REPLACE_STDOUT}/'"
        assert pipe.stdout == REPLACE_STDOUT

    def test__or__callable(self):
        def replace(old: str) -> str:
            return old.replace(PIPE_STDOUT, REPLACE_STDOUT)

        pipe = self.pipe | replace
        assert pipe.stdout == REPLACE_STDOUT

    def test__or__xargs(self):
        pipe = self.pipe | xargs
        x = pipe.stdout
        assert isinstance(x, XArgs)
        assert x.stdin == PIPE_STDOUT

    @pytest.mark.usefixtures("file_mocker")
    def test__gt__(self, file_mocker: Mock):
        self.pipe.sh | ECHO_CMD > FILE_NAME
        file_mocker.assert_called_once_with(Path(FILE_NAME), "w")
        file_mocker().write.assert_called_once_with(ECHO_STDOUT)

    @pytest.mark.usefixtures("file_mocker")
    def test__rshift__(self, file_mocker: Mock):
        (self.pipe.sh | ECHO_CMD) >> FILE_NAME
        file_mocker.assert_called_once_with(Path(FILE_NAME), "a+")
        file_mocker().write.assert_called_once_with(ECHO_STDOUT)
