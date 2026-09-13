# AI Harness Setup Guide

## Files Created

Your AI harness is now set up! Here's what was created:

### Phase 1: Specification Files
- `docs/specs/README.md` - How specs work
- `docs/specs/architecture.md` - System overview
- `docs/specs/backend-capabilities.md` - Backend features
- `docs/specs/frontend-capabilities.md` - Frontend features
- `docs/specs/integration-flows.md` - Key workflows

### Phase 2: Agent Prompts
- `.continue/prompts/planner.md` - Planning agent rules
- `.continue/prompts/implementer.md` - Implementation agent rules
- `.continue/prompts/reviewer.md` - Review agent rules
- `.continue/prompts/tester.md` - Testing agent rules
- `.continue/prompts/security.md` - Security agent rules

### Phase 3: Documentation
- `docs/ai-harness/README.md` - How to use the agents
- `docs/ai-harness/feedback-log.md` - Track improvements
- `.continue/config.example.json` - Example config

---

## Manual Setup Required


### IMPORTANT: API Keys Stay Local

**DO NOT** put API keys in this project's `.continue/config.example.json`!

**Your API keys should stay in your local Continue config**:
- **macOS/Linux**: `~/.continue/config.json` or `~/.continue/config.yaml`
- **Windows**: `%USERPROFILE%\.continue\config.json` or `%USERPROFILE%\.continue\config.yaml`

**This project's config** (`.continue/config.example.json`) **only contains**:
- Custom commands (slash commands for agents)
- Context providers (which files agents should read)
- System message (general instructions)

**NO API keys, NO model configurations** - those stay in your local directory!

---

### Step 1: Locate Your Continue Config

Continue.dev config is usually at:


- **macOS/Linux**: `~/.continue/config.json` or `~/.continue/config.yaml`
- **Windows**: `%USERPROFILE%\.continue\config.json` or `%USERPROFILE%\.continue\config.yaml`

**Or** use Continue's UI:
1. Open Continue sidebar

2. Click the gear icon, then "Open config.json" (or config.yaml)

### Step 2: Copy the Configuration

Open `.continue/config.example.json` (created in this repo) and copy the relevant sections into your Continue config:

#### Add Custom Commands (Agents)

Find or create a `customCommands` section in your config and add:

```json
"customCommands": [
{
"name": "plan",
"description": "Planning Agent: Analyze request and create minimal implementation plan",
"prompt": "{{{ input }}}\n\nRead and follow .continue/prompts/planner.md to create a plan for this request."
},
{
"name": "implement",
"description": "Implementer Agent: Write minimal code following the plan",
"prompt": "{{{ input }}}\n\nRead and follow .continue/prompts/implementer.md to implement this. Always check AGENTS.md for lazy senior dev rules."
},
{
"name": "review",
"description": "Reviewer Agent: Review code against AGENTS.md principles",
"prompt": "{{{ input }}}\n\nRead and follow .continue/prompts/reviewer.md to review the implementation."
},
{
"name": "test",
"description": "Tester Agent: Generate minimal tests for non-trivial code",
"prompt": "{{{ input }}}\n\nRead and follow .continue/prompts/tester.md to create minimal tests."
},
{
"name": "security",
"description": "Security Agent: Scan for vulnerabilities (manual trigger only)",
"prompt": "{{{ input }}}\n\nRead and follow .continue/prompts/security.md to perform a security review."
}
]
```

#### Add Context Providers (Optional but Recommended)

This helps agents access relevant files:

```json
"contextProviders": [
{
"name": "file",
"params": {}
},
{
"name": "folder",
"params": {}
},
{
"name": "codebase",
"params": {}
}
]
```

#### Update System Message (Optional)

Change your global `systemMessage` or add to project-specific config:

```json
"systemMessage": "You are a lazy senior developer working on the KindleForPDF project. Always read AGENTS.md and relevant docs/specs/ before responding."
```

### Step 3: Reload Continue

After editing config:
1. Save the config file
2. Reload Continue extension (or restart VS Code)
3. Verify slash commands appear (type `/` in Continue chat)

---

## Test the Setup

### Test 1: Specs Are Readable

In Continue chat:
```
What capabilities does the backend have?
```

Expected: Agent should reference `docs/specs/backend-capabilities.md`

### Test 2: Planner Agent Works

```
/plan Add a health check endpoint that returns system status
```

Expected: Agent should:
- Read `AGENTS.md` (lazy rules)
- Read `docs/specs/` (understand current system)
- Suggest minimal approach
- Question if it's needed (YAGNI)
- **Save plan to** `.continue/plans/plan-001-health-endpoint.md`

**Note**: Plans are saved to `.continue/plans/` to avoid context pollution. This directory is in `.gitignore`.

### Test 3: Implementer Agent Works

```
/implement Create a simple GET /status endpoint that returns {"status": "ok"}
```

Expected: Agent should:
- Write minimal code
- Follow existing patterns (check `apps/api/src/interfaces/api/main.py`)
- Not over-engineer

---

## Directory Structure (Final)

```
KindleForPDF/
├── .continue/
│ ├── prompts/
│ │ ├── planner.md
│ │ ├── implementer.md
│ │ ├── reviewer.md
│ │ ├── tester.md
│ │ └── security.md
│ └── config.example.json # Copy this to your Continue config
│
├── docs/
│ ├── ai-harness/
│ │ ├── README.md # How to use agents
│ │ ├── feedback-log.md # Track improvements
│ │ └── SETUP.md # This file
│ │
│ └── specs/
│ ├── README.md
│ ├── architecture.md
│ ├── backend-capabilities.md
│ ├── frontend-capabilities.md
│ └── integration-flows.md
│
├── AGENTS.md # Core lazy senior dev rules
└── [your existing project files]
```

---

## Next Steps

### 1. Review the Specs
Check `docs/specs/*.md` to ensure they accurately reflect your current system. Edit as needed.

### 2. Try the Workflow
Pick a small task and run through the full cycle:
```
/plan [your task]
Review plan
/implement
Review code
/review
Approve or iterate
```

### 3. Start Logging Feedback
When an agent does something unexpected, log it in `docs/ai-harness/feedback-log.md` and update the relevant prompt file.

### 4. Iterate
The system gets better as you:
- Refine agent prompts
- Update specs when architecture changes
- Add project-specific rules to `AGENTS.md`

---

## Reference

See the Reference Files table in `docs/ai-harness/README.md` for the full file map.

---

## Troubleshooting

### Slash commands don't appear
- Check config is saved
- Reload Continue extension
- Verify JSON syntax (use a JSON validator)

### Agent doesn't read specs
- Make sure `contextProviders` includes `file` and `codebase`
- Explicitly mention spec files in your prompt: "Read docs/specs/backend-capabilities.md first"

### Agent ignores AGENTS.md rules
- Update the custom command prompt to explicitly reference it
- Add reminder in `systemMessage`
- Log issue in `feedback-log.md` and refine agent prompt

---

## You're All Set!

The AI harness is ready to use. Start with simple tasks, iterate on agent behavior, and enjoy lazy senior dev productivity.

Questions? Check `docs/ai-harness/README.md` for detailed usage patterns.
