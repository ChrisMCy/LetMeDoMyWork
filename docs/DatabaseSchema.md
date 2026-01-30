# LetMeDoMyWork - Database Schema Specification

## Database Technology
- **Engine:** SQLite 3
- **Flutter Package:** `sqflite ^2.3.0`
- **Location:** `/data/data/com.letmedomywork.app/databases/letmedomywork.db`
- **Version:** 1 (initial release)

---

## Schema Overview
```
Tables:
1. settings          - App configuration and SMTP settings
2. todos             - TODO entries (email campaigns)
3. sent_emails       - History of sent emails
4. error_log         - Email send failures (optional for v1.0)

Relationships:
todos (1) ──< (N) sent_emails
```

---

## Table Definitions

### 1. settings

**Purpose:** Stores app-wide configuration, SMTP settings, and template libraries.

**Note:** This is a singleton table (always exactly 1 row with id=1).
```sql
CREATE TABLE settings (
  id INTEGER PRIMARY KEY CHECK(id = 1),  -- Singleton constraint
  
  -- Reminder Configuration
  max_follow_ups INTEGER NOT NULL DEFAULT 10
    CHECK(max_follow_ups >= 1 AND max_follow_ups <= 30),
  randomize_minutes INTEGER NOT NULL DEFAULT 30
    CHECK(randomize_minutes >= 0 AND randomize_minutes <= 120),
  
  -- SMTP Configuration
  smtp_provider TEXT CHECK(smtp_provider IN ('gmail', 'outlook', 'custom', NULL)),
  smtp_host TEXT,
  smtp_port INTEGER CHECK(smtp_port >= 1 AND smtp_port <= 65535),
  smtp_username TEXT,  -- Email address
  smtp_use_tls INTEGER NOT NULL DEFAULT 1,  -- Boolean: 1=true, 0=false
  
  -- Password stored separately in flutter_secure_storage
  -- These fields are markers only
  smtp_password_encrypted TEXT DEFAULT '[ENCRYPTED]',
  
  -- Template Libraries (JSON Arrays)
  -- Each array contains 30+ strings
  subjects_de TEXT NOT NULL,  -- JSON: ["Subject 1", "Subject 2", ...]
  subjects_en TEXT NOT NULL,
  texts_de TEXT NOT NULL,
  texts_en TEXT NOT NULL,
  
  -- Selected Template Indices (JSON Arrays)
  -- Contains indices into the above arrays
  -- Length = max_follow_ups (default 10)
  selected_subjects_de TEXT NOT NULL,  -- JSON: [0, 1, 2, 3, ...]
  selected_subjects_en TEXT NOT NULL,
  selected_texts_de TEXT NOT NULL,
  selected_texts_en TEXT NOT NULL,
  
  -- Metadata
  last_opened INTEGER NOT NULL,  -- UNIX timestamp (milliseconds)
  created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
  updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000)
);

-- Singleton enforcement trigger
CREATE TRIGGER prevent_multiple_settings
BEFORE INSERT ON settings
WHEN (SELECT COUNT(*) FROM settings) >= 1
BEGIN
  SELECT RAISE(ABORT, 'Only one settings row allowed');
END;

-- Auto-update updated_at timestamp
CREATE TRIGGER settings_updated_at
AFTER UPDATE ON settings
BEGIN
  UPDATE settings SET updated_at = strftime('%s', 'now') * 1000 WHERE id = 1;
END;
```

**Field Details:**

| Field | Type | Description | Default | Constraints |
|-------|------|-------------|---------|-------------|
| `id` | INTEGER | Primary key, always 1 | 1 | CHECK(id=1) |
| `max_follow_ups` | INTEGER | Maximum follow-up emails | 10 | 1-30 |
| `randomize_minutes` | INTEGER | ± minutes for send time | 30 | 0-120 |
| `smtp_provider` | TEXT | Email provider type | NULL | 'gmail', 'outlook', 'custom', NULL |
| `smtp_host` | TEXT | SMTP server hostname | NULL | - |
| `smtp_port` | INTEGER | SMTP server port | NULL | 1-65535 |
| `smtp_username` | TEXT | Email address for login | NULL | - |
| `smtp_use_tls` | INTEGER | Use TLS encryption | 1 | 0 or 1 |
| `smtp_password_encrypted` | TEXT | Marker (actual password in secure storage) | '[ENCRYPTED]' | - |
| `subjects_de` | TEXT | German subjects (JSON array) | Required | Valid JSON |
| `subjects_en` | TEXT | English subjects (JSON array) | Required | Valid JSON |
| `texts_de` | TEXT | German texts (JSON array) | Required | Valid JSON |
| `texts_en` | TEXT | English texts (JSON array) | Required | Valid JSON |
| `selected_subjects_de` | TEXT | Selected German subject indices | Required | Valid JSON |
| `selected_subjects_en` | TEXT | Selected English subject indices | Required | Valid JSON |
| `selected_texts_de` | TEXT | Selected German text indices | Required | Valid JSON |
| `selected_texts_en` | TEXT | Selected English text indices | Required | Valid JSON |
| `last_opened` | INTEGER | Last app open timestamp | Required | UNIX ms |
| `created_at` | INTEGER | Row creation timestamp | Auto | UNIX ms |
| `updated_at` | INTEGER | Last update timestamp | Auto | UNIX ms |

**JSON Format Examples:**
```json
// subjects_de (30 elements)
[
  "Follow-Up: {InitialSubject}",
  "Nochmal bzgl.: {InitialSubject}",
  "Kurze Erinnerung: {InitialSubject}",
  ...
]

// selected_subjects_de (10 elements - indices into subjects_de)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Initial Data (Seed):**
```sql
INSERT INTO settings (
  id,
  max_follow_ups,
  randomize_minutes,
  smtp_provider,
  subjects_de,
  subjects_en,
  texts_de,
  texts_en,
  selected_subjects_de,
  selected_subjects_en,
  selected_texts_de,
  selected_texts_en,
  last_opened
) VALUES (
  1,
  10,
  30,
  NULL,
  '[...]',  -- 30 default German subjects
  '[...]',  -- 30 default English subjects
  '[...]',  -- 30 default German texts
  '[...]',  -- 30 default English texts
  '[0,1,2,3,4,5,6,7,8,9]',
  '[0,1,2,3,4,5,6,7,8,9]',
  '[0,1,2,3,4,5,6,7,8,9]',
  '[0,1,2,3,4,5,6,7,8,9]',
  strftime('%s', 'now') * 1000
);
```

---

### 2. todos

**Purpose:** Stores TODO entries (email reminder campaigns).
```sql
CREATE TABLE todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Basic Information
  subject TEXT NOT NULL,
  recipient_email TEXT NOT NULL,
  recipient_first_name TEXT,
  recipient_last_name TEXT,
  
  -- Email Content
  initial_text TEXT NOT NULL,
  language TEXT NOT NULL CHECK(language IN ('de', 'en')),
  
  -- Scheduling
  start_date INTEGER NOT NULL,  -- UNIX timestamp (milliseconds), date only
  send_time TEXT NOT NULL,  -- Format: "HH:MM" (e.g., "09:00")
  interval_days INTEGER NOT NULL CHECK(interval_days >= 1),
  next_send_datetime INTEGER NOT NULL,  -- UNIX timestamp (milliseconds)
  
  -- Template Selection (JSON Arrays of indices)
  selected_subject_indices TEXT NOT NULL,  -- JSON: [0, 1, 2, ...]
  selected_text_indices TEXT NOT NULL,     -- JSON: [0, 1, 2, ...]
  
  -- Flags
  already_sent_first INTEGER NOT NULL DEFAULT 0 CHECK(already_sent_first IN (0, 1)),
  is_paused INTEGER NOT NULL DEFAULT 0 CHECK(is_paused IN (0, 1)),
  is_completed INTEGER NOT NULL DEFAULT 0 CHECK(is_completed IN (0, 1)),
  pending_send INTEGER NOT NULL DEFAULT 0 CHECK(pending_send IN (0, 1)),
  
  -- Metadata
  created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
  completed_at INTEGER,  -- NULL if not completed
  
  -- Constraints
  CHECK(
    (is_completed = 0 AND completed_at IS NULL) OR
    (is_completed = 1 AND completed_at IS NOT NULL)
  )
);

-- Indices for performance
CREATE INDEX idx_todos_next_send 
  ON todos(next_send_datetime, is_paused, is_completed);

CREATE INDEX idx_todos_completed 
  ON todos(is_completed, completed_at DESC);

CREATE INDEX idx_todos_paused 
  ON todos(is_paused);

CREATE INDEX idx_todos_recipient 
  ON todos(recipient_email, is_completed);

CREATE INDEX idx_todos_pending 
  ON todos(pending_send, next_send_datetime);

-- Auto-update completed_at when is_completed changes
CREATE TRIGGER todos_completed
AFTER UPDATE OF is_completed ON todos
WHEN NEW.is_completed = 1 AND OLD.is_completed = 0
BEGIN
  UPDATE todos SET completed_at = strftime('%s', 'now') * 1000 WHERE id = NEW.id;
END;

-- Clear completed_at when reopening
CREATE TRIGGER todos_reopened
AFTER UPDATE OF is_completed ON todos
WHEN NEW.is_completed = 0 AND OLD.is_completed = 1
BEGIN
  UPDATE todos SET completed_at = NULL WHERE id = NEW.id;
END;
```

**Field Details:**

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | INTEGER | Primary key | Auto-increment |
| `subject` | TEXT | Email subject/title | NOT NULL |
| `recipient_email` | TEXT | Recipient email address | NOT NULL, email format |
| `recipient_first_name` | TEXT | First name (parsed or manual) | NULL allowed |
| `recipient_last_name` | TEXT | Last name (parsed or manual) | NULL allowed |
| `initial_text` | TEXT | Initial email text | NOT NULL |
| `language` | TEXT | Template language | 'de' or 'en' |
| `start_date` | INTEGER | Start date (UNIX ms, date only) | NOT NULL |
| `send_time` | TEXT | Send time (HH:MM) | NOT NULL, "00:00"-"23:59" |
| `interval_days` | INTEGER | Days between sends | >= 1 |
| `next_send_datetime` | INTEGER | Next scheduled send (UNIX ms) | NOT NULL |
| `selected_subject_indices` | TEXT | Selected subject indices (JSON) | Valid JSON array |
| `selected_text_indices` | TEXT | Selected text indices (JSON) | Valid JSON array |
| `already_sent_first` | INTEGER | First email already sent? | 0 or 1 |
| `is_paused` | INTEGER | Is TODO paused? | 0 or 1 |
| `is_completed` | INTEGER | Is TODO completed? | 0 or 1 |
| `pending_send` | INTEGER | Send pending (offline)? | 0 or 1 |
| `created_at` | INTEGER | Creation timestamp (UNIX ms) | Auto |
| `completed_at` | INTEGER | Completion timestamp (UNIX ms) | NULL if not completed |

**Data Examples:**
```sql
-- Example TODO (Active, not paused)
INSERT INTO todos (
  subject,
  recipient_email,
  recipient_first_name,
  recipient_last_name,
  initial_text,
  language,
  start_date,
  send_time,
  interval_days,
  next_send_datetime,
  selected_subject_indices,
  selected_text_indices,
  already_sent_first,
  is_paused,
  is_completed
) VALUES (
  'Project Update',
  'john.doe@example.com',
  'John',
  'Doe',
  'Hi John,\n\nI wanted to follow up on our conversation about the project timeline...',
  'en',
  1738108800000,  -- 2026-01-29 00:00:00 UTC
  '09:00',
  1,
  1738144600000,  -- 2026-01-29 09:10:00 UTC (with randomization)
  '[0,1,2,3,4,5,6,7,8,9]',
  '[0,1,2,3,4,5,6,7,8,9]',
  0,
  0,
  0
);

-- Example TODO (Paused)
INSERT INTO todos (..., is_paused) VALUES (..., 1);

-- Example TODO (Completed)
INSERT INTO todos (..., is_completed, completed_at) 
VALUES (..., 1, 1738108800000);
```

---

### 3. sent_emails

**Purpose:** Tracks all sent emails with full content and metadata.
```sql
CREATE TABLE sent_emails (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  todo_id INTEGER NOT NULL,
  
  -- Email Content (as sent)
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  
  -- Metadata
  sent_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
  send_number INTEGER NOT NULL,  -- 1st, 2nd, 3rd... send for this TODO
  template_index INTEGER NOT NULL,  -- Which template was used (for statistics)
  
  -- Foreign Key
  FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
  
  -- Constraints
  CHECK(send_number >= 1),
  CHECK(template_index >= 0)
);

-- Indices for performance
CREATE INDEX idx_sent_emails_todo 
  ON sent_emails(todo_id, sent_at DESC);

CREATE INDEX idx_sent_emails_date 
  ON sent_emails(sent_at DESC);

CREATE INDEX idx_sent_emails_template 
  ON sent_emails(template_index);

-- Auto-increment send_number per TODO
CREATE TRIGGER sent_emails_send_number
BEFORE INSERT ON sent_emails
FOR EACH ROW
WHEN NEW.send_number IS NULL OR NEW.send_number = 0
BEGIN
  SELECT RAISE(ABORT, 'send_number must be provided');
END;
```

**Field Details:**

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | INTEGER | Primary key | Auto-increment |
| `todo_id` | INTEGER | Reference to todos.id | NOT NULL, Foreign Key |
| `subject` | TEXT | Email subject (with placeholders replaced) | NOT NULL |
| `body` | TEXT | Email body (with placeholders replaced) | NOT NULL |
| `sent_at` | INTEGER | When email was sent (UNIX ms) | Auto |
| `send_number` | INTEGER | 1st, 2nd, 3rd... send for this TODO | >= 1 |
| `template_index` | INTEGER | Which template was used | >= 0 |

**Cascade Behavior:**
- When a TODO is deleted, all its `sent_emails` are automatically deleted (CASCADE).

**Data Example:**
```sql
INSERT INTO sent_emails (
  todo_id,
  subject,
  body,
  sent_at,
  send_number,
  template_index
) VALUES (
  1,
  'Follow-Up: Project Update',
  'Hallo John,\n\nich wollte kurz nachhaken bezüglich meiner Mail vom 27.01.2026. Hattest du schon Zeit, das anzuschauen?\n\nViele Grüße',
  1738231200000,  -- 2026-01-30 09:00:00 UTC
  1,
  0
);
```

---

### 4. error_log (Optional for v1.0)

**Purpose:** Logs email send failures for debugging and retry.
```sql
CREATE TABLE error_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  todo_id INTEGER,  -- NULL if error not TODO-specific
  
  -- Error Details
  error_type TEXT NOT NULL,  -- e.g., 'SMTP_AUTH_FAILED', 'NETWORK_ERROR'
  error_message TEXT NOT NULL,
  stack_trace TEXT,
  
  -- Context
  context TEXT,  -- JSON with additional context
  
  -- Metadata
  occurred_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
  
  -- Foreign Key (optional)
  FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE SET NULL
);

-- Index for querying errors by TODO
CREATE INDEX idx_error_log_todo 
  ON error_log(todo_id, occurred_at DESC);

-- Index for recent errors
CREATE INDEX idx_error_log_date 
  ON error_log(occurred_at DESC);
```

**Field Details:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `todo_id` | INTEGER | Associated TODO (NULL if general error) |
| `error_type` | TEXT | Error category |
| `error_message` | TEXT | Human-readable error message |
| `stack_trace` | TEXT | Full stack trace (optional) |
| `context` | TEXT | Additional context as JSON |
| `occurred_at` | INTEGER | Error timestamp (UNIX ms) |

**Data Example:**
```sql
INSERT INTO error_log (
  todo_id,
  error_type,
  error_message,
  context
) VALUES (
  1,
  'SMTP_AUTH_FAILED',
  'Authentication failed: Invalid username or password',
  '{"smtp_host": "smtp.gmail.com", "smtp_port": 587, "smtp_username": "user@gmail.com"}'
);
```

**Note:** This table is OPTIONAL for v1.0. Can be added later if needed for better error tracking.

---

## Queries & Operations

### Common Queries

**1. Get all active TODOs (sorted):**
```sql
SELECT 
  t.*,
  COUNT(se.id) as send_count
FROM todos t
LEFT JOIN sent_emails se ON se.todo_id = t.id
WHERE t.is_completed = 0
GROUP BY t.id
ORDER BY 
  t.is_paused ASC,
  send_count DESC,
  t.created_at ASC;
```

**2. Get all completed TODOs (sorted by completion date):**
```sql
SELECT 
  t.*,
  COUNT(se.id) as send_count
FROM todos t
LEFT JOIN sent_emails se ON se.todo_id = t.id
WHERE t.is_completed = 1
GROUP BY t.id
ORDER BY t.completed_at DESC;
```

**3. Get TODOs due for sending:**
```sql
SELECT * FROM todos
WHERE next_send_datetime <= ?  -- current timestamp
  AND is_paused = 0
  AND is_completed = 0
ORDER BY next_send_datetime ASC;
```

**4. Get next global send event (for alarm scheduling):**
```sql
SELECT MIN(next_send_datetime) as next_send
FROM todos
WHERE is_paused = 0
  AND is_completed = 0;
```

**5. Get sent email history for a TODO:**
```sql
SELECT * FROM sent_emails
WHERE todo_id = ?
ORDER BY sent_at ASC;
```

**6. Get send count for a TODO:**
```sql
SELECT COUNT(*) as send_count
FROM sent_emails
WHERE todo_id = ?;
```

**7. Statistics - Overall:**
```sql
-- Total emails sent
SELECT COUNT(*) as total_sent FROM sent_emails;

-- Active TODOs
SELECT COUNT(*) as active_count 
FROM todos WHERE is_completed = 0;

-- Completed TODOs
SELECT COUNT(*) as completed_count 
FROM todos WHERE is_completed = 1;

-- Average response time (days)
SELECT AVG((completed_at - created_at) / 86400000.0) as avg_response_days
FROM todos WHERE is_completed = 1;

-- Average sends until response
SELECT AVG(send_count) as avg_sends
FROM (
  SELECT COUNT(se.id) as send_count
  FROM sent_emails se
  JOIN todos t ON se.todo_id = t.id
  WHERE t.is_completed = 1
  GROUP BY se.todo_id
);
```

**8. Statistics - By Recipient:**
```sql
SELECT 
  recipient_email,
  recipient_first_name,
  recipient_last_name,
  COUNT(*) as completed_count,
  AVG((completed_at - created_at) / 86400000.0) as avg_response_days,
  AVG(send_count) as avg_sends
FROM (
  SELECT 
    t.*,
    COUNT(se.id) as send_count
  FROM todos t
  LEFT JOIN sent_emails se ON se.todo_id = t.id
  WHERE t.is_completed = 1
  GROUP BY t.id
)
GROUP BY recipient_email
ORDER BY completed_count DESC;
```

**9. Statistics - Best Templates:**
```sql
SELECT 
  template_index,
  AVG((t.completed_at - se.sent_at) / 86400000.0) as avg_response_days,
  COUNT(*) as usage_count
FROM sent_emails se
JOIN todos t ON se.todo_id = t.id
WHERE t.is_completed = 1
  AND se.sent_at = (
    SELECT MAX(sent_at) 
    FROM sent_emails se2
    WHERE se2.todo_id = se.todo_id
      AND se2.sent_at < t.completed_at
  )
GROUP BY template_index
ORDER BY avg_response_days ASC
LIMIT 10;
```

**10. Statistics - Response Heatmap:**
```sql
SELECT 
  CASE CAST(strftime('%w', completed_at / 1000, 'unixepoch') AS INTEGER)
    WHEN 0 THEN 7  -- Sunday
    WHEN 1 THEN 1  -- Monday
    WHEN 2 THEN 2
    WHEN 3 THEN 3
    WHEN 4 THEN 4
    WHEN 5 THEN 5
    WHEN 6 THEN 6  -- Saturday
  END AS weekday,
  COUNT(*) as count
FROM todos
WHERE is_completed = 1
GROUP BY weekday
ORDER BY weekday;
```

---

### Critical Operations

**1. Create TODO:**
```sql
INSERT INTO todos (
  subject,
  recipient_email,
  recipient_first_name,
  recipient_last_name,
  initial_text,
  language,
  start_date,
  send_time,
  interval_days,
  next_send_datetime,
  selected_subject_indices,
  selected_text_indices,
  already_sent_first,
  is_paused,
  is_completed
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
```

**2. Update TODO (Edit):**
```sql
UPDATE todos SET
  subject = ?,
  recipient_email = ?,
  recipient_first_name = ?,
  recipient_last_name = ?,
  initial_text = ?,
  language = ?,
  send_time = ?,
  interval_days = ?,
  next_send_datetime = ?,
  selected_subject_indices = ?,
  selected_text_indices = ?
WHERE id = ?;
```

**3. Complete TODO:**
```sql
UPDATE todos SET
  is_completed = 1,
  completed_at = ?  -- current timestamp
WHERE id = ?;

-- Trigger automatically sets completed_at
```

**4. Reopen TODO:**
```sql
UPDATE todos SET
  is_completed = 0,
  completed_at = NULL,
  next_send_datetime = ?  -- recalculated
WHERE id = ?;
```

**5. Pause TODO:**
```sql
UPDATE todos SET
  is_paused = 1
WHERE id = ?;
```

**6. Resume TODO:**
```sql
UPDATE todos SET
  is_paused = 0,
  next_send_datetime = ?  -- recalculated
WHERE id = ?;
```

**7. Delete TODO:**
```sql
DELETE FROM todos WHERE id = ?;
-- CASCADE automatically deletes sent_emails
```

**8. Record Sent Email:**
```sql
INSERT INTO sent_emails (
  todo_id,
  subject,
  body,
  sent_at,
  send_number,
  template_index
) VALUES (?, ?, ?, ?, ?, ?);
```

**9. Update next_send_datetime after send:**
```sql
UPDATE todos SET
  next_send_datetime = ?,  -- calculated: current + interval + randomization
  pending_send = 0
WHERE id = ?;
```

**10. Mark TODO as pending (offline):**
```sql
UPDATE todos SET
  pending_send = 1
WHERE id = ?;
```

**11. Get all pending TODOs:**
```sql
SELECT * FROM todos
WHERE pending_send = 1
ORDER BY next_send_datetime ASC;
```

---

## Database Migrations

### Version 1 → Version 2 (Example for future)
```sql
-- Add new field example
ALTER TABLE todos ADD COLUMN priority INTEGER DEFAULT 0;

-- Create new index
CREATE INDEX idx_todos_priority ON todos(priority DESC, created_at ASC);

-- Update version
PRAGMA user_version = 2;
```

### Migration Strategy (Flutter)
```dart
class DatabaseHelper {
  static const int _databaseVersion = 1;
  
  Future<Database> database() async {
    return openDatabase(
      'app.db',
      version: _databaseVersion,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
    );
  }
  
  Future _onCreate(Database db, int version) async {
    // Create all tables
    await db.execute('''CREATE TABLE settings (...) ''');
    await db.execute('''CREATE TABLE todos (...) ''');
    await db.execute('''CREATE TABLE sent_emails (...) ''');
    // Create indices
    // Create triggers
  }
  
  Future _onUpgrade(Database db, int oldVersion, int newVersion) async {
    if (oldVersion < 2) {
      // Migration v1 → v2
      await db.execute('ALTER TABLE todos ADD COLUMN priority INTEGER DEFAULT 0');
    }
    // Future migrations...
  }
}
```

---

## Data Integrity Rules

### Constraints Summary

1. **settings Table:**
   - Only one row allowed (id = 1)
   - max_follow_ups: 1-30
   - randomize_minutes: 0-120
   - smtp_port: 1-65535 (if not NULL)

2. **todos Table:**
   - subject, initial_text: NOT NULL
   - language: 'de' or 'en'
   - interval_days: >= 1
   - Boolean fields: 0 or 1
   - completed_at: NULL if not completed, timestamp if completed

3. **sent_emails Table:**
   - Foreign Key: todo_id → todos.id (CASCADE delete)
   - send_number: >= 1
   - template_index: >= 0

4. **Referential Integrity:**
   - Deleting TODO → Auto-delete all sent_emails
   - Cannot delete settings row (singleton)

---

## Backup & Export Format

### Export JSON Structure
```json
{
  "version": "1.0.0",
  "app": "LetMeDoMyWork",
  "export_date": "2026-01-29T10:30:00Z",
  "device": "Android 14",
  
  "settings": {
    "max_follow_ups": 10,
    "randomize_minutes": 30,
    "smtp_provider": "gmail",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "user@gmail.com",
    "smtp_use_tls": 1,
    "subjects_de": ["...", "..."],
    "subjects_en": ["...", "..."],
    "texts_de": ["...", "..."],
    "texts_en": ["...", "..."],
    "selected_subjects_de": [0,1,2,3,4,5,6,7,8,9],
    "selected_subjects_en": [0,1,2,3,4,5,6,7,8,9],
    "selected_texts_de": [0,1,2,3,4,5,6,7,8,9],
    "selected_texts_en": [0,1,2,3,4,5,6,7,8,9]
  },
  
  "todos": [
    {
      "id": 1,
      "subject": "Project Update",
      "recipient_email": "john.doe@example.com",
      "recipient_first_name": "John",
      "recipient_last_name": "Doe",
      "initial_text": "Hi John, ...",
      "language": "en",
      "start_date": 1738108800000,
      "send_time": "09:00",
      "interval_days": 1,
      "next_send_datetime": 1738144600000,
      "selected_subject_indices": [0,1,2,3,4,5,6,7,8,9],
      "selected_text_indices": [0,1,2,3,4,5,6,7,8,9],
      "already_sent_first": 0,
      "is_paused": 0,
      "is_completed": 0,
      "pending_send": 0,
      "created_at": 1738108800000,
      "completed_at": null
    }
  ],
  
  "sent_emails": [
    {
      "id": 1,
      "todo_id": 1,
      "subject": "Follow-Up: Project Update",
      "body": "Hallo John, ...",
      "sent_at": 1738231200000,
      "send_number": 1,
      "template_index": 0
    }
  ]
}
```

**Notes:**
- SMTP password is NOT exported (security)
- All timestamps in UNIX milliseconds (UTC)
- JSON arrays stored as-is (no conversion needed)

---

## Performance Optimization

### Index Strategy

**Critical Indices (already defined):**
1. `idx_todos_next_send` - Finding due TODOs (used every alarm trigger)
2. `idx_todos_completed` - Completed tab query
3. `idx_sent_emails_todo` - Email history per TODO
4. `idx_todos_recipient` - Statistics by recipient

**Index Usage Examples:**
```sql
-- Uses idx_todos_next_send
EXPLAIN QUERY PLAN
SELECT * FROM todos 
WHERE next_send_datetime <= ? AND is_paused = 0 AND is_completed = 0;
-- Expected: SEARCH TABLE todos USING INDEX idx_todos_next_send

-- Uses idx_sent_emails_todo
EXPLAIN QUERY PLAN
SELECT * FROM sent_emails WHERE todo_id = ? ORDER BY sent_at DESC;
-- Expected: SEARCH TABLE sent_emails USING INDEX idx_sent_emails_todo
```

### Query Optimization Tips

1. **Always use indices for WHERE clauses**
   - Filter by indexed columns first
   - Use composite indices for multi-column filters

2. **Limit result sets**
   - Use LIMIT for large tables
   - Paginate TODO lists if > 100 items

3. **Avoid SELECT ***
   - Select only needed columns
   - Reduces memory and I/O

4. **Use transactions for batch operations**
   - Import: Single transaction for all inserts
   - Delete multiple TODOs: Single transaction

5. **Analyze query plans**
   - Use EXPLAIN QUERY PLAN during development
   - Ensure indices are used

---

## Database Maintenance

### Vacuum (Reclaim Space)
```sql
-- Run periodically (e.g., after large deletes)
VACUUM;
```

**When to run:**
- After deleting many TODOs
- After import (replaces all data)
- Monthly maintenance

### Analyze (Update Statistics)
```sql
-- Update query planner statistics
ANALYZE;
```

**When to run:**
- After significant data changes
- After adding/removing indices
- Monthly maintenance

### Integrity Check
```sql
-- Check database integrity
PRAGMA integrity_check;
-- Expected result: "ok"

-- Quick check (faster)
PRAGMA quick_check;
```

**When to run:**
- On app startup (first launch after update)
- After app crash
- Before backup/export

---

## Security Considerations

### What's Stored in SQLite

**Unencrypted (in SQLite):**
- All TODO data (subjects, emails, texts)
- All sent email history
- Template libraries
- SMTP username (email address)

**NOT Stored in SQLite:**
- SMTP password (in flutter_secure_storage)

### Why No SQLite Encryption?

1. **Android Sandbox Protection:**
   - DB file only accessible by app
   - Protected by Android OS permissions

2. **Performance:**
   - Encryption adds overhead
   - Not critical for this use case

3. **User Responsibility:**
   - Exports are user's responsibility
   - Warning shown on export

### SMTP Password Security

**Storage Location:** flutter_secure_storage
- **iOS:** Keychain (hardware-backed)
- **Android:** EncryptedSharedPreferences + KeyStore

**Access:**
```dart
// Write
await secureStorage.write(
  key: 'smtp_password',
  value: encryptedPassword
);

// Read
String? encryptedPassword = await secureStorage.read(
  key: 'smtp_password'
);
```

**On Device Reset:**
- Secure storage cleared
- User must re-enter password
- (This is intentional - security feature)

---

## Testing Considerations

### Test Data Sets

**Minimal (for unit tests):**
```sql
-- 1 settings row
-- 3 todos (1 active, 1 paused, 1 completed)
-- 5 sent_emails (distributed across todos)
```

**Medium (for integration tests):**
```sql
-- 1 settings row
-- 20 todos (mix of states)
-- 50 sent_emails
```

**Large (for stress testing):**
```sql
-- 1 settings row
-- 500 todos
-- 2000 sent_emails
```

### Common Test Scenarios

1. **Create TODO:**
   - Insert, verify ID returned
   - Verify all fields stored correctly
   - Verify JSON arrays parseable

2. **Send Email:**
   - Insert sent_email
   - Update todo.next_send_datetime
   - Verify send_count increments

3. **Complete TODO:**
   - Update is_completed = 1
   - Verify completed_at auto-set (trigger)
   - Verify appears in Completed tab query

4. **Delete TODO:**
   - Verify CASCADE deletes sent_emails
   - Verify no orphan sent_emails

5. **Export/Import:**
   - Export to JSON
   - Clear DB
   - Import from JSON
   - Verify data identical

---

## Database File Size Estimates

### Expected Sizes

**Settings:**
- 1 row ≈ 50 KB (with 30 templates each)

**TODOs:**
- Average TODO ≈ 2 KB
- 100 TODOs ≈ 200 KB
- 500 TODOs ≈ 1 MB

**Sent Emails:**
- Average email ≈ 1 KB
- 500 emails ≈ 500 KB
- 2000 emails ≈ 2 MB

**Total Database (500 TODOs + 2000 emails):**
- ≈ 3-4 MB (uncompressed)
- ≈ 1-2 MB (compressed for export)

**Worst Case (max usage):**
- 1000 TODOs + 10,000 emails ≈ 12 MB

**Conclusion:** Database will easily stay under 10 MB export limit for most users.

---

## Flutter Implementation Example

### Database Helper Class
```dart
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static const String _databaseName = 'letmedomywork.db';
  static const int _databaseVersion = 1;
  
  static Database? _database;
  
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }
  
  Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, _databaseName);
    
    return await openDatabase(
      path,
      version: _databaseVersion,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
    );
  }
  
  Future<void> _onCreate(Database db, int version) async {
    // Create settings table
    await db.execute('''
      CREATE TABLE settings (
        id INTEGER PRIMARY KEY CHECK(id = 1),
        max_follow_ups INTEGER NOT NULL DEFAULT 10,
        randomize_minutes INTEGER NOT NULL DEFAULT 30,
        smtp_provider TEXT,
        smtp_host TEXT,
        smtp_port INTEGER,
        smtp_username TEXT,
        smtp_use_tls INTEGER NOT NULL DEFAULT 1,
        smtp_password_encrypted TEXT DEFAULT '[ENCRYPTED]',
        subjects_de TEXT NOT NULL,
        subjects_en TEXT NOT NULL,
        texts_de TEXT NOT NULL,
        texts_en TEXT NOT NULL,
        selected_subjects_de TEXT NOT NULL,
        selected_subjects_en TEXT NOT NULL,
        selected_texts_de TEXT NOT NULL,
        selected_texts_en TEXT NOT NULL,
        last_opened INTEGER NOT NULL,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
        updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000)
      )
    ''');
    
    // Create todos table
    await db.execute('''
      CREATE TABLE todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        recipient_email TEXT NOT NULL,
        recipient_first_name TEXT,
        recipient_last_name TEXT,
        initial_text TEXT NOT NULL,
        language TEXT NOT NULL CHECK(language IN ('de', 'en')),
        start_date INTEGER NOT NULL,
        send_time TEXT NOT NULL,
        interval_days INTEGER NOT NULL CHECK(interval_days >= 1),
        next_send_datetime INTEGER NOT NULL,
        selected_subject_indices TEXT NOT NULL,
        selected_text_indices TEXT NOT NULL,
        already_sent_first INTEGER NOT NULL DEFAULT 0,
        is_paused INTEGER NOT NULL DEFAULT 0,
        is_completed INTEGER NOT NULL DEFAULT 0,
        pending_send INTEGER NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
        completed_at INTEGER
      )
    ''');
    
    // Create sent_emails table
    await db.execute('''
      CREATE TABLE sent_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        todo_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        sent_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now') * 1000),
        send_number INTEGER NOT NULL,
        template_index INTEGER NOT NULL,
        FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE
      )
    ''');
    
    // Create indices
    await db.execute('CREATE INDEX idx_todos_next_send ON todos(next_send_datetime, is_paused, is_completed)');
    await db.execute('CREATE INDEX idx_todos_completed ON todos(is_completed, completed_at DESC)');
    await db.execute('CREATE INDEX idx_sent_emails_todo ON sent_emails(todo_id, sent_at DESC)');
    // ... more indices
    
    // Create triggers
    await db.execute('''
      CREATE TRIGGER todos_completed
      AFTER UPDATE OF is_completed ON todos
      WHEN NEW.is_completed = 1 AND OLD.is_completed = 0
      BEGIN
        UPDATE todos SET completed_at = strftime('%s', 'now') * 1000 WHERE id = NEW.id;
      END
    ''');
    // ... more triggers
    
    // Insert default settings
    await _insertDefaultSettings(db);
  }
  
  Future<void> _onUpgrade(Database db, int oldVersion, int newVersion) async {
    // Future migrations here
  }
  
  Future<void> _insertDefaultSettings(Database db) async {
    // Load default templates (from assets or hardcoded)
    final defaultSubjectsDe = [...]; // 30 subjects
    final defaultSubjectsEn = [...];
    final defaultTextsDe = [...];
    final defaultTextsEn = [...];
    
    await db.insert('settings', {
      'id': 1,
      'max_follow_ups': 10,
      'randomize_minutes': 30,
      'subjects_de': jsonEncode(defaultSubjectsDe),
      'subjects_en': jsonEncode(defaultSubjectsEn),
      'texts_de': jsonEncode(defaultTextsDe),
      'texts_en': jsonEncode(defaultTextsEn),
      'selected_subjects_de': '[0,1,2,3,4,5,6,7,8,9]',
      'selected_subjects_en': '[0,1,2,3,4,5,6,7,8,9]',
      'selected_texts_de': '[0,1,2,3,4,5,6,7,8,9]',
      'selected_texts_en': '[0,1,2,3,4,5,6,7,8,9]',
      'last_opened': DateTime.now().millisecondsSinceEpoch,
    });
  }
}
```

---

**Ende DatabaseSchema.md**