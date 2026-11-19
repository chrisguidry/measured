.PHONY: all
all: src/measured/_parser.py

src/measured/_parser.py: src/measured/measured.lark
	uv run python -m lark.tools.standalone --start unit --start quantity $< | \
		sed s/Lark_StandAlone/Parser/g > $@
	uv run ruff check --select I --fix $@
	uv run ruff format $@
