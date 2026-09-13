# AI Harness Feedback Log

This file tracks iterations on agent behavior. When an agent gives suboptimal output, document it here, update the prompt, re-run, and log the result.

---

## How to Use This Log

### Format:
```markdown
## YYYY-MM-DD: [Agent Name] [Issue Type]

**Task**: [What you asked the agent to do]
**Issue**: [What went wrong]
**Expected**: [What you wanted instead]
**Root Cause**: [Why the agent did this]

**Fix Applied**: [What you changed in .continue/prompts/[agent].md] 
**Re-Run Result**: [Did it work? yes/no]
**Status**: [Keep this rule / Needs more refinement / Reverted]
```

---

## Log Entries

### 2025-01-20: Agent Over-Generated Documentation Files

**Task**: Fix YAML frontmatter issues and plans directory setup
**Issue**: Created `FIXED-CONFIG.md` and `CHANGES-SUMMARY.md` without asking user first. Wasted tokens/context on unnecessary documentation.
**Expected**: Only fix the actual code/config, ask before creating any documentation files
**Root Cause**: Agent didn't ask permission before creating documentation (violated lazy senior dev principle: don't create files nobody asked for)

**Fix Applied**: Rule for ALL agents - **Always ask before creating documentation files**. Exception: Plan files in `.continue/plans/` during `/plan` phase.
**Re-Run Result**: Files deleted, rule established
**Status**: Keep this rule - NO documentation without asking first

---

## Common Patterns Observed

(Fill this in as you notice trends)

### Pattern: Over-Engineering Simple Tasks
**Frequency**: [How often this happens]
**Fix**: [What prompt changes helped]
**Status**: [Resolved / Ongoing]

### Pattern: Not Reading Existing Code
**Frequency**:
**Fix**:
**Status**:

---

## Prompt Refinement History

Track major changes to agent prompts:

| Date | Agent | Change | Reason |
|------|-------|--------|--------|
| 2025-01-XX | Implementer | Added "grep first" rule | Was duplicating existing utils |
| [Your entries here] | | | |

---

## Lessons Learned

(Summarize key insights as you iterate)

1. **Always run Planner first**: Skipping planning leads to over-engineering.
2. **Specs need updates**: After big features, update docs/specs/ or next agent won't know about them.
3. [Your lessons here]

---

## Open Questions

(Things you're unsure about, need to experiment with)

- [ ] Should Implementer always update specs, or only on Reviewer's request?
- [ ] How much detail should Planner include? (Too much = over-specified, too little = vague)
- [ ] [Your questions here]

---

## Notes

- This log is for **your** learning, not documentation for others
- Be honest about what didn't work (that's how the system improves)
- Delete example entries once you have real ones
- No need to log every interaction, just the ones that teach you something

---

**Remember**: AI agents are like junior devs—they get better with feedback. Use this log to train them.
