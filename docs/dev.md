# Developer Guide

## Setup

For development I'm using [conda](https://www.anaconda.com/) environment and for package management [poetry](https://python-poetry.org/)

Optionally create an environment with conda.

```bash
conda create -n notion-gcal-env python==3.9
conda install poetry
```

You can also use virtualenv from poetry, but that requires to have the python version installed on your system as well as poetry:

```bash
poetry config virtualenvs.in-project true
```

Install all relevant packages
```bash
poetry install
```

Initiate all [pre-commits](https://pre-commit.com/)

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

##

Commit messages:

```bash
git commit -m "fix: bug that is annoying"
```

From https://github.com/commitizen/conventional-commit-types/blob/v3.0.0/index.json
```json
{
  "types": {
    "feat": {
      "description": "A new feature",
      "title": "Features"
    },
    "fix": {
      "description": "A bug fix",
      "title": "Bug Fixes"
    },
    "docs": {
      "description": "Documentation only changes",
      "title": "Documentation"
    },
    "style": {
      "description": "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
      "title": "Styles"
    },
    "refactor": {
      "description": "A code change that neither fixes a bug nor adds a feature",
      "title": "Code Refactoring"
    },
    "perf": {
      "description": "A code change that improves performance",
      "title": "Performance Improvements"
    },
    "test": {
      "description": "Adding missing tests or correcting existing tests",
      "title": "Tests"
    },
    "build": {
      "description": "Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)",
      "title": "Builds"
    },
    "ci": {
      "description": "Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)",
      "title": "Continuous Integrations"
    },
    "chore": {
      "description": "Other changes that don't modify src or test files",
      "title": "Chores"
    },
    "revert": {
      "description": "Reverts a previous commit",
      "title": "Reverts"
    }
  }
}
```


## Other commands

Run tests

```bash
poetry run pytest
# with coverage
poetry run pytest --cov=.
```

Run black:
```bash
poetry run black .
```

Validating your pre-commits:

```bash
poetry run pre-commit run --all-files
```

```bash
Check Yaml...............................................................Passed
Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Don't commit to branch...................................................Passed
Mixed line ending........................................................Passed
Check Toml...............................................................Passed
Check for merge conflicts................................................Passed
flake8...................................................................Passed
black....................................................................Passed
pytest...................................................................Passed
```
