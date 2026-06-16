# Quickstart Worked Example

One concrete pass through the skill: a single book chapter → an agent-native module. This shows the *shape* of the transformation, not a full distillation run.

## Input — raw book text

> **Chapter 7: Managing Childhood Overweight**
>
> "When a child's BMI-for-age crosses the 85th percentile, clinicians should first
> assess growth trajectory rather than a single measurement. Family meal structure
> is the strongest modifiable factor. Avoid framing weight as a moral failure, as
> shame predicts worse long-term outcomes and disordered eating."

This is linear prose. An agent cannot *route* on it. The chapter says what to think, not what to do next.

## Process — how the skill routes this

The skill turns the chapter into operational structures, not a shorter chapter. Three passes:

1. **Shared core** — pull the always-on rules: *use trajectory, not a single point; never use shame language; nutrition advice is high-risk and needs an evidence/referral gate.* These go in the kernel, loaded on every task.

2. **Expert selection** — the chapter is a routed expert, not chapter 7. It triggers on `childhood overweight / BMI percentile / family meals`. Sibling experts (`adult-weight`, `eating-disorder-screening`) stay closed unless their triggers fire. (See `reference/sparse-distillation-methodology.md`.)

3. **Missed-case sweep** — before answering, check the leaves the prose buried: *Is this actually an eating-disorder presentation? Does the BMI cross a referral red line? Is the guideline current?* (See the sweep in `SKILL.md` red lines.)

## Output — the distilled module

A `ROUTING.yaml` entry:

```yaml
childhood-overweight-expert:
  trigger_terms:
    strong: [childhood overweight, BMI-for-age, 85th percentile, family meals]
    weak: [pediatric weight, child diet]
  anti_triggers: [adult weight, athlete body composition]
  budget_default: routed_low
  neighbors:
    safety: [pediatric-referral-gate, stigma-free-language]
    adjacent: [eating-disorder-screening]
```

A checklist (what the agent *does*):

```markdown
- [ ] Use BMI-for-age trajectory across ≥2 points, not a single measurement
- [ ] Assess family meal structure first (strongest modifiable factor)
- [ ] Screen for eating-disorder signs before any restriction advice
- [ ] Use stigma-free, non-moralizing language
- [ ] Verify the percentile cutoff against a current guideline (refresh gate)
```

A decision tree (where the agent *branches*):

```text
BMI-for-age percentile?
├─ < 85th ........... reassure; reinforce family meal habits
├─ 85th–95th ........ family-based behavioral guidance; recheck trajectory
└─ > 95th ........... refer to clinician; do NOT prescribe restriction unsupervised
                      └─ eating-disorder signs present? → referral gate, stop diet advice
```

## The test

Compare the input prose to the output: the agent can now answer **"what do I do next?"** — route to the right expert, run the checklist, branch on the percentile, and stop at the referral gate — *without rereading chapter 7*. That is the difference between a summary and an agent-native skill.
