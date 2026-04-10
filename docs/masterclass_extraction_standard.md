# Masterclass Extraction Standard

## Old procedure

The old extractor optimized for compressed episode recap.

It asked the model for:
- episode
- title
- topics
- masterclass_summary

That produced assets that were useful as summaries, but weak as founder tools.
The failure mode was predictable:
- too much narration
- not enough repeatable doctrine
- not enough operator decisions
- not enough business tests
- not enough reusable frameworks

## New procedure

The new extractor is doctrine-first.
A masterclass is not a summary. It is an operator playbook extracted from the episode.

### Goal

Every masterclass must answer:
1. What repeatable startup axiom did this episode teach?
2. What decision rule should a founder apply next week?
3. What evidence standard separates signal from hype?
4. What operating move becomes obvious after reading this?

## Required output structure

Each extracted masterclass must produce these sections:

- `episode`
- `title`
- `topics`
- `core_question`
- `thesis`
- `axioms` (3-5 max)
- `decision_rules` (2-4 max)
- `proof_points` (specific metrics / facts / examples)
- `contrarian_take`
- `operator_playbook` (concrete steps)
- `watchouts` (ways founders misapply the lesson)
- `one_line_formula`

## Writing rules

- Prefer doctrine over recap
- Prefer rules over observations
- Prefer evidence over adjectives
- Prefer decisions over descriptions
- Pull out only what can be reused by another founder/operator
- Keep every axiom short enough to quote
- If the episode contains one strong line, elevate it into a pull quote or executive axiom

## What a good masterclass looks like

A good masterclass reads like:
- a partner memo
- a boardroom doctrine page
- a founder operating card

It does **not** read like:
- a YouTube summary
- a blog recap
- a timeline of who said what

## Minimum doctrine test

Before accepting an extraction, check:
- Can a founder act on this tomorrow?
- Is there a falsifiable business test in it?
- Is at least one axiom quotable?
- Are proof points concrete?
- Could this stand alone without the original episode?

If not, rewrite it.
