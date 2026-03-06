---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Supported Metrics
description: A list of readability formulas supported by readscore.
---

Not sure which metric to use? The [Choosing a Metric](/readscore/choosing-a-metric/) guide explains the differences.

readscore supports nine readability formulas:

- [**ARI** (Automated Readability Index)](/readscore/metrics/ari/) — Character-based formula; reliable on technical documents; includes age ranges
- [**Coleman-Liau**](/readscore/metrics/coleman-liau/) — Character-based formula; letters only; consistent results at scale
- [**Dale-Chall**](/readscore/metrics/dale-chall/) — Word-list formula; validated for educational and health materials; grades 4+
- [**Flesch Reading Ease**](/readscore/metrics/flesch/) — 0–100 ease score (higher = easier); most widely cited formula
- [**Flesch-Kincaid**](/readscore/metrics/flesch-kincaid/) — US grade level; same inputs as Flesch; targets 75% comprehension
- [**Gunning Fog**](/readscore/metrics/gunning-fog/) — Years of education needed; counts polysyllabic words; good for business prose
- [**Linsear Write**](/readscore/metrics/linsear-write/) — Weighted syllable formula from the Bureau of Land Management (1966)
- [**SMOG**](/readscore/metrics/smog/) — 30-sentence polysyllabic word count; targets 100% comprehension; health literacy standard
- [**Spache**](/readscore/metrics/spache/) — Word-list formula for grades 1–3 only

Each metric provides a `score` and a `grade_level` (or `grade_levels` for more granular ranges). Some metrics provide additional data, like `ages` for ARI or `ease` for Flesch.
