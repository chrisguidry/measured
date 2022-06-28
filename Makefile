.PHONY: all
all: install src/measured/_parser.py

.bookkeeping/development.in: setup.cfg pyproject.toml
	mkdir -p .bookkeeping
	echo "-e .[dev]" > .bookkeeping/development.in

.bookkeeping/installed: .bookkeeping/pip-tools .bookkeeping/development.txt
	pip-sync .bookkeeping/development.txt
	tox -p --recreate --notest
	touch .bookkeeping/installed

.bookkeeping/pip-tools:
	mkdir -p .bookkeeping
	touch .bookkeeping/pip-tools.next

	pip install -U pip pip-tools

	mv .bookkeeping/pip-tools.next .bookkeeping/pip-tools

%.txt: %.in .bookkeeping/pip-tools
	touch $@.next
	pip-compile --upgrade --output-file $@.next $<
	mv $@.next $@

src/measured/_parser.py: src/measured/measured.lark
	python -m lark.tools.standalone --start unit --start quantity $< | \
		sed s/Lark_StandAlone/Parser/g > $@
	black $@
	isort $@

.PHONY: install
install: .bookkeeping/installed

.PHONY: clean
clean:
	rm -Rf .bookkeeping/
	rm -Rf dist/*
