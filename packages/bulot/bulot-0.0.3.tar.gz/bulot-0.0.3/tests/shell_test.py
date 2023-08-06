import subprocess as sp

import pytest

from bulot import Shell, Command, Pipe
from .constants import (
    ECHO_CMD,
    ECHO_STDOUT,
    ECHO_STR,
    WRONG_CMD,
    WRONG_FILE,
    PATH_TESTS,
    PATH_DOES_NOT_EXIST,
)


class TestShell:
    sh = Shell()

    def test_run(self):
        command = self.sh.run(ECHO_CMD)
        assert isinstance(command, Command)
        assert command.stdout == ECHO_STDOUT

    def test_ls_absolute(self):
        self.sh.cd(PATH_TESTS.parent)
        assert self.sh.cwd() == PATH_TESTS.parent
        self.sh.cd(PATH_TESTS)
        assert self.sh.cwd() == PATH_TESTS

    def test_ls_relative(self):
        directory_name = PATH_TESTS.parts[-1]
        self.sh.cd(PATH_TESTS.parent)
        assert self.sh.cwd() == PATH_TESTS.parent
        self.sh.cd(directory_name)
        assert self.sh.cwd() == PATH_TESTS

    def test_ls_wrong_path(self):
        self.sh.cd(PATH_TESTS.parent)
        assert self.sh.cwd() == PATH_TESTS.parent
        with pytest.raises(sp.CalledProcessError):
            self.sh.cd(PATH_DOES_NOT_EXIST)
        assert self.sh.cwd() == PATH_TESTS.parent

    def test_error(self):
        command = self.sh(WRONG_CMD)
        assert isinstance(command, Command)
        assert command.return_code == 2
        assert command.stdout == ""
        assert command.stderr.__contains__(WRONG_FILE)

    def test_error_check(self):
        with pytest.raises(sp.CalledProcessError):
            self.sh(WRONG_CMD, check=True)

        command = self.sh(WRONG_CMD)
        assert command.return_code != 0

        self.sh.config.check = True
        with pytest.raises(sp.CalledProcessError):
            self.sh(WRONG_CMD)
        with pytest.raises(sp.CalledProcessError):
            self.sh(WRONG_CMD)

        command = self.sh(WRONG_CMD, check=False)
        assert command.return_code != 0

    def test__call__(self):
        command = self.sh(ECHO_CMD)
        assert isinstance(command, Command)
        assert command.stdout == ECHO_STDOUT

    def test__or__(self):
        pipe = self.sh | ECHO_CMD
        assert isinstance(pipe, Pipe)
        assert pipe.stdout == ECHO_STDOUT
        assert pipe.sh is self.sh

    def test__lshift__(self):
        pipe = self.sh << ECHO_STR
        assert isinstance(pipe, Pipe)
        assert pipe.stdout == ECHO_STR
        assert pipe.sh is self.sh
