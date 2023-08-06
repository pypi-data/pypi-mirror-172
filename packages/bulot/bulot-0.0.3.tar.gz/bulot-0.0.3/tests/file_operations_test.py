from io import StringIO, BytesIO
from pathlib import Path
from unittest.mock import Mock

import pytest

from bulot.file_operations import write_file
from .constants import ECHO_STDOUT, FILE_NAME, PATH_TESTS


class TestFileOperations:
    def test_wrong_directory(self, file_mocker: Mock):
        with pytest.raises(ValueError):
            write_file(ECHO_STDOUT, PATH_TESTS / "plop" / FILE_NAME, "w")

    @pytest.mark.usefixtures("file_mocker")
    def test_write(self, file_mocker: Mock):
        write_file(ECHO_STDOUT, Path(FILE_NAME), "w")
        file_mocker.assert_called_once_with(Path(FILE_NAME), "w")
        file_mocker().write.assert_called_once_with(ECHO_STDOUT)

    @pytest.mark.usefixtures("file_mocker")
    def test_append(self, file_mocker: Mock):
        write_file(ECHO_STDOUT, FILE_NAME, "a+")
        file_mocker.assert_called_once_with(Path(FILE_NAME), "a+")
        file_mocker().write.assert_called_once_with(ECHO_STDOUT)

    @pytest.mark.usefixtures("file_mocker")
    def test_write_stringio(self, file_mocker: Mock):
        file = StringIO()
        write_file(ECHO_STDOUT, file, "w")
        assert file.getvalue() == ECHO_STDOUT

    @pytest.mark.usefixtures("file_mocker")
    def test_write_stringio_str(self, file_mocker: Mock):
        file = StringIO()
        data = ECHO_STDOUT.encode("utf-8")
        write_file(data, file, "w")
        assert file.getvalue() == ECHO_STDOUT

    @pytest.mark.usefixtures("file_mocker")
    def test_write_bytesio(self, file_mocker: Mock):
        file = BytesIO()
        data = ECHO_STDOUT.encode("utf-8")
        write_file(data, file, "w")
        assert file.getvalue() == data

    @pytest.mark.usefixtures("file_mocker")
    def test_write_bytesio_str(self, file_mocker: Mock):
        file = BytesIO()
        data = ECHO_STDOUT.encode("utf-8")
        write_file(ECHO_STDOUT, file, "w")
        assert file.getvalue() == data
