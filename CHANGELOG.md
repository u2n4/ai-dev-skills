# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-17

### Added
- `.editorconfig` for consistent cross-editor formatting
- `.gitattributes` enforcing LF line endings
- `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1)
- `SECURITY.md` disclosure policy (GitHub private advisories)
- GitHub Actions CI workflow (marketplace + plugin manifest JSON validation)
- Dependabot weekly updates for GitHub Actions

#### Security hardening (rebased from `wip/security-hardening-20260417` into this branch)
- `SECURITY.md` rewritten with full security model: supported versions, content-integrity rules, API-key safety guarantees, plugin-manifest integrity, command-safety bounds for `mcp-config-fix`, post-installation verification checklist, and contributor security checklist
- `SECURITY_CHANGELOG.md` (new) — incident-style log of the hardening pass with severity-tagged entries (CRITICAL-3.x, HIGH-3.x, LOW-3.x)
- `.gitignore` extended with secret-leakage patterns (`*.key`, `*.pem`, `id_rsa`, `credentials.json`, `*secret*`, etc.)
- `README.md` adds `## ⚠️ Security` section linking to `SECURITY.md` with key warnings (forks, command auditing, env-var-only secrets)
- `llms.txt` adds Security Context block aimed at LLMs reading the marketplace
- `plugin.json` (both plugins) adds explicit `permissions[]` and `integrity_hash` placeholder fields
- `marketplace.json` adds `last_reviewed` date and `_security_note` for installer-side hash verification
- `SKILL.md` (mcp-config-fix) heavily expanded with safety-bound execution rules and forbidden-action list
- `SKILL.md` (prompt-generator) tightened around safe placeholder usage

### Changed
- GitHub username migrated from `alihsh0` to `u2n4` across all URLs, plugin manifests, marketplace owner metadata, and install commands

## [1.0.0] - 2026-03-07

### Added
- MCP Config Fix skill — fixes UTF-8 BOM issue in Claude Desktop on Windows
- Claude Code Prompt Generator skill — professional prompts with Agent Teams
- Claude Code Plugin Marketplace support
- Installation via `/plugin marketplace add u2n4/ai-dev-skills`
