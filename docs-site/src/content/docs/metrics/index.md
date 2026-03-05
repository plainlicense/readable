---
title: Supported Metrics
description: A list of readability formulas supported by Readable.
---

Not sure which metric to use? The [Choosing a Metric](/readable/choosing-a-metric/) guide explains the differences.

Readable supports nine readability formulas:

- [**ARI** (Automated Readability Index)](/readable/metrics/ari/) — Character-based formula; reliable on technical documents; includes age ranges
- [**Coleman-Liau**](/readable/metrics/coleman-liau/) — Character-based formula; letters only; consistent results at scale
- [**Dale-Chall**](/readable/metrics/dale-chall/) — Word-list formula; validated for educational and health materials; grades 4+
- [**Flesch Reading Ease**](/readable/metrics/flesch/) — 0–100 ease score (higher = easier); most widely cited formula
- [**Flesch-Kincaid**](/readable/metrics/flesch-kincaid/) — US grade level; same inputs as Flesch; targets 75% comprehension
- [**Gunning Fog**](/readable/metrics/gunning-fog/) — Years of education needed; counts polysyllabic words; good for business prose
- [**Linsear Write**](/readable/metrics/linsear-write/) — Weighted syllable formula from the Bureau of Land Management (1966)
- [**SMOG**](/readable/metrics/smog/) — 30-sentence polysyllabic word count; targets 100% comprehension; health literacy standard
- [**Spache**](/readable/metrics/spache/) — Word-list formula for grades 1–3 only

Each metric provides a `score` and a `grade_level` (or `grade_levels` for more granular ranges). Some metrics provide additional data, like `ages` for ARI or `ease` for Flesch.
