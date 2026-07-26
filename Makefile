.PHONY: all
all: src/measured/_parser.py

src/measured/_parser.py: src/measured/measured.lark
	python -m lark.tools.standalone --start unit --start quantity $< | \
		sed s/Lark_StandAlone/Parser/g > $@
	black $@
	isort $@
