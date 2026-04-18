# Security Changelog

All security fixes applied on 2026-03-08, organized by severity.

---

## CRITICAL

### Fix 3.1 — Skill Content Safety Hardening
**File:** `plugins/mcp-config-fix/skills/mcp-config-fix/SKILL.md`

| Change | Description |
|--------|-------------|
| Security notice added | Prominent warning section at top of SKILL.md with 4 safety rules |
| API key placeholders | Replaced all hardcoded key examples (`"key_here"`, `"key1"`, `"key2"`) with `${ENV_VAR}` references |
| Backup step added | New Step 2 creates timestamped backup before any config modification |
| JSON integrity check | Step 6 validates JSON after every config write |
| Command safety rules | New section explicitly listing allowed and forbidden PowerShell commands |
| Step renumbering | Steps renumbered (2-7 → 2-8) to accommodate backup step |

### Fix 3.2 — Marketplace Manifest Integrity
**Files:** `.claude-plugin/marketplace.json`, `plugins/*/. claude-plugin/plugin.json`, `SECURITY.md`

| Change | Description |
|--------|-------------|
| Version bump | All manifests updated from 1.0.0 to 1.1.0 |
| `last_reviewed` field | Added to marketplace.json with date 2026-03-08 |
| `_security_note` field | Added to marketplace.json with installation verification guidance |
| `permissions` field | Added to both plugin.json files declaring explicit capability scopes |
| `integrity_hash` field | Added to both plugin.json files (placeholder for release signing) |
| SECURITY.md created | New file at repo root with full security policy, threat model, and contributor checklist |

---

## HIGH

### Fix 3.3 — MCP Server Entry Validation
**File:** `plugins/mcp-config-fix/skills/mcp-config-fix/SKILL.md`

| Change | Description |
|--------|-------------|
| Validation checklist | Added 5-item checklist for verifying each mcpServers entry field |
| Known-safe paths | Listed standard Windows paths for Python, Node, and npx executables |
| Red flags section | Documented suspicious patterns that should trigger investigation |

### Fix 3.4 — API Key Exposure Prevention
**Files:** `plugins/prompt-generator/skills/prompt-generator/SKILL.md`, `plugins/mcp-config-fix/skills/mcp-config-fix/SKILL.md`, `.gitignore`

| Change | Description |
|--------|-------------|
| Prompt generator constraints | Added security constraints section forbidding keys in generated prompts |
| API Key Safety section | Added to mcp-config-fix with env var setup instructions |
| Quality checklist updated | Added "no secrets in examples" item to prompt-generator checklist |
| .gitignore hardened | Added entries for `.env.*`, `*.key`, `*.pem`, `credentials.json`, SSH keys, etc. |
| Full audit | Confirmed no real API keys exist in any repo file |

---

## MEDIUM

### Fix 3.5 — Config Corruption Protection
**File:** `plugins/mcp-config-fix/skills/mcp-config-fix/SKILL.md`

| Change | Description |
|--------|-------------|
| Merge safety guidance | Added 5-step merge process (read → parse → merge → preserve → write) |
| Config Health Check | Added comprehensive PowerShell validation script checking JSON validity, mcpServers presence, preferences section, BOM absence, and file size |

### Fix 3.6 — Safe Process Termination
**File:** `plugins/mcp-config-fix/skills/mcp-config-fix/SKILL.md`

| Change | Description |
|--------|-------------|
| Manual closure preferred | Added explicit recommendation for manual quit via system tray |
| Safe vs dangerous commands | Listed safe automated termination command and 4 dangerous alternatives to avoid |
| Claude Code protection | Explicitly documented that `Stop-Process -Name "Claude"` kills Claude Code |

---

## LOW

### Fix 3.7 — Documentation Improvements
**Files:** `README.md`, `CONTRIBUTING.md`, `llms.txt`

| Change | Description |
|--------|-------------|
| README security section | Added with link to SECURITY.md and warnings about forks, commands, and API keys |
| CONTRIBUTING checklist | Added 10-item security review checklist for pull request authors |
| llms.txt security context | Added section describing security model for LLM consumers |

---

## Summary

| Severity | Fixes | Files Modified | Files Created |
|----------|-------|---------------|---------------|
| CRITICAL | 2 | 3 | 1 (SECURITY.md) |
| HIGH | 2 | 3 | 0 |
| MEDIUM | 2 | 1 | 0 |
| LOW | 1 | 3 | 0 |
| **Total** | **7** | **8 unique files** | **2 new files** |
