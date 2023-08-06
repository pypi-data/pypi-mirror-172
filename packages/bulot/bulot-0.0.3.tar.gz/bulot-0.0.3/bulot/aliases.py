from __future__ import annotations

import re
from collections import UserDict


ALIASES = {
    "ls": "ls --color=always",
    "grep": "grep --color=always --exclude-dir={.bzr,CVS,.git,.hg,.svn,.idea,.tox}",
}


class Aliases(UserDict):
    @classmethod
    def default(cls):
        return cls(ALIASES)

    @staticmethod
    def compile(alias):
        return re.compile(r"\b" + alias + r"\b")

    def process_aliases(self, cmd: str):
        for (regex, replacement) in self.regexes.values():
            cmd = regex.sub(replacement, cmd)
        return cmd

    def __init__(self, *args, **kwargs):
        self.regexes = {}
        super().__init__(*args, **kwargs)

    def __setitem__(self, alias, replacement):
        self.data[alias] = replacement
        self.regexes[alias] = (Aliases.compile(alias), replacement)

    def __delitem__(self, alias):
        del self.data[alias]
        del self.regexes[alias]
