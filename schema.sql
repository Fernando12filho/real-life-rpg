CREATE TABLE IF NOT EXISTS character (
  id INTEGER PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS attribute (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  xp INTEGER DEFAULT 0,
  base_level INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS quest (
  id INTEGER PRIMARY KEY,
  title TEXT,
  description TEXT,
  attr TEXT,
  xp INTEGER,
  status TEXT DEFAULT 'open',
  type TEXT DEFAULT 'side',
  created_at TEXT,
  due_date TEXT
);

CREATE TABLE IF NOT EXISTS journal (
  id INTEGER PRIMARY KEY,
  note TEXT,
  created_at TEXT
);
