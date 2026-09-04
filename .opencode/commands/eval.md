---
description: Run the AI evaluation suite and report scores against thresholds (RAG, agentic, GEval), and confirm the CI gate is real.
agent: eval-guardian
subtask: true
---

<!-- Two level-1 `!` lines only. Shell lives in .github/scripts/eval_context.sh; the body at
     .github/docs/prompts/commands/eval.md is instructions-only. `!` substitution is
     single-pass, so shell written inside the imported body never executes (ADR-0001).
     Do not add ad-hoc `!` here — extend the script instead (ADR-0003). -->
 
!`bash .github/scripts/eval_context.sh`
 
!`cat .github/docs/prompts/commands/eval.md`
