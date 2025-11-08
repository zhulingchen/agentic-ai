CREATE TABLE IF NOT EXISTS research_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    report_en TEXT NOT NULL,
    report_zh TEXT NOT NULL,
    word_count_en INTEGER,
    word_count_zh INTEGER,
    created_timestamp TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS research_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    research_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    title TEXT,
    domain TEXT,
    FOREIGN KEY (research_id) REFERENCES research_records(id) ON DELETE CASCADE
);
