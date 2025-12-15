# Makefile for Artillery 3 Python Port

.PHONY: all run test clean

all: check

check:
	@echo "Checking Python version..."
	@python --version || (echo "Python 3 is required"; exit 1)

run: check
	@python artillery3.py

test: check
	@python test_artillery3.py

lint: check
	@echo "Running linter..."
	@pylint artillery3.py || true

clean:
	@echo "Cleaning up..."
	@rm -f *.pyc
	@rm -rf __pycache__

# For cross-platform packaging (example)
package: check
	@echo "Creating distribution package..."
	@zip -r artillery3_python.zip artillery3.py README.md LICENSE Makefile test_artillery3.py
