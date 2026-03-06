<!--
SPDX-FileCopyrightText: 2026 PlainLicense

SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT
-->

# 📗 Readable
[![MIT license](https://img.shields.io/badge/License-MIT-green.svg)](https://lbesson.mit-license.org/)

Score the _readability_ of text using popular readability formulas and metrics including: [Flesch Kincaid Grade Level](#flesch-kincaid-grade-level), [Flesch Reading Ease](#flesch-reading-ease), [Gunning Fog Index](#gunning-fog), [Dale Chall Readability](#dale-chall-readability), [Automated Readability Index (ARI)](#automated-readability-index-ari), [Coleman Liau Index](#coleman-liau-index), [Linsear Write](#linsear-write), [SMOG](#smog), and [SPACHE](#spache). 📗

[![GitHub stars](https://img.shields.io/github/stars/plainlicense/readable.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/plainlicense/readable/stargazers/)

## Prerequisites

- Python 3.12 or higher
- NLTK data download required on first use: `python -c "import nltk; nltk.download('punkt_tab')"`

## Installation

```bash
pip install readable
```

## Quick Start

```python
from readable import Readability

text = """
In linguistics, the Gunning fog index is a readability test for English writing. 
The index estimates the years of formal education a person needs to understand 
the text on the first reading. For instance, a fog index of 12 requires the 
reading level of a United States high school senior (around 18 years old). 
The test was developed in 1952 by Robert Gunning, an American businessman 
who had been involved in newspaper and textbook publishing.
"""

r = Readability(text)

# Automated Readability Index (ARI)
ari = r.ari()
print(f"ARI Score: {ari.score}")
print(f"Grade Levels: {ari.grade_levels}")
print(f"Ages: {ari.ages}")

# Flesch Reading Ease
flesch = r.flesch()
print(f"Flesch Score: {flesch.score}")
print(f"Ease: {flesch.ease}")

# Flesch-Kincaid Grade Level
fk = r.flesch_kincaid()
print(f"FK Score: {fk.score}")
print(f"Grade Level: {fk.grade_level}")

# Get all statistics used for calculation
stats = r.statistics()
print(stats)

# For custom metrics, use r.stats (returns a StatSummary object)
print(r.stats)
```

For score interpretation, metric selection, and full API docs, see **[docs.plainlicense.org/readable](https://docs.plainlicense.org/readable/)**.

## About

Readable is a fork of the excellent [py-readability-metrics](https://github.com/cdimascio/py-readability-metrics) library by [Carmine DiMascio (@cdimascio)](https://github.com/cdimascio). We wanted to build on the great work that Carmine did, and add some additional features and metrics as an engine for future [Plain License](https://plainlicense.org/) projects, like our in-development CLI tool, [**plainr**](https://github.com/plainlicense/plainr) and similar plain language focused CI/CD tools. We also wanted to make some major breaking changes to the API and add robust typing support, so we decided to fork the project and start fresh.

## Supported Metrics

- **ARI** (Automated Readability Index)
- **Coleman-Liau** Index
- **Dale-Chall** Readability Score
- **Flesch** Reading Ease
- **Flesch-Kincaid** Grade Level
- **Gunning Fog** Index
- **Linsear Write** Formula
- **SMOG** Index
- **Spache** Readability Formula

## Acknowledgements

Readable is a fork of [py-readability-metrics](https://github.com/cdimascio/py-readability-metrics)
by [Carmine DiMascio](https://github.com/cdimascio). We are grateful for that foundation.
