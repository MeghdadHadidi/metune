# Content & Voice Template

This template is used by the design-lead agent to create project-specific content guidelines.

## Instructions for Design-Lead Agent

When creating the content voice skill:

1. Analyze the BRD for brand personality
2. Define tone based on target users
3. Create examples for common scenarios
4. Output to `.claude/skills/content-voice.md`

---

## Template Content (copy below this line)

```markdown
---
name: content-voice
description: Use when writing UI copy, error messages, help text, or any user-facing content for {{PROJECT_NAME}}. Provides voice, tone, and specific copy patterns.
---

# {{PROJECT_NAME}} Content & Voice Guide

## Brand Voice

{{BRAND_VOICE_DESCRIPTION}}

### Voice Attributes
- **{{ATTRIBUTE_1}}**: {{DESCRIPTION_1}}
- **{{ATTRIBUTE_2}}**: {{DESCRIPTION_2}}
- **{{ATTRIBUTE_3}}**: {{DESCRIPTION_3}}

## Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Success | {{SUCCESS_TONE}} | {{SUCCESS_EXAMPLE}} |
| Error | {{ERROR_TONE}} | {{ERROR_EXAMPLE}} |
| Empty state | {{EMPTY_TONE}} | {{EMPTY_EXAMPLE}} |
| Loading | {{LOADING_TONE}} | {{LOADING_EXAMPLE}} |
| Onboarding | {{ONBOARDING_TONE}} | {{ONBOARDING_EXAMPLE}} |

## Writing Principles

### Be Concise
- Headlines: 3-6 words
- Body text: 1-2 sentences max for UI
- Button labels: 1-3 words, verb-first

### Be Clear
- Use plain language (no jargon)
- Front-load important information
- One idea per sentence

### Be Helpful
- Tell users what to do, not just what went wrong
- Provide context when needed
- Offer next steps

## Common UI Copy Patterns

### Button Labels
| Action | Do | Don't |
|--------|-----|-------|
| Save | "Save" or "Save changes" | "Submit" |
| Delete | "Delete" or "Remove" | "Destroy" |
| Create | "Create {{item}}" | "Add new" |
| Confirm | "Confirm" | "OK" |
| Cancel | "Cancel" | "Go back" |

### Form Labels
- Use sentence case: "Email address" not "Email Address"
- Be specific: "Work email" not just "Email"
- Avoid redundancy: "Password" not "Enter your password"

### Placeholder Text
- Show format: "name@example.com"
- Don't repeat the label
- Use for hints only, not instructions

### Error Messages

Structure: **What happened** + **How to fix it**

Examples:
```
{{ERROR_EXAMPLE_1}}
{{ERROR_EXAMPLE_2}}
{{ERROR_EXAMPLE_3}}
```

### Empty States

Structure: **What this area is for** + **How to get started**

Example:
```
{{EMPTY_STATE_EXAMPLE}}
```

### Confirmation Dialogs

Structure: **Clear question** + **Consequence** + **Action options**

Example:
```
{{CONFIRMATION_EXAMPLE}}
```

### Loading States
- Under 2s: No text needed
- 2-10s: "Loading..." or specific "Loading your projects..."
- Over 10s: Show progress and be specific

### Success Messages
- Be specific: "Project saved" not "Success!"
- Include what happened
- Brief celebration is okay for milestones

## Terminology

Use these terms consistently:

| Preferred | Avoid |
|-----------|-------|
| {{TERM_1_PREFERRED}} | {{TERM_1_AVOID}} |
| {{TERM_2_PREFERRED}} | {{TERM_2_AVOID}} |
| {{TERM_3_PREFERRED}} | {{TERM_3_AVOID}} |

## Date & Time Format

- Dates: {{DATE_FORMAT}}
- Times: {{TIME_FORMAT}}
- Relative: "2 hours ago", "Yesterday", "Last week"

## Numbers

- Use commas for thousands: 1,000 not 1000
- Currency: {{CURRENCY_FORMAT}}
- Percentages: 50% not 50 percent
```
