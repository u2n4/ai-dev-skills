<!-- SECURITY: CRITICAL-3.2 -->
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.1.x   | Yes       |
| 1.0.x   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in this project:

1. **DO NOT** open a public issue
2. Report privately via [GitHub Security Advisories](https://github.com/alihsh0/ai-dev-skills/security/advisories/new)
3. Include a clear description, reproduction steps, and potential impact
4. You will receive a response within 48 hours

## Security Model

This is a **static plugin marketplace** — there is no runtime server, no executable code, and no data collection. Security is focused on:

### Content Integrity
- All skill files (SKILL.md) contain **instructional content only**
- No skill should ever instruct users to download or execute external scripts
- All command examples are scoped to their declared purpose

### API Key Safety
- **No hardcoded API keys** in any file — all examples use `${ENV_VAR}` placeholders
- Skills must never ask users to paste API keys into prompts or chat
- Environment variables are the only acceptable method for secret injection

### Plugin Manifest Integrity
- Each `plugin.json` declares explicit `permissions` for what the skill can do
- `integrity_hash` fields should be verified against published release hashes
- `marketplace.json` includes `last_reviewed` date for audit trail

### Command Safety (mcp-config-fix)
The MCP Config Fix skill only uses PowerShell commands that:
- Read/write `claude_desktop_config.json` in `%APPDATA%\Claude\`
- Create backup copies of the config file
- List directories to locate config paths
- Locate Python installations via `where.exe`
- Stop only Claude Desktop processes (never Claude Code)
- Validate JSON structure

Commands that are **explicitly forbidden**:
- Downloading files from the internet
- Executing remote scripts
- Reading files outside `%APPDATA%\Claude\`
- Modifying system settings or registry
- Deleting non-config files

## Post-Installation Verification

After installing any plugin from this marketplace:

1. **Review the SKILL.md** — read all instructions before running any command
2. **Check permissions** — verify `plugin.json` permissions match expected behavior
3. **Verify source** — ensure the plugin was installed from `alihsh0/ai-dev-skills`
4. **Check for forks** — forked versions may contain modifications; always prefer the original

## Security Checklist for Contributors

Before submitting a PR:
- [ ] No hardcoded secrets (API keys, tokens, passwords)
- [ ] All examples use `${ENV_VAR}` placeholders for sensitive values
- [ ] No commands that download or execute external content
- [ ] No commands that access files outside the skill's declared scope
- [ ] `plugin.json` permissions accurately reflect skill capabilities
- [ ] No instructions that could trick users into exposing credentials
