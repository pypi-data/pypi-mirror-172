import sys


def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b)


class PythonVersion:
    version = sys.version_info[:3]

    def compare(self, expected_str: str) -> int:
        expected: list[int] = list(map(int, expected_str.split(".")))

        for exp, ver in zip(expected, self.version):
            comparaison = cmp(ver, exp)
            if comparaison != 0:
                return comparaison

        return 0

    def __eq__(self, expected: object) -> bool:
        if not isinstance(expected, str):
            raise NotImplementedError(f"Can't handle type '{type(expected)}' only str")
        return self.compare(expected) == 0

    def __lt__(self, expected: str) -> bool:
        return self.compare(expected) < 0

    def __le__(self, expected: str) -> bool:
        return self.compare(expected) <= 0

    def __gt__(self, expected: str) -> bool:
        return self.compare(expected) > 0

    def __ge__(self, expected: str) -> bool:
        return self.compare(expected) >= 0


PY = PythonVersion()
