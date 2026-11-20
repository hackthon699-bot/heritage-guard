"""
Heritage-Guard | Person 5 Module: db_manager.py (v1.7)
Role: Thread-Safe SQLite GI Registry Vault & Security Audit Logger
      with Non-Destructive Schema Migration.
"""

import os
import time
import sqlite3
import threading

VERSION = "1.7"
DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heritage_guard_local.db")


class DatabaseManager:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_and_migrate_tables()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_and_migrate_tables(self):
        with self.lock:
            conn = self._get_conn()
            try:
                cur = conn.cursor()

                # Non-destructive migration: rename legacy table instead of dropping historical data
                cur.execute("PRAGMA table_info(security_audit_logs)")
                audit_cols = {row[1] for row in cur.fetchall()}
                if audit_cols and ("time_str" not in audit_cols or "event_type" not in audit_cols):
                    backup_name = f"security_audit_logs_legacy_{int(time.time())}"
                    cur.execute(f"ALTER TABLE security_audit_logs RENAME TO {backup_name}")

                cur.execute("PRAGMA table_info(gi_registry_vault)")
                vault_cols = {row[1] for row in cur.fetchall()}
                if vault_cols and ("gi_cluster" not in vault_cols or "watermark_payload" not in vault_cols):
                    backup_name = f"gi_registry_vault_legacy_{int(time.time())}"
                    cur.execute(f"ALTER TABLE gi_registry_vault RENAME TO {backup_name}")

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS gi_registry_vault (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sha256_hash TEXT UNIQUE NOT NULL,
                        artisan_id TEXT NOT NULL,
                        gi_cluster TEXT NOT NULL,
                        watermark_payload TEXT NOT NULL,
                        cloak_mode TEXT NOT NULL,
                        psnr_db REAL NOT NULL,
                        jpeg_survival_pct REAL NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS security_audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time_str TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        reason TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
            finally:
                conn.close()

    def register_gi_asset(
        self,
        sha256_hash: str,
        artisan_id: str,
        gi_cluster: str,
        watermark_payload: str,
        cloak_mode: str,
        psnr_db: float,
        jpeg_survival_pct: float,
    ) -> bool:
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            conn = self._get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT OR REPLACE INTO gi_registry_vault
                    (sha256_hash, artisan_id, gi_cluster, watermark_payload, cloak_mode, psnr_db, jpeg_survival_pct, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (sha256_hash, artisan_id, gi_cluster, watermark_payload, cloak_mode, psnr_db, jpeg_survival_pct, now_str),
                )
                conn.commit()
                return True
            finally:
                conn.close()

    def get_gi_asset_by_hash(self, sha256_hash: str) -> dict:
        with self.lock:
            conn = self._get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT sha256_hash, artisan_id, gi_cluster, watermark_payload, cloak_mode, psnr_db, created_at "
                    "FROM gi_registry_vault WHERE sha256_hash = ?",
                    (sha256_hash,),
                )
                row = cur.fetchone()
                if not row:
                    return {}
                return {
                    "sha256_hash": row[0],
                    "artisan_id": row[1],
                    "gi_cluster": row[2],
                    "watermark_payload": row[3],
                    "cloak_mode": row[4],
                    "psnr_db": row[5],
                    "created_at": row[6],
                }
            finally:
                conn.close()

    def log_security_event(self, event_type: str, reason: str):
        t_str = time.strftime("%H:%M:%S")
        with self.lock:
            conn = self._get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO security_audit_logs (time_str, event_type, reason) VALUES (?, ?, ?)",
                    (t_str, event_type, reason),
                )
                conn.commit()
            finally:
                conn.close()

    def get_recent_security_logs(self, limit: int = 15) -> list:
        with self.lock:
            conn = self._get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT time_str, event_type, reason FROM security_audit_logs ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
                rows = cur.fetchall()
                return [{"time_str": r[0], "event": r[1], "reason": r[2]} for r in rows]
            finally:
                conn.close()