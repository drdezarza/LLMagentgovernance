PY ?= python3
STAGES := $(shell $(PY) -c "import sys;sys.path.insert(0,'.');from agentgov import config as C;print(' '.join(e['id'] for e in C.plan()['experiments'] if e.get('enabled')))")

.PHONY: help install test verify analyze mock plan

help:
	@echo "make install   install Python dependencies"
	@echo "make test      simulator equivalence tests"
	@echo "make verify    check every number quoted in the paper against data/"
	@echo "make analyze   recompute every stage's analysis from the saved unit records"
	@echo "make mock      offline end-to-end run of two stages with the mock model"
	@echo "make plan      stage status and live cost estimates"

install:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) tests/test_equivalence.py

verify:
	$(PY) paper/check_numbers.py

analyze:
	@for s in $(STAGES); do echo "== $$s"; $(PY) -m agentgov analyze $$s > /dev/null || exit 1; done
	@echo "done; inspect changes with: git status --short data/runs"

mock:
	$(PY) -m agentgov run --mock --hours 0.3 --only S7b_C S5h_live_quarantine

plan:
	$(PY) -m agentgov plan
