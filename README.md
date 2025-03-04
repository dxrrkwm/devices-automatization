# 🧩Devices automatization

Python application that includes functionality for scanning QR codes, checking their validity, and handling different states based on the QR code content.

## 🐾Getting Started

### Prerequisites

- Python
- Poetry
- Make (Optional)

### Local Setup
#### 1. Install Dependencies
Run the following command to install dependencies using Poetry:
```bash
make deps
```
OR 
```bash
poetry install
```

#### 2. Run tests
```bash
pytest
```

#### 3. Run script
```bash
python do_it_yourself.py
```

## ⚙️Makefile Commands

- `make deps`: Install dependencies using Poetry.
- `make lint`: Run code linting with Ruff and isort.
- `make clean`: Remove `__pycache__` directories.
