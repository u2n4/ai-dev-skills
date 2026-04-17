<div align="center">
  <img src="assets/banner.png" alt="AI Dev Skills" width="100%">

  <h1>AI Dev Skills</h1>
  <p><strong>Claude Code plugin marketplace — MCP config fixer + professional prompt generator skills</strong></p>

  <p>
    <a href="#"><img src="https://img.shields.io/badge/Claude_Code-Plugin-purple?style=for-the-badge" alt="Claude Code"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT"></a>
    <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge" alt="Platform"></a>
    <a href="#"><img src="https://img.shields.io/badge/Skills-2-orange?style=for-the-badge" alt="Skills"></a>
  </p>

  <p>
    <a href="#installation">Installation</a> •
    <a href="#skills">Skills</a> •
    <a href="#mcp-config-fix">MCP Config Fix</a> •
    <a href="#prompt-generator">Prompt Generator</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>

---

## What is This?

AI Dev Skills is a Claude Code plugin marketplace that provides developer productivity skills. Install the marketplace once, then pick and choose the skills you need.

## Installation

```
/plugin marketplace add u2n4/ai-dev-skills
```

Then browse and install individual skills from the marketplace.

## Skills

### MCP Config Fix

Fixes the UTF-8 BOM issue that prevents Claude Desktop from loading MCP servers on Windows. This is one of the most common issues Windows users face.

**Triggers:**
- "MCP tools not showing up"
- "Config keeps getting deleted"
- "Claude Desktop not loading servers"
- "Add MCP server to config"

**What it does:**
1. Kills Claude Desktop safely (without killing Claude Code)
2. Reads existing config to preserve settings
3. Rewrites config WITHOUT UTF-8 BOM using `[System.IO.File]::WriteAllText()`
4. Verifies no BOM exists
5. Validates JSON
6. Handles MSIX virtualization edge case

### Prompt Generator

Generate professional, structured prompts for Claude Code with Agent Teams patterns, multi-phase workflows, and skill-aware orchestration.

**Triggers:**
- "Create a Claude Code prompt"
- "Set up an Agent Team"
- "Design a workflow"
- "Generate instructions for Claude Code"

**What it provides:**
- 5-Layer prompt structure (Context, Task, Requirements, Agent Team, Output Controls)
- 4 ready-to-use templates (Feature Implementation, Multi-Repo, Bug Fix, API Development)
- 4 Agent Team patterns (Research→Execute, Parallel Specialists, Iterative, Pipeline)
- Best practices checklist

## Architecture

```
ai-dev-skills/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace manifest
├── plugins/
│   ├── mcp-config-fix/      # MCP Config Fix skill
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       └── mcp-config-fix/
│   │           └── SKILL.md
│   └── prompt-generator/    # Prompt Generator skill
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── prompt-generator/
│               └── SKILL.md
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

<!-- SECURITY: LOW-3.7 — Security section in README -->
## ⚠️ Security

See [SECURITY.md](SECURITY.md) for full security policy, vulnerability reporting, and the threat model for this project.

**Important warnings:**
- **Forked versions** of this marketplace may contain modified skill files with different behavior. Always verify you are installing from `alihsh0/ai-dev-skills`.
- **Never run commands** from any skill without reading them first.
- **Never paste API keys** directly into config examples — use environment variables.
- Report security issues privately via [GitHub Security Advisories](https://github.com/alihsh0/ai-dev-skills/security/advisories/new).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

## Support

If you find this useful, please star this repository!

---

Made with ❤️ in the Eastern Province of Saudi Arabia.
