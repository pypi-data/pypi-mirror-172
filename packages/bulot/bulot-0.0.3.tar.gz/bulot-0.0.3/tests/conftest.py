import pytest
from unittest import mock


@pytest.fixture(scope="function")
def file_mocker():
    # Read a mocked /etc/release file
    mocked_file = mock.mock_open()
    # with mock.patch("__main__.open", mocked_file), mock.patch(
    #     "pathlib.Path.exists", lambda: True
    # ):
    with mock.patch("builtins.open", mocked_file):
        yield mocked_file
