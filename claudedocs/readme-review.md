<!--
SPDX-FileCopyrightText: 2026 PlainLicense

SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT
-->

# README Review: Readable

Reviewed against: `readable/README.md` (current HEAD on `feat_modern_refactor`)
Reference files: `readable/readability.py`, `readable/types/results.py`, `readable/types/_interfaces.py`,
`docs-site/src/content/docs/index.mdx`, `docs-site/src/content/docs/metrics/index.md`,
`docs-site/src/content/docs/choosing-a-metric.md`, `pyproject.toml`, `readable/__about__.py`

---

## What Works

The README's fundamental structure is appropriate for its role: installation first, quick-start second, attribution last. The package name, import path (`from readable import Readability`), and all nine metric names in the "Supported Metrics" list are correct and match the current codebase. The quick-start text sample (the Gunning Fog description paragraph) is used consistently across the README, the docs site, and the choosing-a-metric guide, which is a good practice.

---

## Issues Found

### 1. Quick-start code has a broken indentation line (README line 34)

```python
# Automated Readability Index (ARI)
 ari = r.ari()   # <-- leading space before `ari`
```

Line 34 has a leading space before `ari = r.ari()`. This is a syntax error. The code block will not run as written.

---

### 2. `ari.grade_levels` does not exist on `ARIResult` — only `grade_level` (singular) and `ages`

README line 36:
```python
print(f"Grade Levels: {ari.grade_levels}")
```

`ARIResult` inherits `grade_levels: list[str]` from `GradeResult`, so this attribute does exist. However, the README prints it as `Grade Levels` (plural) and separately prints `ari.ages`, which is correct. This is accurate. No fix needed here.

---

### 3. `fk.grade_level` returns a string, not an int (README line 47)

README line 47:
```python
print(f"Grade Level: {fk.grade_level}")
```

`GradeResult.grade_level` is defined as a property that returns `str` (`self.grade_levels[0] if self.grade_levels else "na"`). The README print statement works fine, but the comment label says "Grade Level" without indicating the type. This is a minor omission rather than an error — it may confuse users who expect an integer and then try to do arithmetic on it. The docs site's metric pages correctly describe `grade_level` as returning a string. The README is just silent on the type.

---

### 4. `r.statistics()` returns a `dict`, not a printable object — the comment implies otherwise

README lines 50–51:
```python
stats = r.statistics()
print(stats)
```

`statistics()` does return a plain `dict`, so `print(stats)` works. But the comment "Get all statistics used for calculation" is slightly misleading: `statistics()` only returns a subset of six fields (letters, words, sentences, polysyllabic words, avg words per sentence, avg syllables per word). It omits `num_syllables`, `num_gunning_complex`, `num_dale_chall_complex`, and `num_spache_complex` that are on the underlying `StatSummary`. If a user needs the full stats object, they should use the `r.stats` property instead.

The README does not mention `r.stats` at all. A user extending the library (per `docs-site/guides/extending.md`) needs `r.stats`, not `r.statistics()`.

---

### 5. No score interpretation anywhere in the README

A user who runs the quick-start and gets `52.4` from `flesch().score` has no context for what that means. The docs site's `choosing-a-metric.md` has a worked example with inline comments explaining scores (e.g., `# ~52.4 → "fairly_difficult" → grades 10–12`), and `metrics/flesch.md` has a full interpretation table. None of this appears in the README, not even a pointer.

---

### 6. No link to the docs site

The docs site exists at `https://docs.plainlicense.org/readable/` and contains substantial content: nine per-metric pages, a metric selector guide, an extending guide, and an architecture reference. The README has no mention of it and no link to it. A user who installs the package from PyPI or finds the GitHub repo has no path to this documentation.

---

### 7. No Python version requirement stated

`pyproject.toml` requires `python >= 3.12`. The README says nothing about this. A user on Python 3.10 or 3.11 will install the package and get an error, with no prior indication of the requirement.

---

### 8. No NLTK prerequisite mentioned

The library requires an NLTK data download before any scoring will work (`nltk.download('punkt_tab')`). The CLAUDE.md project file notes this explicitly as a one-time step. The README has no mention of it. A user who installs the package and runs the quick-start example will get an NLTK `LookupError` with no warning in the README that this step was needed.

This is the most impactful missing item for new users. The error message NLTK produces is not obvious about the fix.

---

### 9. The Contributors section contains a contributor from the upstream repo, not this one

README lines 84–88 contain a `<table>` entry for `rbamos` with links pointing to `github.com/cdimascio/py-readability-metrics`. This is a contributor to the original `py-readability-metrics`, not to Readable. The all-contributors badge at line 3 shows `0` contributors, which contradicts the table entry below. This looks like the all-contributors tooling was partially initialized (the empty `<!-- ALL-CONTRIBUTORS-LIST -->` block at lines 73–79) and then the original upstream contributor table was left in from the fork.

If the intent is to credit the original contributors, the attribution is better placed in the "About" section, not in a "Contributors" section that implies these people contributed to this repo. If the intent is to track Readable's own contributors, the table should be empty or removed until actual contributors exist.

---

### 10. The "About" section refers to an in-development CLI

README line 56 mentions `plainr` as an "in-development CLI tool" with a link to `https://github.com/plainlicense/plainr`. If that repository does not yet exist publicly, this link will 404. This may or may not be intentional — worth verifying before the first release.

---

## Recommended Changes (Priority Order)

### Priority 1 — Fix the syntax error before any release

**What:** Remove the leading space on README line 34. Change ` ari = r.ari()` to `ari = r.ari()`.

**Why:** The quick-start code block will not run as written. This is the first thing a new user tries.

---

### Priority 2 — Add NLTK prerequisite to Installation section

**What:** Add a note immediately after the `pip install readable` line.

**Why:** New users will hit an `LookupError` without this. It is the most common failure mode for first-time users of any NLTK-dependent package.

**Example:**
```markdown
## Installation

```bash
pip install readable
```

Readable uses NLTK for tokenization. After installing, download the required data:

```python
import nltk
nltk.download('punkt_tab')
```

This is a one-time step. You do not need to repeat it in your code.
```

---

### Priority 3 — Add Python version requirement to Installation section

**What:** Add one line stating the Python requirement next to or just below the install command.

**Why:** `pyproject.toml` requires Python 3.12+. Users on older versions get no warning from the README.

**Example:**
```markdown
Requires Python 3.12 or later.
```

---

### Priority 4 — Add a docs site link

**What:** Add a "Documentation" section or a badge linking to `https://docs.plainlicense.org/readable/`.

**Why:** The docs site has the information users actually need after the quick-start: score interpretation tables, metric selection guidance, an extending guide, and architecture notes. Without a link, the docs site is invisible to anyone who finds the package on PyPI or GitHub.

**Example:** Place this near the top, between the badges and the Installation section:

```markdown
**[Full documentation at docs.plainlicense.org/readable](https://docs.plainlicense.org/readable/)**
```

Or add a docs badge next to the existing MIT badge.

---

### Priority 5 — Add minimal score interpretation to the quick-start

**What:** Add a one-paragraph note after the quick-start code block explaining how to read the output.

**Why:** A user who gets `52.4` from `flesch().score` has no context. The key facts are: Flesch scores 0–100 where higher is easier; grade-level metrics output US grade numbers; `ease` is a string label. The full interpretation tables live in the docs site — the README just needs to point users there.

**Example:**
```markdown
Flesch scores run from 0 to 100 — higher means easier. A score of 52 falls in the
"fairly difficult" range (grades 10–12). Grade-level metrics like `flesch_kincaid()`
and `ari()` return US grade numbers directly. See the [score interpretation tables](https://docs.plainlicense.org/readable/choosing-a-metric/) for all metrics.
```

---

### Priority 6 — Add a note about `r.stats` alongside `r.statistics()`

**What:** Either add a sentence to the quick-start comment or replace the `r.statistics()` call with `r.stats` (and explain both).

**Why:** `r.statistics()` returns a dict with six fields. `r.stats` returns the full `StatSummary` object used by all metrics. Users who extend the library need `r.stats`, not `r.statistics()`. The README mentions only the dict version, which sets incorrect expectations for anyone reading the extending guide.

**Example comment addition:**
```python
# Get a summary dict of six key statistics
stats = r.statistics()
print(stats)

# For the full StatSummary object (needed for custom metrics), use r.stats
# print(r.stats)
```

---

### Priority 7 — Clean up the Contributors section

**What:** Remove the `<table>` entry for `rbamos` (README lines 84–88), or move the credit to the "About" section. Keep or remove the all-contributors infrastructure depending on whether it will be actively used.

**Why:** The `rbamos` entry links to the upstream repo and implies that person contributed to Readable, which is misleading. The badge shows `0` contributors, contradicting the table. The section is internally inconsistent.

If you plan to use all-contributors going forward, remove the upstream table entry and let the bot populate the list from actual Readable contributions. If you do not plan to use all-contributors, remove the entire section and the badge at line 3.

**If keeping the attribution:** Move it to the "About" section where it is clearly framed as upstream credit, not Readable contributions:
```markdown
Readable is built on the work of Carmine DiMascio and contributors to
[py-readability-metrics](https://github.com/cdimascio/py-readability-metrics).
```

---

## What NOT to Touch

- **The "About" section (line 56):** The framing of Readable as a fork with breaking API changes and robust typing is accurate and appropriate. The mention of Plain License and plainr is intentional project context. Do not change the substance; the only potential issue is the `plainr` link if that repo is not yet public.

- **The metric list (lines 60–68):** All nine metrics are correct, complete, and match what the codebase implements. The names and ordering match the docs site.

- **The quick-start text sample:** The Gunning Fog paragraph used as example text is used consistently across the README, `choosing-a-metric.md`, and the Flesch metric page. Changing it in the README would create inconsistency with the docs.

- **The badge links (lines 3, 5, 9):** The MIT license badge and GitHub stars badge are correct. The all-contributors badge count (`0`) is technically accurate for this repo, though the section inconsistency noted above applies.

- **The import statement:** `from readable import Readability` is correct. `Readability` is exported from `readable/__init__.py`.

- **The metric method names:** `r.ari()`, `r.flesch()`, `r.flesch_kincaid()`, `r.gunning_fog()`, `r.dale_chall()`, `r.coleman_liau()`, `r.linsear_write()`, `r.smog()`, `r.spache()` — all correct and present on `Readability`.
