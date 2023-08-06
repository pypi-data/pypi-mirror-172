import subprocess as sp
from pathlib import Path
from unittest.mock import Mock

import pytest

from bulot import Shell, Command
from .constants import ECHO_CMD, ECHO_STDOUT, FILE_NAME


class TestCommand:
    command = Shell()(ECHO_CMD)

    def test_command(self):
        command = self.command
        assert isinstance(command, Command)
        assert command.value == ECHO_CMD
        assert command.cwd == Path(__file__).parent.parent / "bulot"
        assert command.start < command.end
        assert command.return_code == 0

        result = command.result
        assert isinstance(result, sp.CompletedProcess)
        assert result.args == ["echo", "Plop"]
        assert result.returncode == 0
        assert result.stdout == f"{ECHO_STDOUT}\n".encode("utf-8")
        assert result.stderr == "".encode("utf-8")

    @pytest.mark.usefixtures("file_mocker")
    def test__gt__(self, file_mocker: Mock):
        self.command > FILE_NAME
        file_mocker.assert_called_once_with(Path(FILE_NAME), "w")
        file_mocker().write.assert_called_once_with(ECHO_STDOUT)

    @pytest.mark.usefixtures("file_mocker")
    def test__rshift__(self, file_mocker: Mock):
        self.command >> FILE_NAME
        file_mocker.assert_called_once_with(Path(FILE_NAME), "a+")
        file_mocker().write.assert_called_once_with(ECHO_STDOUT)
