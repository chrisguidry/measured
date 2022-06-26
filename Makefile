.PHONY: all
all: install src/measured/_measured_parser.py

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

_%_parser.py: %.lark
	python -m lark.tools.standalone $< | sed s/Lark_StandAlone/Parser/g > $@
	black $@
	isort $@

.PHONY: install
install: .bookkeeping/installed src/measured/_measured_parser.py

.PHONY: clean
clean:
	rm -Rf .bookkeeping/
	rm -Rf dist/*
