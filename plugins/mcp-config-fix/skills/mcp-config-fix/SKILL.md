---
name: mcp-config-fix
description: Fix and manage Claude Desktop MCP server configuration on Windows. Use this skill whenever MCP tools don't show up in Claude Desktop, when mcpServers config gets deleted or overwritten on restart, when adding new MCP servers to Claude Desktop config, or when troubleshooting any MCP connection issues on Windows. Also triggers for "Claude Desktop config", "MCP not working", "tools not showing", "config keeps getting deleted", "add MCP server", or any mention of claude_desktop_config.json problems.
---

# MCP Config Fix — Claude Desktop Windows

<!-- SECURITY: CRITICAL-3.1 -->
## ⚠️ SECURITY NOTICE
This skill modifies your Claude Desktop configuration file.
- NEVER run commands from this skill without reading them first
- NEVER paste API keys directly — use environment variables instead
- ALWAYS back up your config before running any fix
- This skill will NEVER ask you to download or run external scripts

## The Problem

On Windows, Claude Desktop silently fails to load MCP servers when the config file has a UTF-8 BOM (Byte Order Mark). PowerShell's `Set-Content -Encoding UTF8` adds a 3-byte BOM (`EF BB BF`) to the beginning of files. Claude Desktop cannot parse JSON with BOM → ignores `mcpServers` → overwrites the file with only `preferences`.

## Root Cause

```
❌ PowerShell Set-Content -Encoding UTF8  → adds BOM → Claude Desktop ignores mcpServers
❌ Notepad "Save as UTF-8"               → adds BOM → same problem
✅ [System.IO.File]::WriteAllText()       → no BOM  → works perfectly
```

## The Fix — ALWAYS Use This Method

### Step 1: Kill Claude Desktop FIRST

**IMPORTANT**: Never kill processes named "Claude" generically — this will kill Claude Code too!

```powershell
# Safe way — only kills Claude Desktop, NOT Claude Code
Get-Process | Where-Object {$_.ProcessName -eq "Claude Desktop" -or ($_.MainWindowTitle -like "*Claude*" -and $_.ProcessName -ne "claude")} | Stop-Process -Force -ErrorAction SilentlyContinue
```

**Or better**: Ask the user to manually quit Claude Desktop from the system tray (right-click → Quit). This is the safest approach.

<!-- SECURITY: CRITICAL-3.1 — Backup before modification -->
### Step 2: Back Up Existing Config

**ALWAYS** create a backup before modifying anything:

```powershell
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $configPath) {
    $backupPath = "$env:APPDATA\Claude\claude_desktop_config.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
    Copy-Item $configPath $backupPath
    "Backup saved to: $backupPath"
} else {
    "No existing config found — skipping backup"
}
```

### Step 3: Read Existing Config

```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue
```

Note any existing `mcpServers` and `preferences` to preserve them.

### Step 4: Write Config WITHOUT BOM

```powershell
$config = @'
{
  "mcpServers": {
    "server-name": {
      "command": "FULL_PATH_TO_PYTHON_OR_NODE",
      "args": ["FULL_PATH_TO_SERVER_SCRIPT"],
      "env": {
        "API_KEY": "${YOUR_API_KEY_ENV_VAR}"
      }
    }
  },
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "sidebarMode": "chat"
  }
}
'@

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("$env:APPDATA\Claude\claude_desktop_config.json", $config, $utf8NoBom)
```

### Step 5: Verify No BOM

```powershell
$bytes = [System.IO.File]::ReadAllBytes("$env:APPDATA\Claude\claude_desktop_config.json")
if ($bytes[0] -eq 0xEF) { "❌ BAD - HAS BOM" } else { "✅ GOOD - No BOM" }
```

<!-- SECURITY: CRITICAL-3.1 — JSON integrity validation after every config edit -->
### Step 6: Verify Valid JSON

```powershell
try {
    Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json | Out-Null
    "✅ Valid JSON"
} catch {
    "❌ Invalid JSON: $_"
}
```

### Step 7: Show Final Config

```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

### Step 8: Restart Claude Desktop

Tell the user to reopen Claude Desktop and check for the 🔨 hammer icon.

---

## Critical Rules

1. **NEVER** use `Set-Content -Encoding UTF8` — always use `[System.IO.File]::WriteAllText()` with `UTF8Encoding($false)`
2. **NEVER** use just `"python"` in the command — always use the **FULL path** to `python.exe`
3. **ALWAYS** merge new servers with existing ones — don't overwrite
4. **ALWAYS** preserve the `preferences` section
5. **ALWAYS** verify no BOM after writing
6. **ALWAYS** use double backslashes `\` in JSON paths
7. **NEVER** kill Claude processes generically — ask user to quit manually

<!-- SECURITY: CRITICAL-3.1 — PowerShell command safety boundary -->
## ⚠️ Command Safety Rules

This skill's PowerShell commands are **strictly limited** to:
- **Reading** `claude_desktop_config.json` (via `Get-Content`, `[System.IO.File]::ReadAllBytes/ReadAllText`)
- **Writing** `claude_desktop_config.json` (via `[System.IO.File]::WriteAllText`)
- **Copying** `claude_desktop_config.json` for backups (via `Copy-Item`)
- **Listing** directories to locate config paths (via `Get-ChildItem`)
- **Locating** Python installations (via `where.exe python`)
- **Stopping** only Claude Desktop processes (via filtered `Stop-Process`)
- **Parsing** JSON for validation (via `ConvertFrom-Json`)

**NEVER** use commands that:
- Download files from the internet (`Invoke-WebRequest`, `wget`, `curl`, `Net.WebClient`)
- Execute remote scripts (`Invoke-Expression`, `iex`, `Start-Process` with URLs)
- Read files outside `%APPDATA%\Claude\` (no reading `.env`, credentials, SSH keys)
- Delete files other than Claude config backups (`Remove-Item` on non-config paths)
- Modify system settings, registry, or environment variables

## Finding the Correct Python Path

```powershell
# Find all Python installations
where.exe python
python --version

# Common Windows paths:
# Windows Store: C:\Users\USERNAME\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe
# Standard:      C:\Users\USERNAME\AppData\Local\Programs\Python\Python313\python.exe
# System:        C:\Python313\python.exe
```

Use the FULL path from `where.exe python` in the config.

## MSIX Virtualization Bug (Advanced)

Some Windows installations have TWO config files due to MSIX packaging:

```powershell
# Check for virtualized path
Get-ChildItem "$env:LOCALAPPDATA\Packages" -Filter "Claude*" -Directory -ErrorAction SilentlyContinue
Get-ChildItem "$env:LOCALAPPDATA\Packages" -Filter "Anthropic*" -Directory -ErrorAction SilentlyContinue
```

If found, write config to BOTH locations:

```powershell
# Real path
$realPath = "$env:APPDATA\Claude\claude_desktop_config.json"

# Virtualized path (find the actual folder name first)
$virtualBase = Get-ChildItem "$env:LOCALAPPDATA\Packages" -Filter "Claude*" -Directory | Select-Object -First 1
$virtualPath = Join-Path $virtualBase.FullName "LocalCache\Roaming\Claude\claude_desktop_config.json"

# Write to both
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($realPath, $config, $utf8NoBom)
if (Test-Path $virtualPath) {
    [System.IO.File]::WriteAllText($virtualPath, $config, $utf8NoBom)
}
```

## Example: Adding Multiple MCP Servers

```powershell
$config = @'
{
  "mcpServers": {
    "video-analyzer": {
      "command": "C:\\Path\\To\\python.exe",
      "args": ["C:\\Path\\To\\server.py"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    },
    "nanobanana": {
      "command": "C:\\Path\\To\\python.exe",
      "args": ["-m", "nanobanana_mcp_server.server"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    },
    "veo": {
      "command": "C:\\Path\\To\\python.exe",
      "args": ["C:\\Path\\To\\veo_mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "VIDEO_OUTPUT_DIR": "C:\\Path\\To\\videos"
      }
    }
  },
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "sidebarMode": "chat"
  }
}
'@

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("$env:APPDATA\Claude\claude_desktop_config.json", $config, $utf8NoBom)

# Verify
$bytes = [System.IO.File]::ReadAllBytes("$env:APPDATA\Claude\claude_desktop_config.json")
if ($bytes[0] -eq 0xEF) { "❌ BAD" } else { "✅ No BOM" }
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

<!-- SECURITY: HIGH-3.3 — MCP server entry validation guidance -->
## ⚠️ MCP Server Entry Validation

Before adding ANY mcpServers entry, verify each field against this checklist:

### Validation Checklist

For **every** server entry in `mcpServers`, confirm:

- [ ] **`command`** — Points to a known-safe executable at a full, absolute path:
  - Allowed: `python.exe`, `node.exe`, `npx`, `uvx`, `docker` at their standard install locations
  - Reject: relative paths, URLs, `cmd.exe /c`, `powershell -Command`, or unknown executables
- [ ] **`args`** — Contains only file paths or module names:
  - Allowed: paths to `.py`/`.js` server scripts, `-m module_name` arguments
  - Reject: shell operators (`|`, `>`, `&&`), URLs, encoded payloads, or `-c "code"` patterns
- [ ] **`env`** — Contains only environment variable assignments:
  - Allowed: `"VAR_NAME": "${ENV_VAR_REFERENCE}"` or actual env var names
  - Reject: hardcoded API keys, tokens, or passwords (use `${ENV_VAR}` placeholders)
- [ ] **Server name** — Is descriptive and matches the server's actual purpose
- [ ] **Script path** — The referenced server script actually exists at the specified path

### Known-Safe Command Paths (Windows)

```
C:\Users\<USER>\AppData\Local\Programs\Python\Python3*\python.exe
C:\Users\<USER>\AppData\Local\Microsoft\WindowsApps\python*.exe
C:\Program Files\nodejs\node.exe
C:\Users\<USER>\AppData\Roaming\npm\npx.cmd
```

### Red Flags — STOP and Investigate

If any mcpServers entry contains:
- A `command` pointing to `cmd.exe`, `powershell.exe`, or `bash.exe`
- Arguments that include `Invoke-WebRequest`, `curl`, `wget`, or `DownloadString`
- Environment variables containing what looks like an actual key (not a `${reference}`)
- Paths to temporary directories or downloads folder

**DO NOT add the entry.** Ask the user to verify the server source first.

<!-- SECURITY: HIGH-3.4 — API key exposure prevention in config examples -->
## ⚠️ API Key Safety

**NEVER** include real API keys in the config. Always use environment variable references:

```json
"env": {
    "GEMINI_API_KEY": "${GEMINI_API_KEY}",
    "OPENAI_API_KEY": "${OPENAI_API_KEY}"
}
```

Set the actual values in your system environment variables:

```powershell
# Set environment variable (run once in an admin PowerShell)
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your-actual-key", "User")
```

Then restart Claude Desktop to pick up the new environment variables.

<!-- SECURITY: MEDIUM-3.5 — Config corruption protection -->
## Config Merge Safety

When adding new MCP servers, **NEVER** overwrite the entire config. Always:

1. **Read** the existing config first (Step 3)
2. **Parse** it as JSON to extract current `mcpServers` and `preferences`
3. **Merge** new server entries into the existing `mcpServers` object
4. **Preserve** all existing entries and `preferences`
5. **Write** the merged result back

### Config Health Check

After any modification, run this validation:

```powershell
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$content = Get-Content $configPath -Raw

# 1. Valid JSON?
try {
    $json = $content | ConvertFrom-Json
    "1. Valid JSON"
} catch {
    "FAIL: Invalid JSON — restore from backup!"
    return
}

# 2. Has mcpServers?
if ($json.mcpServers) {
    $serverCount = ($json.mcpServers | Get-Member -MemberType NoteProperty).Count
    "2. mcpServers: $serverCount server(s) configured"
} else {
    "WARNING: No mcpServers section found"
}

# 3. Has preferences?
if ($json.preferences) {
    "3. preferences section present"
} else {
    "WARNING: No preferences section — Claude Desktop may add defaults"
}

# 4. No BOM?
$bytes = [System.IO.File]::ReadAllBytes($configPath)
if ($bytes[0] -eq 0xEF) { "FAIL: BOM detected!" } else { "4. No BOM" }

# 5. File size reasonable?
$size = (Get-Item $configPath).Length
if ($size -gt 0 -and $size -lt 100000) { "5. File size OK ($size bytes)" } else { "WARNING: Unusual file size ($size bytes)" }
```

<!-- SECURITY: MEDIUM-3.6 — Safe process termination -->
## ⚠️ Safe Process Termination

### Preferred Method: Manual Closure

The safest way to stop Claude Desktop is to **ask the user to quit manually**:

> Right-click the Claude icon in the system tray (bottom-right) → click **Quit**.

### Automated Method (Use With Caution)

If automated termination is needed, **only target Claude Desktop processes**:

```powershell
# SAFE: Only targets Claude Desktop by exact process name
Get-Process | Where-Object {$_.ProcessName -eq "Claude Desktop" -or ($_.MainWindowTitle -like "*Claude*" -and $_.ProcessName -ne "claude")} | Stop-Process -Force -ErrorAction SilentlyContinue
```

**NEVER use any of these** — they will kill Claude Code:
```powershell
# DANGEROUS — kills ALL Claude processes including Claude Code
Stop-Process -Name "Claude" -Force          # ← NEVER
Stop-Process -Name "claude" -Force          # ← NEVER
Get-Process "claude*" | Stop-Process        # ← NEVER
taskkill /IM "claude.exe" /F               # ← NEVER
```

If unsure whether the automated command is safe, **always fall back to manual closure**.

## Troubleshooting Checklist

| Problem | Solution |
|---------|----------|
| Tools don't show after restart | Check for BOM → rewrite without BOM |
| Config gets deleted on restart | You didn't fully quit Claude Desktop → right-click system tray → Quit |
| Server connected but no tools | Check Python path is FULL and correct |
| "Failed to spawn process" | Python path wrong or dependencies not installed |
| Config has BOM | Rewrite using `[System.IO.File]::WriteAllText()` |
| Two config files exist | MSIX bug → write to both paths |
| Claude Code killed itself | Used `Stop-Process -Name "Claude"` → never do this |
