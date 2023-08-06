# Bulot
Helper to run Bash commands with python

[![PyPI - Version](https://img.shields.io/pypi/v/bulot.svg)](https://pypi.org/project/bulot)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bulot.svg)](https://pypi.org/project/bulot)

-----

**Table of Contents**

- [Installation](#installation)
- [Examples](#examples)
    - [Concept](#concept)
    - [Print](#print)
    - [Classes](#classes)
    - [Git](#git)
- [License](#license)

## Installation

```console
pip install bulot
```

## Examples

### Concept
```python
from bulot import Shell

# Create a shell
sh = Shell()
sh | "ls" | print

# Create another shell independant from the first one
sh2 = Shell()
sh2.cd("..")
print(sh2.cwd())
# remove alias for ls
del sh2.aliases["ls"]
files = sh2 | "ls"
# without the alias, will print ls without color
print(files)
```

### Print
```python
import json
from pprint import pprint
from bulot import Pipe


def jprint(data):
    print(json.dumps(data, indent=4, default=repr))


data = sh << list(__builtins__.keys())[:10]
assert len(data.stdout) == 10
assert isinstance(data, Pipe)
data | print
data | pprint
data | jprint
```

### Classes
```python
import re
from bulot import xargs
from bulot.utils import stdout
from glob import glob


def extract_classes(stdin: str) -> list:
    """Returns classes' name"""
    def extract_name(class_line):
        return re.sub(r"class (\w+).*:", r"\1", class_line)

    return [extract_name(line) for line in stdin.splitlines() if line.startswith("class")]


classes = sh << glob("bulot/*.py") | xargs - "cat {}" | "\n".join | extract_classes
assert "Shell" in classes.stdout
```
`sh | "ls *.py"` can't expand * because subprocess.run has shell=False then we must use glob
see https://docs.python.org/3/library/subprocess.html#security-considerations

### Git
```python
from bulot import Pipe, shell
from bulot.utils import stdout

class Git(Shell):
    def __or__(self, cmd: RunPipeCmd) -> "Pipe":
        if isinstance(cmd, str):
            cmd = f"git {cmd}"
        return super().__or__(cmd)


git = Git()

CREATE_BRANCH = False
BRANCH_NAME = "plop"

branch_init = git | "branch --show-current" | stdout

# Save current changes
nb_stash_before = git | "stash list" | str.splitlines | len | stdout
git | "stash"
nb_stash_after = git | "stash list" | str.splitlines | len | stdout
is_stashed = nb_stash_before != nb_stash_after

# Update main branch
if branch_init != "main":
    git | "chechout main"
git | "pull"

# Create new branch
checkout = git | f"checkout -b {BRANCH_NAME}"
if checkout.return_code == 128:
    git | f"checkout {BRANCH_NAME}"

# Modify
sh.fake = True
FILE = "bulot/__init__.py"
sh << "\nraise RuntimeError('Oups')" >> FILE
sh.fake = False
git.fake = True
git | f"add {FILE}"
git | "commit -m 'Add error'"
git.fake = False

# push changes
branch_exist_on_remote = git | f"ls-remote --exit-code --heads origin {BRANCH_NAME}"
git.fake = True
if branch_exist_on_remote.return_code == 2:
    git | "push --set-upstream origin {BRANCH_NAME}"
else:
    git | "push"
git.fake = False

# restore previous state
git | f"checkout {branch_init}"
if is_stashed:
    git | "stash pop"

# Historic
git_commands = [command.value for command in git.historic]
assert "git branch --show-current" in git_commands
print(git_commands)
# to print all stdout
# print([command.stdout for command in git.historic])
assert git.historic[0].stdout == branch_init
assert any(command.fake for command in git.historic)
```

## License

`Bulot` is distributed under the terms of the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) license.

