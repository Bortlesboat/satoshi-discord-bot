"""Simple SQLite usage logger for command tracking."""

import hashlib
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).parent / "usage.db"


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """CREATE TABLE IF NOT EXISTS command_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            guild_id TEXT,
            user_hash TEXT,
            timestamp REAL NOT NULL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS guild_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id TEXT NOT NULL,
            guild_name TEXT,
            member_count INTEGER,
            event_type TEXT NOT NULL,
            timestamp REAL NOT NULL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS error_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            guild_id TEXT,
            error_type TEXT NOT NULL,
            error_message TEXT,
            timestamp REAL NOT NULL
        )"""
    )
    conn.commit()
    return conn


def log_command(command: str, guild_id: int | None, user_id: int | None):
    """Log a command invocation."""
    user_hash = hashlib.sha256(str(user_id).encode()).hexdigest()[:16] if user_id else None
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO command_log (command, guild_id, user_hash, timestamp) VALUES (?, ?, ?, ?)",
            (command, str(guild_id) if guild_id else None, user_hash, time.time()),
        )
        conn.commit()
    finally:
        conn.close()


def get_total_commands() -> int:
    """Get total number of commands served."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT COUNT(*) FROM command_log").fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def get_command_counts() -> dict[str, int]:
    """Get command usage counts, ordered by most popular."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT command, COUNT(*) as cnt FROM command_log GROUP BY command ORDER BY cnt DESC"
        ).fetchall()
        return {row[0]: row[1] for row in rows}
    finally:
        conn.close()


def get_unique_guilds() -> int:
    """Get number of unique guilds that have used the bot."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT COUNT(DISTINCT guild_id) FROM command_log WHERE guild_id IS NOT NULL").fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def get_unique_users() -> int:
    """Get number of unique users that have used the bot."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT COUNT(DISTINCT user_hash) FROM command_log WHERE user_hash IS NOT NULL").fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def get_commands_since(seconds_ago: float) -> int:
    """Get number of commands in the last N seconds."""
    conn = _get_conn()
    try:
        cutoff = time.time() - seconds_ago
        row = conn.execute("SELECT COUNT(*) FROM command_log WHERE timestamp > ?", (cutoff,)).fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def log_guild_event(guild_id: int, guild_name: str, member_count: int, event_type: str):
    """Log a guild join or leave event."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO guild_events (guild_id, guild_name, member_count, event_type, timestamp) VALUES (?, ?, ?, ?, ?)",
            (str(guild_id), guild_name, member_count, event_type, time.time()),
        )
        conn.commit()
    finally:
        conn.close()


def log_error(command: str | None, guild_id: int | None, error_type: str, error_message: str):
    """Log a command error."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO error_log (command, guild_id, error_type, error_message, timestamp) VALUES (?, ?, ?, ?, ?)",
            (command, str(guild_id) if guild_id else None, error_type, error_message[:500], time.time()),
        )
        conn.commit()
    finally:
        conn.close()


def get_error_count() -> int:
    """Get total error count."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT COUNT(*) FROM error_log").fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def get_guild_event_count(event_type: str) -> int:
    """Get count of guild join or leave events."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT COUNT(*) FROM guild_events WHERE event_type = ?", (event_type,)).fetchone()
        return row[0] if row else 0
    finally:
        conn.close()
