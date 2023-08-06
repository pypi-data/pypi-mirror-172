# TCGPlayer Wrapper

[![PyPI - Python](https://img.shields.io/pypi/pyversions/TCGPlayer-Wrapper.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/TCGPlayer-Wrapper/)
[![PyPI - Status](https://img.shields.io/pypi/status/TCGPlayer-Wrapper.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/TCGPlayer-Wrapper/)
[![PyPI - Version](https://img.shields.io/pypi/v/TCGPlayer-Wrapper.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/TCGPlayer-Wrapper/)
[![PyPI - License](https://img.shields.io/pypi/l/TCGPlayer-Wrapper.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/Black-Enabled-000000?style=flat-square)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/Imports-isort-informational?style=flat-square)](https://pycqa.github.io/isort/)
[![Flake8](https://img.shields.io/badge/Flake8-Enabled-informational?style=flat-square)](https://github.com/PyCQA/flake8)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/TCGPlayer-Wrapper.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/TCGPlayer-Wrapper/graphs/contributors)

[![Read the Docs](https://img.shields.io/readthedocs/tcgplayer-wrapper?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://tcgplayer-wrapper.readthedocs.io/en/latest/?badge=latest)
[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/TCGPlayer-Wrapper/Code%20Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/TCGPlayer-Wrapper/actions/workflows/code-analysis.yaml)
[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/TCGPlayer-Wrapper/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/TCGPlayer-Wrapper/actions/workflows/testing.yaml)

A [Python](https://www.python.org/) wrapper for the [TCGPlayer](https://tcgplayer.com) API.

## Installation

### PyPI

1. Make sure you have [Python](https://www.python.org/) installed: `python --version`
2. Install the project from PyPI: `pip install tcgplayer-wrapper`

### Github

1. Make sure you have [Python](https://www.python.org/) installed: `python --version`
2. Clone the repo: `git clone https://github.com/Buried-In-Code/TCGPlayer-Wrapper`
3. Install the project: `pip install .`

## Example Usage

```python
from tcgplayer.service import TCGPlayer
from tcgplayer.sqlite_cache import SQLiteCache

session = TCGPlayer(client_id="Client ID", client_secret="Client Secret", cache=SQLiteCache())

# List Games
results = session.list_categories()
for game in results:
    print(f"{game.category_id} | {game.display_name}")

# List Magic: the Gathering Expansions
results = session.list_category_groups(category_id=1)
for expansion in results:
    print(f"{expansion.group_id} | [{expansion.abbreviation}] - {expansion.name}")

# Get Product and Prices via product ID
result = session.product(product_id=257275)
prices = session.product_prices(product_id=257275)
print(f"{result.clean_name} ${prices.market_price:,.2f}")
```

## Socials

[![Social - Discord](https://img.shields.io/badge/Discord-The--DEV--Environment-7289DA?logo=Discord&style=flat-square)](https://discord.gg/nqGMeGg)
