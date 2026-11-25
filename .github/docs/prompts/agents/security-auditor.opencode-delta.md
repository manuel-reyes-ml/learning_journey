> 🔒 **OpenCode note:** this agent runs on a **cloud model** (GLM-5.2 via OpenCode Go,
> 0-day retention). Repository code leaves the machine when it runs. Point it only at
> repos that hold synthetic data. The real PII boundary is the pre-commit layer
> (gitleaks + detect-private-key), not this agent.
