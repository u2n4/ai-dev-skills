---
name: prompt-generator
description: Generate professional, structured prompts for Claude Code with Agent Teams patterns, multi-phase workflows, and skill-aware orchestration. Use when users need to create complex Claude Code prompts, set up agent teams, design multi-step workflows, or craft effective instructions for Claude Code projects.
---

# Claude Code Prompt Generator

## When to Use This Skill

Activate when the user asks to:
- Create a prompt for Claude Code
- Set up an Agent Team for a project
- Design a multi-phase workflow
- Generate a professional Claude Code instruction set
- Build a CLAUDE.md for a project
- Create task-specific prompts with proper structure

## Prompt Architecture

### The 5-Layer Prompt Structure

Every professional Claude Code prompt should include these layers:

#### Layer 1: Context & Role
Define WHO Claude is and WHAT the project context is.

```markdown
You are an expert [role] with deep knowledge of [domains].

<context>
[Project description, current state, relevant background]
</context>
```

#### Layer 2: Task Definition
Define WHAT needs to be done with clear phases.

```markdown
<task>
## Phase 1: [Research/Audit]
[Steps with specific actions]

## Phase 2: [Implementation]
[Steps with expected outputs]

## Phase 3: [Verification]
[Testing and validation steps]
</task>
```

#### Layer 3: Requirements & Constraints
Define HOW the work should be done.

```markdown
<requirements>
- [Quality standards]
- [Technical constraints]
- [Output format]
</requirements>

<constraints>
- NEVER [dangerous action]
- ALWAYS [safety requirement]
- [Boundary conditions]
</constraints>
```

#### Layer 4: Agent Team Pattern
For complex tasks, define specialized agent roles.

```markdown
## Agent Team

### Research Agent
- Role: Gather information and audit current state
- Tools: WebSearch, Grep, Glob, Read
- Output: Research report

### Implementation Agent
- Role: Execute the plan
- Tools: Write, Edit, Bash
- Output: Working code

### Review Agent
- Role: Verify quality and security
- Tools: Read, Grep, Bash
- Output: Review report with issues
```

#### Layer 5: Output Controls
Define verification checkpoints and stop conditions.

```markdown
## Verification Checkpoint

Present to me:
1. [Deliverable 1]
2. [Deliverable 2]
3. [Status summary]

**STOP HERE. Wait for my confirmation before proceeding.**
```

## Prompt Templates

### Template 1: Feature Implementation

```markdown
You are a senior [language] developer.

<context>
Project: [name]
Stack: [technologies]
Current state: [description]
</context>

<task>
## Phase 1: Analysis
1. Read and understand [files]
2. Identify integration points
3. Map dependencies

## Phase 2: Implementation
1. Create [component/feature]
2. Write tests (80%+ coverage)
3. Integrate with existing code

## Phase 3: Verification
1. Run all tests
2. Check for regressions
3. Verify edge cases
</task>

<requirements>
- Follow existing code patterns
- Maintain backwards compatibility
- Include error handling
- Add JSDoc/docstrings
</requirements>
```

### Template 2: Multi-Repo Publishing

```markdown
You are an expert open-source developer and GitHub SEO specialist.

<context>
[Project descriptions and file locations]
</context>

<task>
## Phase 1: Locate and Audit
[File discovery and security scanning]

## Phase 2: Build Professional Repos
[README, LICENSE, documentation]

## Phase 3: Create Repos
[Git operations, GitHub API]

## Phase 4: Verification
[Security audit, structure check]
</task>

<requirements>
- ALL content in English
- MIT License
- PRIVATE repos initially
- Zero tolerance for leaked secrets
</requirements>

<constraints>
- NEVER push API keys
- NEVER make public without confirmation
</constraints>
```

### Template 3: Bug Fix with Agent Team

```markdown
You are a debugging specialist.

<context>
Bug: [description]
Error: [stack trace]
Affected files: [list]
</context>

<task>
Use the following agent team:

### Diagnostic Agent
1. Read error logs and stack traces
2. Identify root cause
3. Map affected code paths

### Fix Agent
1. Implement minimal fix
2. Write regression test
3. Verify no side effects

### Review Agent
1. Check fix completeness
2. Verify test coverage
3. Scan for similar issues elsewhere
</task>
```

### Template 4: API Development

```markdown
You are a backend API architect.

<context>
API: [name]
Framework: [Express/FastAPI/etc]
Database: [PostgreSQL/MongoDB/etc]
Auth: [JWT/OAuth/etc]
</context>

<task>
## Phase 1: Schema Design
1. Define data models
2. Create migration scripts
3. Set up database connection

## Phase 2: API Endpoints
For each endpoint:
1. Define route and method
2. Implement handler
3. Add validation (Zod/Pydantic)
4. Write integration test

## Phase 3: Security
1. Implement authentication
2. Add rate limiting
3. Input sanitization
4. Error handling (no leaked internals)
</task>

<requirements>
- RESTful conventions
- Consistent error response format: { success, data, error }
- Pagination for list endpoints
- Request validation at boundary
</requirements>
```

## Agent Team Patterns

### Pattern 1: Research → Plan → Execute
Best for: New features, greenfield projects
```
Research Agent → Planning Agent → Implementation Agent → Review Agent
```

### Pattern 2: Parallel Specialists
Best for: Complex tasks with independent concerns
```
Security Agent ─┐
Performance Agent ─┤→ Synthesis Agent
Quality Agent ──┘
```

### Pattern 3: Iterative Refinement
Best for: Creative work, UI/UX, prompt optimization
```
Draft Agent → Critique Agent → Refine Agent → (repeat until quality threshold)
```

### Pattern 4: Pipeline
Best for: Data processing, CI/CD, multi-stage builds
```
Stage 1 Agent → Stage 2 Agent → Stage 3 Agent → Verification Agent
```

## Best Practices

### DO
- Use XML tags for clear section boundaries (<context>, <task>, <requirements>)
- Include explicit phase checkpoints
- Define success criteria before starting
- Specify output format expectations
- Use numbered steps for sequential tasks
- Include "STOP and wait" checkpoints for risky operations

### DON'T
- Don't leave tasks open-ended without completion criteria
- Don't mix multiple unrelated tasks in one prompt
- Don't forget constraints for destructive operations
- Don't skip the verification phase
- Don't use vague instructions ("make it better")

## Quality Checklist

Before sending a Claude Code prompt:
- [ ] Context is clear and complete
- [ ] Task phases are logically ordered
- [ ] Requirements are specific and measurable
- [ ] Constraints prevent destructive actions
- [ ] Verification checkpoint is defined
- [ ] Agent team roles don't overlap (if using teams)
- [ ] Output format is specified
