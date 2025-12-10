# Makefile для Artillery 3
# Автоматизация сборки и тестирования

# Определяем интерпретатор Python (можно переопределить через окружение)
PYTHON = python3

# Пути к файлам
SRC = artillery3.py
TEST = test_artillery3.py
REQS = requirements.txt

# Цели по умолчанию (выполняется при запуске просто `make`)
.PHONY: default
default: help

# Основная цель - сборка проекта
.PHONY: build
build: check-deps
	@echo "=== Building Artillery 3 ==="
	@chmod +x $(SRC)
	@echo "Build complete. Run 'make run' to start the game."

# Проверка и установка зависимостей
.PHONY: check-deps
check-deps:
	@echo "=== Checking dependencies ==="
	@if [ -f $(REQS) ]; then \
		echo "Installing requirements..."; \
		$(PYTHON) -m pip install -r $(REQS); \
	else \
		echo "requirements.txt not found, skipping..."; \
	fi

# Запуск игры
.PHONY: run
run: build
	@echo "=== Starting Artillery 3 ==="
	@$(PYTHON) $(SRC)

# Запуск в режиме тестирования
.PHONY: test-run
test-run: build
	@echo "=== Starting Artillery 3 (Test Mode) ==="
	@$(PYTHON) $(SRC) --test

# Запуск unit-тестов
.PHONY: test
test: build
	@echo "=== Running tests ==="
	@$(PYTHON) -m pytest $(TEST) -v

# Создание requirements.txt
.PHONY: reqs
reqs:
	@echo "=== Generating requirements.txt ==="
	@$(PYTHON) -m pip freeze | grep -E "(pytest|numpy)" > $(REQS) || echo "Creating empty requirements.txt" && touch $(REQS)
	@echo "Requirements file created/updated."

# Сборка для Web (используя Pyodide)
.PHONY: web
web: build
	@echo "=== Building for Web ==="
	@echo "Note: Web version requires additional setup with Pyodide or Brython"
	@mkdir -p web_build
	@cp $(SRC) web_build/
	@cp README.md web_build/
	@echo "Basic web structure created in 'web_build/' directory."

# Сборка исполняемого файла для Windows (через PyInstaller)
.PHONY: windows
windows: check-deps
	@echo "=== Building Windows executable ==="
	@if ! command -v pyinstaller >/dev/null 2>&1; then \
		echo "Installing PyInstaller..."; \
		$(PYTHON) -m pip install pyinstaller; \
	fi
	@pyinstaller --onefile --name artillery3 $(SRC) || echo "PyInstaller not fully configured. Run manually: pyinstaller --onefile artillery3.py"
	@echo "Windows executable built in 'dist/' directory."

# Сборка для Android (заглушка - требуется Kivy/BeeWare)
.PHONY: android
android:
	@echo "=== Android build placeholder ==="
	@echo "To build for Android, you need to setup Kivy or BeeWare."
	@echo "See: https://kivy.org/doc/stable/guide/packaging-android.html"

# Запуск линтера для проверки кода
.PHONY: lint
lint:
	@echo "=== Linting Python code ==="
	@if command -v pylint >/dev/null 2>&1; then \
		pylint $(SRC) $(TEST); \
	else \
		echo "pylint not installed. Run: pip install pylint"; \
	fi

# Проверка типа данных (type checking)
.PHONY: type-check
type-check:
	@echo "=== Type checking ==="
	@if command -v mypy >/dev/null 2>&1; then \
		mypy $(SRC) $(TEST); \
	else \
		echo "mypy not installed. Run: pip install mypy"; \
	fi

# Очистка проекта
.PHONY: clean
clean:
	@echo "=== Cleaning project ==="
	@rm -rf __pycache__
	@rm -rf *.pyc
	@rm -rf build
	@rm -rf dist
	@rm -rf *.spec
	@rm -rf web_build
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Project cleaned."

# Показать справку
.PHONY: help
help:
	@echo "Artillery 3 - Build System"
	@echo ""
	@echo "Available commands:"
	@echo "  make build      - Install dependencies and prepare project"
	@echo "  make run        - Run the game"
	@echo "  make test-run   - Run game in test mode"
	@echo "  make test       - Run unit tests"
	@echo "  make web        - Prepare web version"
	@echo "  make windows    - Build Windows executable (requires PyInstaller)"
	@echo "  make android    - Android build placeholder"
	@echo "  make lint       - Check code quality"
	@echo "  make type-check - Type checking (requires mypy)"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make help       - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make build && make run"
	@echo "  make test"

# Псевдонимы для удобства
.PHONY: all
all: build test

.PHONY: check
check: lint type-check test
