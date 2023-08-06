from __future__ import annotations

from pathlib import Path

from bulot import Shell


README = Path(__file__).parent.parent / "README.md"


def extract_codes(language: str = "python") -> list[str]:
    blocks = []
    with open(README) as f:
        block: list[str] = []
        is_inside_block = False

        for line in f.read().split("\n"):
            if line == f"```{language}":
                is_inside_block = True
            elif is_inside_block and line == "```":
                blocks.append("\n".join(block))
                block.clear()
                is_inside_block = False
            elif is_inside_block:
                block.append(line)

    return blocks


class TestReadmeCodeBlocks:
    blocks_python = extract_codes()

    def test_python(self):
        assert len(self.blocks_python) == 4
        for block in self.blocks_python:
            sh = Shell()
            sh.cd(Path(__file__).parent.parent)
            exec(block, globals())
