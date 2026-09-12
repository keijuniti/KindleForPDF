# AI Harness Usage Guide

This guide explains how to use the 5 AI agents (Planner, Implementer, Reviewer, Tester, Security) and how to improve them with feedback loops.

---

## 🤖 The 5 Agents

### 1. Planner Agent
**When to use**: Starting a new feature or fixing a bug  
**What it does**: Creates a minimal implementation plan  
**Follows**: YAGNI, challenges complexity, suggests shortest approach

### 2. Implementer Agent
**When to use**: After approving a plan  
**What it does**: Writes the minimal code to solve the problem  
**Follows**: Lazy senior dev rules, reuses patterns, shortest diff wins

### 3. Reviewer Agent
**When to use**: After implementation  
**What it does**: Checks code against AGENTS.md principles  
**Follows**: Enforces no over-engineering, checks correctness

### 4. Tester Agent
**When to use**: When ready to add tests (non-trivial code only)  
**What it does**: Generates minimal test coverage  
**Follows**: No heavy frameworks, test what matters

### 5. Security Agent
**When to use**: Manual trigger only (before sensitive changes)  
**What it does**: Scans for vulnerabilities  
**Follows**: Focus on trust boundaries, minimal fixes

---

## 📋 How to Invoke Each Agent

### Method 1: Slash Commands (Recommended)

In Continue.dev chat:

```
/plan Add pagination to GET /windows endpoint
```

Available commands:
- `/plan` - Planning Agent
- `/implement` - Implementer Agent
- `/review` - Reviewer Agent
- `/test` - Tester Agent
- `/security` - Security Agent

### Method 2: Natural Language (Also Works)

Just describe what you want, and Continue will pick the right agent based on context:

**Planning phase:**
```
"Plan how to add a new endpoint for listing captured PDFs"
"I need to fix bug #42 where window detection fails - make a plan"
```

**Implementation phase:**
```
"Implement the plan above"
"Follow the planner's approach and write the code"
```

**Review phase:**
```
"Review the implementation against AGENTS.md"
"Check if this is over-engineered"
```

**Testing phase:**
```
"Generate minimal tests for the pagination endpoint"
"Create a test for the capture use case edge cases"
```

**Security phase:**
```
"Security check the file upload handler"
"Scan for vulnerabilities in the authentication middleware"
```

---

## 🔄 Typical Workflow

### Example: Adding a New Feature

```
You:  /plan Add a GET /pdfs endpoint to list all generated PDFs in the outputs folder

Agent (Planner):
- Reads docs/specs/
- Checks existing code
- Creates minimal plan
- Questions if this is needed (YAGNI check)
- Outputs: files to modify, approach, edge cases

You: [Review plan] → Approve or ask for changes

You:  /implement Use the plan above

Agent (Implementer):
- Follows planner's approach
- Writes minimal code
- Reuses existing patterns
- Updates specs if needed
- Shows diff

You: [Review code] → Looks good

You:  /review Check the implementation

Agent (Reviewer):
- Checks against AGENTS.md rules
- Verifies no over-engineering
- Checks edge cases
- Approves or requests changes

You: [If approved] → Merge/commit

You (later):  /test Generate tests for GET /pdfs

Agent (Tester):
- Creates minimal test
- Happy path + 1-2 edge cases
- Runnable standalone

You (optional):  /security Check the /pdfs endpoint

Agent (Security):
- Scans for path traversal
- Checks input validation
- Approves or suggests fixes
```

---

## 🔁 Feedback Loop: Improving Agents

### When an Agent Gives Suboptimal Output

**Example**: Implementer over-engineers a solution

#### Step 1: Document in `feedback-log.md`

```markdown
## 2025-01-20: Implementer Over-Engineering

**Task**: Add simple `page_count` field to API response  
**Issue**: Created new service layer, added Pydantic model, created 3 files  
**Expected**: Just add one field to existing `CaptureConfig` model  

**Root Cause**: Agent didn't grep for existing patterns first
```

#### Step 2: Update Agent Prompt

Edit `.continue/prompts/implementer.md`:

```markdown
## Before Writing ANY Code
**Climb the ladder** (stop at first rung that holds):
1. Can this be added to an existing model/class? (ONE FIELD = NO NEW FILE) ← ADD THIS
2. Does it already exist in this codebase?
...
```

#### Step 3: Re-Run the Task

```
/implement Add page_count field to CaptureConfig (try again with updated rules)
```

#### Step 4: Log the Result

```markdown
**Fix Applied**: Added "one field = no new file" rule to implementer.md  
**Re-Run Result**: ✅ Now just modifies existing Pydantic model  
**Status**: Keep this rule, works well
```

### Continuous Improvement

The more you use the agents and log feedback, the better they become at following your project's patterns.

**Key principle**: Agents learn from iteration, not from reading minds.

---

## 💡 Tips for Best Results

### 1. Always Start with Planning
Don't skip the planner. Even for "simple" tasks, planning catches YAGNI violations.

### 2. Be Specific About Scope
```
❌ "Add authentication"  (too vague)
✅ "Add basic API key authentication to POST /capture endpoint only"
```

### 3. Reference Existing Code
```
✅ "Use the same pattern as CaptureConfig for the new model"
✅ "Follow the use case structure in get_windows_usecase.py"
```

### 4. Challenge Complexity
If an agent suggests something complex, push back:
```
"Do we actually need a new service class, or can this be a one-liner in the existing use case?"
```

### 5. Use Security Agent Sparingly
Only for:
- Before deploying to production
- When touching auth/permissions
- When handling user uploads/inputs
- When you're unsure about a security implication

**AIKIDO** handles continuous scanning; this agent is for manual spot-checks.

---

## 📊 When to Use Which Agent

| Scenario | Agent | Command |
|----------|-------|---------|
| New feature idea | Planner | `/plan Add X feature` |
| Bug needs fixing | Planner | `/plan Fix bug where Y happens` |
| Ready to code | Implementer | `/implement` (after plan approved) |
| Code written, need check | Reviewer | `/review` |
| Need test coverage | Tester | `/test Generate tests for X` |
| Security-sensitive change | Security | `/security Check X for vulnerabilities` |
| Unsure if needed | Planner | `/plan` (let YAGNI check run) |

---

## 🚨 Common Mistakes to Avoid

### ❌ Skipping the Planner
"It's a simple change, I'll just implement it."  
→ Result: Over-engineered solution, missed existing code reuse.

**Fix**: Always `/plan` first, even for "obvious" changes.

### ❌ Not Updating Specs After Architecture Changes
Implementer adds new capability, forgets to update `docs/specs/backend-capabilities.md`.  
→ Result: Next agent doesn't know the capability exists, re-implements it.

**Fix**: Reviewer should catch this. Update specs when architecture changes.

### ❌ Over-Relying on Security Agent
Running `/security` on every trivial change.  
→ Result: Wasted time, security fatigue.

**Fix**: Use it only for trust boundaries (API inputs, file handling, auth).

### ❌ Not Logging Feedback
Agent gives bad output, you manually fix it, move on.  
→ Result: Agent makes same mistake next time.

**Fix**: Log in `feedback-log.md`, update prompt, re-run.

---

## 📚 Reference Files

| File | Purpose |
|------|---------|
| `.continue/config.json` | Agent definitions, slash commands |
| `.continue/prompts/planner.md` | Planner agent system prompt |
| `.continue/prompts/implementer.md` | Implementer agent system prompt |
| `.continue/prompts/reviewer.md` | Reviewer agent system prompt |
| `.continue/prompts/tester.md` | Tester agent system prompt |
| `.continue/prompts/security.md` | Security agent system prompt |
| `docs/ai-harness/feedback-log.md` | Your iteration notes |
| `docs/specs/` | System specs (agents read these for context) |
| `AGENTS.md` | Core lazy senior dev rules (all agents follow this) |

---

## 🎓 Learning Curve

**Week 1**: Feel awkward using agents, manually fix outputs  
**Week 2**: Start logging feedback, update prompts  
**Week 3**: Agents match your style, minimal manual fixes  
**Week 4+**: Agents feel like a well-trained junior dev

**Key**: Iteration. The system gets better as you refine it.

---

## 🦥 Remember

You're building a **harness**, not a perfect AI system.

- Agents will make mistakes → Log feedback, improve prompts
- Specs will drift → Update them when architecture changes
- Rules will evolve → Add to `AGENTS.md` as you find patterns

**Lazy senior dev = efficient iteration, not perfection on first try.**

---

Need help? Check `feedback-log.md` for common issues and fixes.
