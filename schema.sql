-- HERITAGE-GUARD | Person 5 SQL GI Vault Schema (v1.7 - Synced with db_manager.py)

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
);

CREATE INDEX IF NOT EXISTS idx_gi_vault_sha256 ON gi_registry_vault(sha256_hash);

CREATE TABLE IF NOT EXISTS security_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_str TEXT NOT NULL,
    event_type TEXT NOT NULL,
    reason TEXT NOT NULL
);