---
name: mcp-config-fix
description: Fix and manage Claude Desktop MCP server configuration on Windows. Use this skill whenever MCP tools don't show up in Claude Desktop, when mcpServers config gets deleted or overwritten on restart, when adding new MCP servers to Claude Desktop config, or when troubleshooting any MCP connection issues on Windows. Also triggers for "Claude Desktop config", "MCP not working", "tools not showing", "config keeps getting deleted", "add MCP server", or any mention of claude_desktop_config.json problems.
---

# MCP Config Fix — Claude Desktop Windows

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

### Step 2: Read Existing Config

```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue
```

Note any existing `mcpServers` and `preferences` to preserve them.

### Step 3: Write Config WITHOUT BOM

```powershell
$config = @'
{
  "mcpServers": {
    "server-name": {
      "command": "FULL_PATH_TO_PYTHON_OR_NODE",
      "args": ["FULL_PATH_TO_SERVER_SCRIPT"],
      "env": {
        "API_KEY": "key_here"
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

### Step 4: Verify No BOM

```powershell
$bytes = [System.IO.File]::ReadAllBytes("$env:APPDATA\Claude\claude_desktop_config.json")
if ($bytes[0] -eq 0xEF) { "❌ BAD - HAS BOM" } else { "✅ GOOD - No BOM" }
```

### Step 5: Verify Valid JSON

```powershell
try {
    Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json | Out-Null
    "✅ Valid JSON"
} catch {
    "❌ Invalid JSON: $_"
}
```

### Step 6: Show Final Config

```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

### Step 7: Restart Claude Desktop

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
        "GEMINI_API_KEY": "key1"
      }
    },
    "nanobanana": {
      "command": "C:\\Path\\To\\python.exe",
      "args": ["-m", "nanobanana_mcp_server.server"],
      "env": {
        "GEMINI_API_KEY": "key2"
      }
    },
    "veo": {
      "command": "C:\\Path\\To\\python.exe",
      "args": ["C:\\Path\\To\\veo_mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "key1",
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
