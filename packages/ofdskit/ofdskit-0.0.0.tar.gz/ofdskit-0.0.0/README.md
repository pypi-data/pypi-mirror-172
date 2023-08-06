# OFDSKit

## Command line

### Installation

Installation from this git repo:

```bash
git clone https://github.com/Open-Telecoms-Data/ofdskit.git
cd ofdskit
python3 -m venv .ve
source .ve/bin/activate
pip install -e .
```

### Using

    ofdskit --help

### Running tests

    python -m pytest

### Code linting

Make sure dev dependencies are installed in your virtual environment:

    pip install -e .[dev]

Then run:

    isort ofdskit/ tests/ setup.py
    black ofdskit/ tests/ setup.py
    flake8 ofdskit/ tests/ setup.py
    mypy --install-types --non-interactive -p  ofdskit
