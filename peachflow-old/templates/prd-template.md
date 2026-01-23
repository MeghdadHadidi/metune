---
product: {product-name}
document: prd
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
owner: product-manager
---

# Product Requirements Document: {Product Name}

## Strategic Questions Checklist

> **Instructions**: Before completing this document, ensure you can answer these fundamental questions. Unclear answers indicate discovery gaps.

### Problem Definition

| Question | Answer | Confidence |
|----------|--------|------------|
| Can we articulate the problem in one sentence that makes a stranger nod? | | |
| What's the cost of NOT solving this (quantified in time/money/pain)? | | |
| Are we solving the whole problem, or just a symptom? | | |

### Scope & Focus

| Question | Answer | Confidence |
|----------|--------|------------|
| What is the ONE thing this product must do exceptionally well to win? | | |
| What features are we explicitly NOT building, and why? | | |
| What's our MVP bar — functional, usable, or lovable? | | |

### Success Metrics

| Question | Answer | Confidence |
|----------|--------|------------|
| What single metric, if improved 10x, proves product-market fit? | | |
| How will we know in 30 days if we're on the right track? | | |
| What user behavior indicates they "get it" without being told? | | |

### Prioritization Logic

| Question | Answer | Confidence |
|----------|--------|------------|
| For each feature: acquisition, activation, retention, or revenue impact? | | |
| Are we building highest-leverage features first? | | |
| What would a competitor do to make our roadmap irrelevant? | | |

### Risk Validation

| Question | Answer | Confidence |
|----------|--------|------------|
| What assumption, if wrong, invalidates the entire product? | | |
| Which features have highest technical risk? Should we prototype? | | |
| What's the minimal path to proving/disproving our core hypothesis? | | |

### Kill-the-Project Check

> **STOP if any of these are true:**
> - [ ] Can't articulate the problem clearly
> - [ ] No measurable success metric defined
> - [ ] Core hypothesis cannot be tested quickly
> - [ ] ROI assumptions are unrealistic

---

## Executive Summary

{2-3 paragraph overview of the product, the problem it solves, and the opportunity}

---

## Problem Statement

### Current State
{What exists today? What's broken or missing?}

### Impact
{Cost of the problem - time, money, frustration, missed opportunity}

### Opportunity
{Market size, growth potential}
[Reference: domain-research.md]

---

## Target Users

### Primary Persona: {Name}
[From user-personas.md]
- **Segment**: {User segment}
- **Demographics**: {Key demographics}
- **Goals**: {What they're trying to achieve}
- **Pain Points**: {Current frustrations}
- **Current Solutions**: {How they solve this today}

### Secondary Persona: {Name}
[From user-personas.md]
- ...

---

## Product Vision

### Vision Statement
{One sentence describing the ideal future state}

### Value Proposition
{Why users will choose this over alternatives}

### Success Metrics

| Metric | Baseline | Target | Timeframe |
|--------|----------|--------|-----------|
| {KPI 1} | {current} | {goal} | {when} |
| {KPI 2} | {current} | {goal} | {when} |
| {KPI 3} | {current} | {goal} | {when} |

---

## Feature Requirements

### Core Features (MVP)

| ID | Feature | Description | Priority | Effort |
|----|---------|-------------|----------|--------|
| F001 | {Feature} | {Description} | Must Have | M |
| F002 | {Feature} | {Description} | Must Have | L |
| F003 | {Feature} | {Description} | Should Have | S |

### Future Features

| ID | Feature | Description | Phase |
|----|---------|-------------|-------|
| F010 | {Feature} | {Description} | Q2 |
| F011 | {Feature} | {Description} | Q3 |

---

## User Journeys

### Journey 1: {Name}
[From user-journeys.md]

{Summary of the journey}

### Journey 2: {Name}
{Summary}

---

## Non-Functional Requirements

### Performance
[NEEDS CLARIFICATION: Expected scale and performance requirements]

### Security
{Security requirements}
[Reference: domain-research.md for compliance]

### Accessibility
- WCAG Level: [NEEDS CLARIFICATION: AA or AAA?]
- Platforms: [NEEDS CLARIFICATION: Web, mobile, desktop?]

---

## Constraints

### Technical
[From architecture.md]
- {Constraint 1}
- {Constraint 2}

### Business
- Budget: [NEEDS CLARIFICATION]
- Timeline: [NEEDS CLARIFICATION]
- Team: [NEEDS CLARIFICATION]

### Regulatory
[From domain-research.md]
- {Regulation 1}
- {Regulation 2}

---

## Monetization Strategy

[NEEDS CLARIFICATION: Pricing model and revenue targets]

Options to consider:
- Freemium
- Subscription
- Usage-based
- Enterprise licensing

---

## Competitive Positioning

[From domain-research.md]

| Competitor | Our Advantage | Their Advantage |
|------------|---------------|-----------------|
| {Name} | {What we do better} | {What they do better} |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | Medium | High | {Strategy} |
| {Risk 2} | Low | High | {Strategy} |

---

## Success Criteria

Before launch:
- [ ] {Measurable criterion 1}
- [ ] {Measurable criterion 2}
- [ ] {Measurable criterion 3}

---

## Appendices

- A: [Domain Research](domain-research.md)
- B: [User Personas](user-personas.md)
- C: [User Journeys](user-journeys.md)
- D: [Design Vision](design-vision.md)
- E: [Architecture](architecture.md)
