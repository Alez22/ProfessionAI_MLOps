<!-- Auto-generated guidance for AI coding agents working in this repo -->
# Copilot instructions for contributors

Purpose
- Provide focused, actionable guidance for AI agents working in this repository.

Repository snapshot
- Detected files: `README.md` at repository root (very small / initial state).
- No source code, tests, or build scripts were found when scanning the workspace.

Quick start checks (what to do first)
- Run a repository file search for code patterns: `grep -R "def \|class \|package.json\|pyproject.toml\|requirements.txt" .`
- If no language files exist, open an issue or ask maintainers before adding major scaffolding.

Big picture / architecture notes
- This repository currently contains only project metadata. There is no enforced architecture to follow yet.
- When introducing components, prefer small, self-contained modules with clear README updates explaining: purpose, entry points, and how to run locally.

Developer workflows (repo-specific)
- Branching: create a feature branch `feat/<short-desc>` for new features and `fix/<short-desc>` for bug fixes.
- Commits: keep single-purpose commits and include brief descriptions in the PR body that reference this file when appropriate.
- Pull requests: target `main` (default branch). Include a short changelog entry in `README.md` or a CHANGES.md when adding features.

Project-specific conventions and patterns
- No project-specific code conventions were discovered. If you add code, include linter config and tests at the same time.
- Prefer explicit examples in `README.md` for any new command or service added.

Integration points & dependencies
- No external services or dependency manifests were found. If you add integrations (cloud, DB, model registry), document:
  - connection config file location
  - authentication steps
  - required environment variables

When to ask the maintainer
- Before creating major structure (language runtime, CI, or deployment) — this repo is currently minimal.
- If tests or CI are added, ask for the preferred CI provider and secrets handling.

Examples of useful commands for the agent to propose/run
- Find language/runtime: `rg "^\s*(import |from |using |package )" --hidden -S || true`
- List repo files: `git ls-files`

If you (human) want more detail
- Tell the agent which language/runtime you prefer (Python, Node, etc.) and whether to scaffold a minimal app, CI, and tests; the agent will create a small, runnable prototype and update this file with concrete commands.

-- End of guidance
