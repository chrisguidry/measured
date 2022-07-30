.PHONY: all
all: install src/measured/_parser.py

.bookkeeping/development.in: setup.cfg pyproject.toml
	mkdir -p .bookkeeping
	echo "-e .[dev]" > .bookkeeping/development.in

.bookkeeping/installed: .bookkeeping/pip-tools .bookkeeping/development.txt
	pip-sync .bookkeeping/development.txt

ifdef PYENV_VIRTUAL_ENV
	pyenv rehash
endif

	touch .bookkeeping/installed

.bookkeeping/pip-tools:
	mkdir -p .bookkeeping
	touch .bookkeeping/pip-tools.next

	pip install -U pip pip-tools

ifdef PYENV_VIRTUAL_ENV
	pyenv rehash
endif

	mv .bookkeeping/pip-tools.next .bookkeeping/pip-tools

%.txt: %.in .bookkeeping/pip-tools
	touch $@.next
	pip-compile --upgrade --output-file $@.next $<
	mv $@.next $@

.git/hooks/pre-commit: .bookkeeping/development.txt
	pre-commit install

src/measured/_parser.py: src/measured/measured.lark
	python -m lark.tools.standalone --start unit --start quantity $< | \
		sed s/Lark_StandAlone/Parser/g > $@
	black $@
	isort $@

.PHONY: install
install: .bookkeeping/installed .git/hooks/pre-commit

.PHONY: all-versions
all-versions:
	tox -p --recreate --notest

.PHONY: clean
clean:
	rm -Rf .bookkeeping/
	rm -Rf dist/*
