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

### Changed
- GitHub username migrated from `alihsh0` to `u2n4` across all URLs, plugin manifests, marketplace owner metadata, and install commands

### Notes
- Security-hardening content (richer `SECURITY.md`, `SECURITY_CHANGELOG.md`, README security section) is staged on branch `wip/security-hardening-20260417` pending review before merge

## [1.0.0] - 2026-03-07

### Added
- MCP Config Fix skill — fixes UTF-8 BOM issue in Claude Desktop on Windows
- Claude Code Prompt Generator skill — professional prompts with Agent Teams
- Claude Code Plugin Marketplace support
- Installation via `/plugin marketplace add u2n4/ai-dev-skills`
