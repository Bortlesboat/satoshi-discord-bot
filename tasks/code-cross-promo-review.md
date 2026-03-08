# Cross-Promotion Code Review: Satoshi Discord Bot <-> bitcoinsapi.com

**Date:** 2026-03-07
**Reviewer:** Code Review Lead

---

## 1. Current Cross-Promotion State

### Bot -> API (what exists today)

| Location | What's There | Notes |
|----------|-------------|-------|
| `embeds.py` L8 | `FOOTER_TEXT = "Powered by Satoshi API \| bitcoinsapi.com"` | Every `btc_embed()` and `error_embed()` includes this. Good — global branding. |
| `cogs/price.py` L42 | `embed.set_footer(text="Powered by Satoshi API \| Not financial advice \| bitcoinsapi.com")` | **Overrides** the default footer from `btc_embed()` — adds "Not financial advice" disclaimer. Duplicate/inconsistent with `embeds.py` default. |
| `cogs/tools.py` L62 | Same override as price.py | Same inconsistency — `/convert` overrides footer. |
| `cogs/tools.py` L108 | `/help` command has invite link but **no link to bitcoinsapi.com** | Missed opportunity — the help command is the highest-intent surface for cross-promo. |
| `README.md` L3, L45-46, L53, L58 | 4 references to bitcoinsapi.com, 2 hyperlinked | Solid coverage. Architecture diagram mentions it. "Powered by" in opening line. |
| `config.py` L7 | Default API_URL is `https://bitcoinsapi.com` | Functional, not promotional. |
| `.env.example` L2-3 | References bitcoinsapi.com and API key | Functional. |
| `bot.py` L54-58 | Presence: "Watching Bitcoin in N servers" | **No mention of API** — could add "bitcoinsapi.com" or "Satoshi API" to presence. |

### API -> Bot (what exists today)

| Location | What's There |
|----------|-------------|
| `bitcoin-api/static/index.html` | **Zero mentions of Discord or the bot.** Searched all static HTML files — no Discord references anywhere. |

**Summary:** The bot promotes the API reasonably well via footers and README. The API website does not mention the bot at all. The `/help` command — the single best in-app promo surface — has no API link. Two cogs override the global footer inconsistently.

---

## 2. Code Touchpoints Per Change Type

### A. Bot Embed Footer (consistency fix)

**Files to change:**
- `cogs/price.py` L42 — remove `set_footer` override (let `btc_embed()` handle it)
- `cogs/tools.py` L62 — remove `set_footer` override (same)
- `embeds.py` L8 — optionally update `FOOTER_TEXT` to include "Not financial advice" globally so no cog needs to override

**Complexity:** Trivial. 3 lines changed, 0 logic impact. The "Not financial advice" text should live in the global `FOOTER_TEXT` constant if it's desired on all embeds.

### B. /help Command — Add API Link

**File to change:**
- `cogs/tools.py` L103-111 — the bottom field of the `/help` embed. Add a line like `[Satoshi API](https://bitcoinsapi.com) | [GitHub](https://github.com/Bortlesboat/bitcoin-api)`

**Complexity:** Trivial. Single string addition in existing field.

### C. Bot Presence / Activity

**File to change:**
- `bot.py` L56-58 (and L66-68, L76-78) — `change_presence()` calls. Could change to `"Bitcoin data | bitcoinsapi.com"` or keep current and add a rotating presence.

**Complexity:** Low. If static text change, trivial (3 locations). If rotating presence (cycling between "Bitcoin in N servers" and "bitcoinsapi.com"), medium — requires a background task loop.

### D. README Updates (bot repo)

**File to change:**
- `README.md` — already good. Could add a "Powered by" badge at the top (shields.io style).

**Complexity:** Trivial.

### E. API Website — Add Discord Bot Section

**File to change:**
- `bitcoin-api/static/index.html` — add a "Discord Bot" card in the use cases or ecosystem section, or add it to the bottom CTA section (L845-853) alongside "Get Started", "Interactive Docs", and "Self-Host".

**Complexity:** Low. The landing page is a single self-contained HTML file. Adding a card or CTA button requires ~10-20 lines of HTML. No build system, no templating — direct edit.

**Specific insertion points:**
- Bottom CTA section (L845-853): Add a 4th button: `<a href="https://discord.com/oauth2/authorize?client_id=1479972638918049895..." class="btn-secondary">Discord Bot</a>`
- Or create a new section between the existing use cases and the bottom CTA.

### F. API Website — Footer Link

**File to change:**
- `bitcoin-api/static/index.html` L860-867 (footer area) — add Discord invite link alongside existing Status/Privacy/Terms links.

**Complexity:** Trivial. One `<a>` tag.

---

## 3. Implementation Complexity Summary

| Change | Complexity | Files | Lines Changed |
|--------|-----------|-------|--------------|
| Fix inconsistent footers (A) | Trivial | 3 | ~5 |
| Add API link to /help (B) | Trivial | 1 | ~2 |
| Static presence text (C) | Trivial | 1 | ~3 |
| Rotating presence (C alt) | Medium | 1 | ~20 (new task loop) |
| README badge (D) | Trivial | 1 | ~1 |
| API website Discord CTA (E) | Low | 1 | ~15 |
| API website footer link (F) | Trivial | 1 | ~1 |

**Total for all non-rotating changes: ~7 files, ~27 lines.** Very low risk.

---

## 4. Code Quality Review: Recent Analytics Additions

### Files reviewed: `usage_log.py`, `bot.py` (event hooks), `cogs/tools.py` (`/stats` command)

### Overall Assessment: Solid for an MVP. A few items to tighten.

### Strengths

1. **Privacy-conscious design.** User IDs are SHA-256 hashed (L48) before storage — good practice, prevents PII in the DB.
2. **Error message truncation.** `error_message[:500]` (L133) prevents unbounded storage from stack traces.
3. **Clean separation.** `usage_log.py` is a self-contained module with no Discord imports — testable in isolation.
4. **Consistent try/finally pattern.** Every function opens a connection and closes it in `finally`. No leaked connections.
5. **Guild event tracking.** `on_guild_join` and `on_guild_remove` both log with member count — useful for growth analytics.

### Issues

#### Issue 1: Connection-per-call anti-pattern (Low severity)
Every function calls `_get_conn()` which opens a new connection AND runs 3 CREATE TABLE IF NOT EXISTS statements. For a bot handling commands, this means:
- Every `/price` command = 1 new SQLite connection + 3 DDL statements
- The `/stats` command alone calls 5 functions = 5 connections + 15 DDL statements

**Recommendation:** Run CREATE TABLE once at module load or on first call (with a module-level flag). Consider a connection pool or a single long-lived connection with proper thread safety (`check_same_thread=False`).

#### Issue 2: No indexes on `command_log` (Low severity, future concern)
The `timestamp` column is queried with `WHERE timestamp > ?` in `get_commands_since()`, and `guild_id`/`user_hash` are used in `COUNT(DISTINCT ...)` queries. With thousands of rows these will be fine, but at scale:

**Recommendation:** Add `CREATE INDEX IF NOT EXISTS idx_command_log_ts ON command_log(timestamp)` — one line, future-proofs the time-range queries.

#### Issue 3: `get_unique_guilds()` counts from command_log, not guild_events (Nitpick)
`get_unique_guilds()` counts distinct `guild_id` from `command_log`, which means it reports "guilds that have used commands" not "guilds the bot is in." The `/stats` command separately shows `len(self.bot.guilds)` for current server count. This is fine but the naming is slightly misleading.

**Recommendation:** The value returned by `get_unique_guilds()` is not actually used in `/stats` (L134 uses `self.bot.guilds`). Consider removing it or renaming to `get_guilds_with_usage()`.

#### Issue 4: Footer override inconsistency (mentioned above)
`cogs/price.py` L42 and `cogs/tools.py` L62 both manually set footers that differ from the global `FOOTER_TEXT` in `embeds.py`. The `/convert` command calls `btc_embed()` (which sets the footer) and then immediately overrides it with `set_footer()`.

**Recommendation:** Either update `FOOTER_TEXT` to include "Not financial advice" globally, or remove the overrides.

#### Issue 5: `get_commands_since` and `get_unique_users` — clean implementations
Both are straightforward, correct SQL. `get_commands_since` takes seconds (not a datetime), which matches the `time.time()` storage format — consistent. `get_unique_users` correctly counts distinct hashes, not raw user IDs. No issues.

#### Issue 6: `guild_events` table stores `guild_name` (Informational)
Guild names can change. The table captures the name at event time, which is actually the right behavior for a log table (snapshot, not current state). Good design choice.

### Code Quality Score: 7.5/10
Clean, functional, well-structured for a small bot. The connection-per-call pattern is the main thing to address before scaling. No bugs found. The analytics data model is sound.
