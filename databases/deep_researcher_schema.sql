CREATE TABLE IF NOT EXISTS research_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    report_en TEXT NOT NULL,
    report_zh TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
