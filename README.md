# MeTune Plugin Marketplace

A curated marketplace of Claude Code plugins focused on developer experience (DX). Enhance your CLI-based AI development workflow with professional-grade tools.

## What's Inside

| Plugin | Description | Version |
|--------|-------------|---------|
| **[Peachflow](./peachflow)** | Your AI development team in a CLI. Orchestrates specialized agents through the entire software lifecycle—from idea to implementation. | 2.3.0 |

## Installation

### Option 1: Add from GitHub (Recommended)

```bash
/plugin marketplace add MeghdadHadidi/metune
```

Then install the plugins you want:

```bash
/plugin install peachflow@meghdadhadidi-metune
```

### Option 2: Clone and Load Locally

```bash
# Clone the repository
git clone https://github.com/MeghdadHadidi/metune.git

# Load plugins directly during development/testing
claude --plugin-dir ./metune/peachflow
```

Or add to your settings for persistent use:

```json
// ~/.claude/settings.json
{
  "plugins": ["/path/to/metune/peachflow"]
}
```

## Copilot Compatibility

This marketplace is fully compatible with **GitHub Copilot in VS Code** (agent mode). The plugins work seamlessly with Copilot's chat interface when configured as Claude Code extensions.

To use with Copilot:
1. Install the plugins using either method above
2. Access plugin commands through Copilot chat using the same slash command syntax (e.g., `/peachflow:init`)

## Quick Start

Once installed, try Peachflow:

```bash
# Initialize a new project
/peachflow:init

# Start discovery for a new idea
/peachflow:discover "your product idea"

# Or analyze an existing codebase
/peachflow:analyze
```

## Available Plugins

### Peachflow

Professional product development workflow that simulates a complete software engineering team:

```
  idea ──► discover ──► define ──► design ──► plan ──► implement ──► ship
              │            │          │         │           │
          analysts    requirements   UX &    roadmap    developers
          research    engineers    architects  tasks    build code
```

**Features:**
- 13 specialized AI agents (business analyst, UX designer, developers, etc.)
- 9 workflow commands for each development phase
- Automated documentation generation (BRD, PRD, FRD, architecture docs)
- Sprint planning and task management
- Technical debt tracking

[View Peachflow Documentation →](./peachflow/README.md)

## Requirements

- Claude Code CLI v1.0.33 or higher (run `claude --version` to check)
- Node.js 18+ (for some plugin scripts)

## Contributing

Want to add a plugin to this marketplace? See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - see individual plugins for their specific licenses.

---

**Maintained by [Meghdad Hadidi](https://github.com/MeghdadHadidi)**
