# Satoshi Discord Bot — Analytics Review

**Date:** 2026-03-07
**Reviewer:** Analytics Review Agent

---

## Current State

### What Exists

**Database:** `usage.db` (SQLite), single table `command_log`:
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| command | TEXT | Slash command name |
| guild_id | TEXT | Nullable, stored as string |
| user_hash | TEXT | SHA-256 prefix (16 chars) — good privacy practice |
| timestamp | REAL | Unix epoch |

**Logging hook:** `on_app_command_completion` in `bot.py` fires after every successful slash command, calling `log_command()`.

**Query functions in `usage_log.py`:**
- `get_total_commands()` — count of all rows
- `get_command_counts()` — per-command breakdown, ordered by popularity
- `get_unique_guilds()` — distinct guild_id count from command_log

**User-facing:** `/stats` command in `cogs/tools.py` displays total commands, server count (from `bot.guilds`), guilds using commands, and top 5 commands.

### What Works Well

- Privacy-respecting user tracking (hashed IDs, truncated)
- Timestamp on every event enables time-series analysis later
- Clean separation of logging (`usage_log.py`) from bot logic
- `/stats` gives a nice public-facing growth signal

---

## Gaps and Missing Analytics

### 1. No Guild Join/Leave Tracking

**Problem:** There is no `on_guild_join` or `on_guild_remove` handler. The bot knows the current guild count at startup (`on_ready` logs it), but there is no historical record of when servers added or removed the bot.

**Impact:** Cannot measure growth rate, churn rate, or correlate installs with directory listing events.

**Recommendation:** Add a `guild_events` table:
```
guild_events (id, guild_id, guild_name, member_count, event_type ['join'|'leave'], timestamp)
```
Hook into `on_guild_join` and `on_guild_remove`. Log guild name and member count at join time for sizing analysis.

### 2. No Install Attribution (Directory Tracking)

**Problem:** Cannot distinguish whether a guild add came from top.gg, discordbotlist.com, the support Discord invite, or organic discovery.

**Impact:** No way to measure ROI of directory listings or prioritize where to invest effort.

**Recommendation:** Two approaches, use both:

- **OAuth2 `state` parameter:** When generating invite links for each directory, append a unique UTM-style query param or use Discord's OAuth2 `state` param. However, Discord's bot invite flow does not reliably pass custom state back to the bot, so this has limited utility.

- **Temporal correlation (practical approach):** Log guild joins with timestamps. Cross-reference against known directory listing approval dates and any upvote/bump activity on top.gg or discordbotlist. Spikes in joins after a listing goes live = attribution signal. This is the realistic approach.

- **top.gg webhook:** top.gg provides a webhook that fires when users vote for your bot. Set up a `/topgg-webhook` endpoint (or use their Python SDK `topggpy`) to capture vote events. Votes correlate with visibility boosts on the platform.

### 3. No Error Tracking

**Problem:** The global error handler in `bot.py` (`on_app_command_error`) logs exceptions to stdout but does not write to the database. `on_app_command_completion` only fires on *successful* commands, so errors are invisible to analytics.

**Impact:** No error rate metric. Cannot identify which commands are flaky, whether the API is degrading, or if specific guilds hit errors disproportionately.

**Recommendation:** Add an `error_log` table:
```
error_log (id, command, guild_id, error_type, error_message, timestamp)
```
Log from `on_app_command_error`. Classify errors: `rate_limit`, `api_unavailable`, `api_error`, `unhandled`. This enables:
- Error rate per command
- API reliability monitoring
- Rate limit hit frequency

### 4. No Response Latency Tracking

**Problem:** No measurement of how long commands take to respond. Users in high-latency scenarios get a degraded experience with no visibility.

**Impact:** Cannot identify slow commands, API degradation over time, or regional performance differences.

**Recommendation:** Add a `latency_ms` column to `command_log`. Capture `time.time()` at `interaction.created_at` (Discord provides this) and compare to completion time. Alternatively, wrap the `on_app_command_completion` hook to compute the delta between `interaction.created_at` and `datetime.utcnow()`. This gives per-command p50/p95/p99 latency.

### 5. No Daily/Weekly Aggregation

**Problem:** All queries run against raw rows. As volume grows, queries like `COUNT(*)` will slow down. There is also no pre-computed trend data for the `/stats` command.

**Impact:** At low volume this is fine. At 10K+ rows per day, raw queries become expensive on SQLite.

**Recommendation:** Two phases:
- **Short term (now):** Add query functions for time-windowed data — `get_commands_since(timestamp)` for "today", "this week", "last 7 days" breakdowns. Add these to `/stats` output (e.g., "Today: 42 | This week: 287 | All time: 1,204").
- **Medium term (1K+ daily commands):** Add a `daily_stats` rollup table:
  ```
  daily_stats (date TEXT, command TEXT, count INTEGER, unique_users INTEGER, unique_guilds INTEGER, avg_latency_ms REAL, error_count INTEGER)
  ```
  Run a nightly aggregation (cron or background task) that rolls up the previous day. Query rollup table for trends instead of raw logs.

### 6. No Unique User Metrics

**Problem:** `user_hash` is stored but never queried. No function to get unique user count or per-user command frequency.

**Recommendation:** Add `get_unique_users()` and expose in `/stats`. Also useful: DAU (daily active users) and retention (users who return after 7+ days).

### 7. No Guild Size Context

**Problem:** When a guild adds the bot, we don't know if it's a 10-person server or a 50K-member community. This matters for prioritizing support and understanding reach.

**Recommendation:** Capture `guild.member_count` in the `guild_events` join record. Optionally snapshot all current guilds + member counts on startup.

---

## Priority Ranking

| # | Item | Effort | Impact | Priority |
|---|------|--------|--------|----------|
| 1 | Guild join/leave tracking | Low | High | **Do first** |
| 2 | Error logging to DB | Low | High | **Do first** |
| 3 | Time-windowed queries + `/stats` enhancement | Low | Medium | **Do second** |
| 4 | Unique user metrics | Trivial | Medium | **Do second** |
| 5 | Response latency tracking | Medium | Medium | **Do third** |
| 6 | Daily rollup table | Medium | Low (until scale) | Later |
| 7 | top.gg webhook integration | Medium | Medium | Later |
| 8 | Directory install attribution (temporal) | Low | Medium | Ongoing analysis |

---

## Implementation Notes

- All new tables should be created with `CREATE TABLE IF NOT EXISTS` in `_get_conn()` or a dedicated `init_db()` function to keep the migration-free pattern.
- Consider extracting DB init into a single `init_db()` call at bot startup rather than checking on every `_get_conn()` call. This avoids repeated CREATE TABLE overhead.
- The `usage.db` file lives alongside `bot.py`. Back it up periodically — it is the only analytics store. A cron job on GMKtec to `cp usage.db usage.db.bak` daily would be cheap insurance.
- For the `/stats` command, consider an owner-only `/analytics` command with richer data (error rates, latency percentiles, daily trends) vs. the public-facing `/stats` which stays simple.

---

## Summary

The current analytics setup covers the basics (command counts, guild counts, per-command breakdown) and is well-structured. The biggest gaps are: **no guild join/leave history** (critical for measuring distribution effectiveness), **no error tracking** (blind to reliability issues), and **no time-series queries** (cannot see trends). All three are low-effort, high-value additions. Latency tracking and daily rollups are worthwhile but less urgent at current scale.
