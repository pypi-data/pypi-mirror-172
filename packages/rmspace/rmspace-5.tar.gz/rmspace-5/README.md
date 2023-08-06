# rmspace

Remove trailing whitespace from code and other plain-text files.

## Usage

```bash
pip install rmspace

# Remove trailing whitespace.
python -m rmspace ./rmspace/rmspace/main.py

# Remove trailing whitespace, return 1 if any file was formatted.
# This is intended for linting in CI flows.
python -m rmspace ./rmspace/rmspace/main.py --check
```
