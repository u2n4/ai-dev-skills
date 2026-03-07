# Contributing to AI Dev Skills

Thank you for your interest in contributing to AI Dev Skills! This guide will help you get started.

## How to Contribute

### Reporting Issues

- Use the GitHub Issues tab to report bugs or request features
- Include clear steps to reproduce any bugs
- Provide your OS version and Claude Code version

### Adding a New Skill

1. Fork this repository
2. Create a new branch: `git checkout -b feat/my-new-skill`
3. Create your skill directory under `plugins/`:

```
plugins/
  my-skill/
    .claude-plugin/
      plugin.json
    skills/
      my-skill/
        SKILL.md
```

4. Write your `SKILL.md` following the existing skill format:
   - Include YAML frontmatter with `name` and `description`
   - Provide clear trigger conditions
   - Include step-by-step instructions
   - Add examples and troubleshooting sections

5. Add your plugin entry to `.claude-plugin/marketplace.json`
6. Submit a Pull Request with a clear description

### Plugin Manifest Format

Your `plugin.json` should follow this structure:

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "Brief description of what the skill does",
  "author": {
    "name": "your-github-username",
    "email": "your-email@users.noreply.github.com"
  }
}
```

### Improving Existing Skills

1. Fork and create a branch
2. Make your changes
3. Test the skill by installing it locally
4. Submit a Pull Request explaining the improvement

## Code of Conduct

- Be respectful and constructive
- Focus on the technical merits of contributions
- Help others learn and grow

## Security

- NEVER include API keys, tokens, or personal paths in skills
- Use generic placeholder paths (e.g., `C:\Path\To\...`)
- Report security issues privately via GitHub Security Advisories

## Style Guide

- Use clear, concise language in skill instructions
- Include both the problem description and the solution
- Add troubleshooting tables for common issues
- Use code blocks with language identifiers for syntax highlighting

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
