.PHONY: run test

run:
	# python3 main.py
	python3 nth-triangle-number.py

test:
	make test-fast
	@echo
	@echo Warning: Slow tests skipped. Run \"make test-all\" to run all, or \"make test-slow\" to run just slow tests.

test-fast:
	./run-fast-tests.sh

test-slow:
	./run-slow-tests.sh

test-all:
	make test-fast
	make test-slow
