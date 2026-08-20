> 🔒 **How your limits are enforced.** OpenCode expressed this agent's boundary as a
> per-agent allow/deny path map. **Claude Code has no equivalent** — `permissions`
> rules are project-global, not per-subagent. Your boundary is therefore enforced by
> the scoped `PreToolUse` hook in your own frontmatter, which blocks any write outside
> the doc surface. If a write is blocked, that is the design working; report the
> intended change and hand it to Build mode rather than looking for a way around it.
