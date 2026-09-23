# SETUP.md — Lab Environment Build Steps

Follow this in order. Everything here uses only free GitHub features.

---

## 1. Create the repo

1. On GitHub (your personal account), create a new **public** repo named
   `sdlc-demo-app`. Public is required for CodeQL/free security features
   and so anyone can view your showcase later.
2. Do NOT initialize with a README (you already have the files here).
3. Push this folder:

```bash
cd sdlc-demo-app
git init
git add .
git commit -m "Initial commit: task tracker app scaffold"
git branch -M main
git remote add origin https://github.com/<your-username>/sdlc-demo-app.git
git push -u origin main
```

4. Edit `CODEOWNERS` and replace `@yourusername` with your real GitHub
   username, commit, and push directly (this is the last direct push to
   main you'll ever make on this repo — branch protection goes on next).

---

## 2. Turn on branch protection (Controls #1 and #2)

Repo → **Settings → Branches → Add branch protection rule**

Branch name pattern: `main`

Enable:
- [x] Require a pull request before merging
  - [x] Require approvals — set to **1**
  - [x] Dismiss stale pull request approvals when new commits are pushed
- [x] Require status checks to pass before merging
  - Search for and select: `Run test suite` (from ci.yml) and the CodeQL
    check (from codeql.yml) — these only appear in the list **after** the
    workflows have run at least once, so come back to this after step 3.
- [x] Require conversation resolution before merging
- [x] Do not allow bypassing the above settings (uncheck "allow
  administrators to bypass" — otherwise you, as admin, could self-approve
  and the control would be meaningless)

This single screen is what enforces:
- No direct pushes to `main`
- Independent review required (SoD)
- CI + SAST must pass before merge

---

## 3. Enable CodeQL and Dependabot (Control #3 evidence)

Repo → **Settings → Code security and analysis**
- Enable **Dependabot alerts**
- Enable **Dependabot security updates**
- CodeQL will auto-enable once `codeql.yml` runs (already included in this
  repo under `.github/workflows/`)

Push once more (or open a dummy PR) to trigger the first CodeQL/CI run, then
go back to step 2 and add both checks as required status checks.

---

## 4. Create a fine-grained Personal Access Token (for the automation repo later)

Settings (your account, not the repo) → **Developer settings → Personal
access tokens → Fine-grained tokens → Generate new token**

- Resource owner: your personal account
- Repository access: **Only select repositories** → `sdlc-demo-app` (add the
  Juice Shop fork here too once it exists)
- Permissions needed (read-only):
  - Contents: Read-only
  - Pull requests: Read-only
  - Issues: Read-only
  - Metadata: Read-only (mandatory default)
  - Administration: Read-only (needed to read branch protection settings)

Save the token somewhere safe for now — you'll add it as a GitHub Actions
secret when we build `sdlc-controls-automation`. **Never commit this token
to any repo.**

---

## 5. Seed the history — 6 scenarios to create manually

This is the most important step. Your controls automation is only
interesting if the evidence shows **both pass and fail states**. Create
these six PRs/issues yourself, in order, using a second GitHub account (or
ask a friend) to act as the "second reviewer" — or approve your own
alt-account's PR to keep it realistic. If you truly only have one identity
available, note this limitation openly in your README; it's a common
constraint in solo demo projects and auditors will respect the honesty more
than a fudge.

For each scenario: open a GitHub **Issue** first, then a PR that references
it with `Closes #<issue-number>` in the PR description.

| # | Issue title | PR behavior | Expected control outcome |
|---|---|---|---|
| 1 | "Add DELETE endpoint validation" | Small real code change, PR references issue, gets 1 approval from a different account, CI passes, merged normally | **PASS** — SoD, traceability, CI all green |
| 2 | "Fix task title validation bug" | Same as above but include a deliberately weak test (e.g. skip an edge case) so CI still passes but coverage looks thin | **PASS** but flagged as "weak evidence" in your report — good for showing nuance, not just binary pass/fail |
| 3 | "Emergency hotfix" | Try to push directly to `main` (it should be blocked) — take a screenshot of the block for your README | **FAIL (blocked)** — proves control #2 works |
| 4 | "Refactor task storage" | Open PR, approve it **yourself** (if using a single account) or self-merge without review | **FAIL** — flagged as SoD violation in your dashboard |
| 5 | "Add task priority field" | Open PR with no linked issue at all | **FAIL** — flagged as traceability violation |
| 6 | "Update dependency versions" | A real PR that bumps a package version, triggers Dependabot / CodeQL, merged only after checks pass | **PASS** — ties together CI + SAST gate cleanly |

Keep a plain list of these six PR numbers somewhere (a `SCENARIOS.md` note
is fine) — the automation repo will reference specific PR numbers as
"known evidence" examples in its own README/demo screenshots.

---

## 6. Access review evidence (Control #5)

Repo → **Settings → Collaborators and teams**

Take a dated screenshot or export the list (Settings page shows it plainly).
This becomes your "access review" evidence artifact — in a real org this
would be a quarterly review; for the demo, one dated snapshot plus a note
in your README saying "this would run quarterly via the same collector
script" is enough to prove you understand the control, without needing to
fabricate a history you don't have.

---

## Next

Once steps 1–6 are done, move to the Juice Shop fork (control #4 SAST
target), then `sdlc-controls-automation`, which will read all of this via
the GitHub API and turn it into a dashboard.
