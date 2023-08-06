import re

from bulot.aliases import Aliases, ALIASES


# To provide correct tests we must be sure that ALIASES still caontains enough entries
assert len(ALIASES) > 1


class TestAliases:
    aliases = Aliases(ALIASES)

    def test_regex(self):
        for alias, (regex, replacement) in self.aliases.regexes.items():
            assert isinstance(alias, str)
            assert isinstance(regex, re.Pattern)
            assert isinstance(replacement, str)

    def test_process(self):
        cmd = " ".join(ALIASES.keys())
        cmd = self.aliases.process_aliases(cmd)
        assert cmd == " ".join(ALIASES.values())
