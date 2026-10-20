# Lines of Action — build & run helpers
PYTHON  ?= python
CXX     ?= g++
CXXFLAGS ?= -O2 -std=c++17 -Wall
AI_BIN   = ai/loa_ai

.PHONY: all ai run test clean setup

all: ai

ai: $(AI_BIN)

$(AI_BIN): ai/ai.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements-dev.txt

run: ai
	$(PYTHON) main.py

test:
	$(PYTHON) -m pytest -q

clean:
	rm -f $(AI_BIN) log.txt
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
