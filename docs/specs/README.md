# Specification Files

## Purpose

These specs provide **high-level architectural context** for AI agents (and humans) working on this project.

**NOT detailed API documentation** — those live in dedicated API doc tools or inline code comments.

## What Goes Here

### ✅ Good for specs/
- System architecture overview
- What capabilities exist (broadly)
- Key integration flows (how pieces connect)
- Tech stack and conventions
- Design patterns in use

### ❌ Don't put here
- Detailed endpoint lists (maintain those in API docs)
- Every single component/function
- Implementation details better suited for code comments

## Update Rules

**When to update:**
- After implementing a new major feature/capability
- When architecture changes (new layer, service, integration)
- When tech stack changes (new framework, major dependency)

**Who updates:**
- AI Implementer agent (during feature development)
- Developers (when agents miss something)

**Keep it:**
- High-level (forest, not trees)
- Accurate (better to delete outdated info than leave it wrong)
- Concise (one paragraph > five bullet points)

## Structure

- `architecture.md` - System design overview
- `backend-capabilities.md` - What the backend can do
- `frontend-capabilities.md` - What the frontend provides
- `integration-flows.md` - How major workflows operate
