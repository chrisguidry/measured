.DEFAULT_GOAL := install

.bookkeeping/development.in: setup.cfg
	mkdir -p .bookkeeping
	echo "-e .[dev]" > .bookkeeping/development.in

.bookkeeping/installed: .bookkeeping/pip-tools .bookkeeping/development.txt
	pip-sync .bookkeeping/development.txt
	tox --recreate --notest
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

.PHONY: install
install: .bookkeeping/installed

.PHONY: clean
clean:
	rm -Rf .bookkeeping/
	rm -Rf dist/*
