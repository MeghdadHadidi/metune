---
name: peachflow-research-patterns
description: This skill provides research and web search patterns for domain consultants and experts. Use when conducting market research, competitor analysis, industry standards research, or gathering domain knowledge. Applies automatically during discovery phase or when agents need external information.
---

# Peachflow Research Patterns

Effective research strategies for gathering domain knowledge, market data, and industry standards.

## Search Query Formulation

### Query Templates by Research Type

#### Market Size & Growth
```
"{industry} market size {current_year} {next_year} growth forecast"
"{product_type} industry statistics {current_year}"
"{market} total addressable market TAM"
```

#### Competitor Analysis
```
"{product_type} competitors comparison features pricing"
"top {product_type} companies {current_year}"
"{competitor_name} vs {competitor_name} comparison"
"{product_type} market leaders analysis"
```

#### Industry Standards
```
"{domain} industry standards regulations compliance {region}"
"{industry} best practices guidelines {current_year}"
"{domain} regulatory requirements {country}"
"{industry} certification requirements"
```

#### Technology Landscape
```
"{tech_category} frameworks tools comparison {current_year}"
"best {tech_type} for {use_case} {current_year}"
"{technology} alternatives comparison"
"{problem_domain} technical solutions overview"
```

#### User Research
```
"{user_type} pain points challenges {domain}"
"{user_segment} behavior study research"
"{product_type} user expectations survey"
"{industry} customer satisfaction trends"
```

#### Pricing & Business Models
```
"{product_type} pricing strategies {current_year}"
"{industry} SaaS pricing models"
"{product_type} monetization strategies"
"{competitor} pricing plans"
```

### Query Enhancement Techniques

| Technique | Example | Purpose |
|-----------|---------|---------|
| Year qualifier | `"react frameworks 2026"` | Recent data |
| Authority qualifier | `"UX research study"` | Credible sources |
| Exact phrase | `"user experience"` | Precise matches |
| Region filter | `"GDPR compliance EU"` | Geographic relevance |
| Format filter | `"market report PDF"` | Specific formats |

## Research Workflow

### Phase 1: Initial Exploration
1. Start with broad queries to understand landscape
2. Identify key players, terms, and concepts
3. Note recurring themes and terminology

### Phase 2: Deep Dive
1. Use discovered terminology for refined searches
2. Target specific competitors, standards, or technologies
3. Look for primary sources (research firms, official docs)

### Phase 3: Verification
1. Cross-reference important claims across sources
2. Check publication dates for recency
3. Verify authority of sources

### Phase 4: Synthesis
1. Organize findings by category
2. Identify patterns and insights
3. Note gaps requiring further research

## Source Evaluation

### High Authority Sources
- Research firms: Gartner, Forrester, McKinsey, Deloitte
- Industry associations and standards bodies
- Government regulatory agencies
- Academic research papers
- Official company documentation

### Medium Authority Sources
- Tech blogs from established companies
- Industry news sites (TechCrunch, The Verge)
- Professional community forums (Stack Overflow, Reddit tech subs)
- Conference presentations

### Use with Caution
- Wikipedia (good for overview, verify claims)
- Personal blogs (may be biased)
- Old articles (check date)
- Marketing materials (promotional bias)

## Output Formatting

### Market Research Output
```markdown
## Market Research: {Topic}

### Market Overview
- **Market Size**: ${X}B (2025), projected ${Y}B (2028)
- **CAGR**: X% (2025-2028)
- **Key Drivers**: [list]

### Key Players
| Company | Market Share | Strengths |
|---------|-------------|-----------|
| {Name} | X% | {list} |

### Trends
1. {Trend 1}: {description}
2. {Trend 2}: {description}

### Sources
- [{Source Name}]({URL}): {brief description}
```

### Competitor Analysis Output
```markdown
## Competitor Analysis: {Product Type}

### Competitor Matrix
| Feature | Us | Competitor A | Competitor B |
|---------|-----|--------------|--------------|
| {Feature 1} | {status} | {status} | {status} |

### Detailed Profiles

#### {Competitor Name}
- **Founded**: {year}
- **Funding**: ${X}M
- **Target Market**: {description}
- **Pricing**: {model and range}
- **Strengths**: {list}
- **Weaknesses**: {list}

### Sources
- [{Source}]({URL})
```

### Industry Standards Output
```markdown
## Industry Standards: {Domain}

### Regulatory Requirements
| Standard | Region | Requirements | Compliance Needed |
|----------|--------|--------------|-------------------|
| GDPR | EU | {requirements} | Yes/No |

### Best Practices
1. **{Practice}**: {description}
   - Implementation: {how}
   - Importance: {why}

### Certifications
- {Certification}: {description and relevance}

### Sources
- [{Official Body}]({URL})
```

## Search Strategy by Phase

### Discovery Phase
- Market size and opportunity
- Competitor landscape
- Industry standards and compliance
- Technology options
- User behavior patterns

### Planning Phase
- Technical implementation patterns
- Framework comparisons
- Architecture best practices
- Similar product case studies

### Implementation Phase
- Specific technical solutions
- Library/package comparisons
- Code patterns and examples
- Troubleshooting guides

## Tips for Effective Research

1. **Start broad, then narrow**: General queries → specific queries
2. **Use multiple sources**: Don't rely on single source
3. **Check dates**: Prefer recent information (last 2 years)
4. **Note confidence**: Mark findings as high/medium/low confidence
5. **Track sources**: Always save URLs for reference
6. **Identify gaps**: Note what couldn't be found
7. **Iterate**: Use findings to inform new searches
