"""Point `import httpx` at httpx2 before respx patches the wrong module."""

import httpx2

httpx2.alias_httpx()  # makes `import httpx` / `import httpcore` resolve to httpx2 / httpcore2
