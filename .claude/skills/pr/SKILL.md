---
name: pr
description: Fill .github/pull_request_template.md from this branch's commits and diff against the base branch and output it as a copyable Markdown code block in chat. Use when the user asks to create, open, or write a pull request.
argument-hint: "[base branch, default main]"
disable-model-invocation: true
---

# Write a PR description from the template

Base branch: `$ARGUMENTS` if given, otherwise `main`. Call it BASE below.

## 1. Check the branch state

- `git branch --show-current`: if it is BASE, stop and ask the user to create a feature branch.
- `git status --short`: if there are uncommitted changes, list them and ask whether to commit them first. Never commit on your own.
- `git fetch origin BASE` so the diff is against the latest base.

## 2. Collect what changed (commits, not the working tree)

- `git log --oneline origin/BASE..HEAD`: the commits in this PR. If empty, stop: nothing to PR.
- `git diff --stat origin/BASE...HEAD`: the files touched.
- `git diff origin/BASE...HEAD`: read the real diff. Don't describe changes from commit messages alone.
- `git rev-parse --abbrev-ref @{u}` and `git log --oneline @{u}..HEAD`: whether the branch is pushed and which commits are not pushed yet (only reported; never push).

## 3. Fill the template

Read `.github/pull_request_template.md` and fill in every section, keeping its headings and order:

- **Summary**: what and why, 1-3 sentences, for a reviewer who hasn't seen the code.
- **Related Issue**: only issue numbers found in commit messages or the branch name, otherwise "None". Never invent one.
- **Type of Change**: tick (`[x]`) every box that matches the diff; leave the others unticked.
- **Changes**: bullets grouped by area (`apps/api`, `apps/web`, `docs`...), based on the diff.
- **How Has This Been Tested?**: only checks that were actually run in this session or are shown in the commits. List runnable checks the diff adds (for example `*_selfcheck.py`) as commands. Say plainly what was not tested. Never claim a test passed without evidence.
- **Screenshots**: "N/A" unless the user gave some.
- **Checklist**: tick an item only if you verified it (for example, you ran `npx biome check src`). Leave uncertain items unticked.
- Remove the `<!-- -->` hint comments.
- Title: under 70 characters, imperative mood (for example "Add web UI for Kindle capture").

## 4. Output it in chat as a code block

Do not push, do not create the PR (no `gh`), and do not write a file. The user copies the text and opens the PR themselves.

1. Print the title in its own code block, so it can be copied into GitHub's Title field.
2. Print the filled body as raw Markdown inside a code block opened with four backticks plus `markdown` and closed with four backticks, so the three-backtick code blocks inside the body don't close it early.
3. After it, give the compare link for opening the PR: `https://github.com/<owner>/<repo>/compare/BASE...<branch>?expand=1` (owner/repo from `git remote get-url origin`). If the branch has unpushed commits (from step 2), say so: the user needs to push before opening the PR.
