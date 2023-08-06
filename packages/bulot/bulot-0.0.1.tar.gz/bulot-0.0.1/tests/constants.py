from pathlib import Path


ECHO_STR = "Plop"
ECHO_CMD = f"echo '{ECHO_STR}'"
ECHO_ARGS = ["echo", ECHO_STR]
ECHO_STDOUT = f"{ECHO_STR}"

WRONG_FILE = "a_file_that_does_not_exist"
WRONG_CMD = f"ls {WRONG_FILE}"

PIPE_STDOUT = "Plop"
REPLACE_STDOUT = "truc"

FILE_NAME = "Plop.plop"
PATH_TESTS = Path(__file__).parent
PATH_DOES_NOT_EXIST = PATH_TESTS / "Plop"
