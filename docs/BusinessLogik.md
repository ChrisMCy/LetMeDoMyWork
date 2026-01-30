# LetMeDoMyWork - Business Logic Specification

## Overview
Automatisierte Follow-Up Email Reminder App mit menschlich wirkenden Texten für Android.

---

## Core Entities

### TODO Entry
Ein TODO repräsentiert eine Email-Kampagne mit Initial-Mail und automatischen Follow-Ups.

**Eigenschaften:**
- `id`: Unique identifier
- `subject`: Email Subject
- `recipient_email`: Empfänger Email-Adresse
- `recipient_first_name`: Vorname (auto-parsed oder manuell)
- `recipient_last_name`: Nachname (auto-parsed oder manuell)
- `initial_text`: Text der Initial-Mail (wird in Follow-Ups referenziert via Platzhalter)
- `language`: 'de' oder 'en' (bestimmt welche Templates verwendet werden)
- `start_date`: Datum ab wann gesendet werden soll
- `send_time`: Uhrzeit im Format HH:MM (z.B. "09:00", Default: "09:00")
- `interval_days`: Alle X Tage senden (z.B. 1 = täglich, 3 = alle 3 Tage)
- `next_send_datetime`: Berechneter nächster Sendezeitpunkt (inkl. Randomisierung)
- `already_sent_first`: Boolean - wurde Initial-Mail schon gesendet?
- `is_paused`: Boolean - ist TODO pausiert?
- `is_completed`: Boolean - ist TODO abgeschlossen?
- `created_at`: Erstellungsdatum
- `completed_at`: Abschlussdatum (null wenn nicht completed)
- `selected_subject_indices`: JSON Array mit Indices der gewählten Subjects [0,1,2,...]
- `selected_text_indices`: JSON Array mit Indices der gewählten Texte [0,1,2,...]

---

## Email Sending Logic

### Send Time Calculation
```
Basis-Sendezeit = start_date + send_time
Randomisierung = random(0, max_random_minutes) - (max_random_minutes / 2)
Tatsächliche Sendezeit = Basis-Sendezeit + Randomisierung

Beispiel:
- Konfiguriert: 09:00 Uhr
- max_random_minutes = 30
- Random-Wert: 18 Minuten
- Offset: 18 - 15 = +3 Minuten
- Tatsächlich: 09:03 Uhr
```

### Next Send Calculation
```
Wenn TODO erstellt wird:
  - Wenn "already_sent_first" = true:
      next_send = start_date + interval_days + randomized_send_time
      send_count startet bei 1 (erste Mail als gesendet markiert)
  - Wenn "already_sent_first" = false:
      next_send = start_date + randomized_send_time
      send_count startet bei 0

Nach jedem Send:
  next_send = aktuelles_datum + interval_days + randomized_send_time

Wenn TODO resumed wird (nach Pause):
  next_send = current_date + interval_days + randomized_send_time

Wenn TODO reopened wird (aus Completed):
  next_send = current_date + interval_days + randomized_send_time

Wenn Interval geändert wird:
  next_send = current_date + neuer_interval + randomized_send_time
```

### Email Template Selection
```
Aktuelle Sende-Nummer berechnen:
  send_count = Anzahl Einträge in sent_emails für dieses TODO

Wenn "already_sent_first" = true:
  template_index = send_count  // Skip Index 0, starte bei 1
Sonst:
  template_index = send_count  // Starte bei 0

Subject auswählen:
  - Wenn template_index < Länge von selected_subject_indices:
      Verwende selected_subject_indices[template_index]
  - Sonst:
      Verwende selected_subject_indices[letzter Index]

Text auswählen:
  - Wenn template_index < Länge von selected_text_indices:
      Verwende selected_text_indices[template_index]
  - Sonst:
      Verwende selected_text_indices[letzter Index]

Beispiel (already_sent_first = true, 10 Templates):
  - send_count = 0 → verwendet Template Index 1 (zweites Template)
  - send_count = 1 → verwendet Template Index 2 (drittes Template)
  - send_count = 9 → verwendet Template Index 10 (letztes Template)
  - send_count = 10+ → verwendet Template Index 10 (letztes Template, wiederholt)
```

### Placeholder Replacement
Alle Subjects und Texte können folgende Platzhalter enthalten:

- `{Vorname}` → recipient_first_name
- `{Nachname}` → recipient_last_name
- `{DateToday}` → Aktuelles Datum im Format DD.MM.YYYY
- `{DateLastMail}` → Datum der letzten gesendeten Mail (DD.MM.YYYY)
- `{InitialSubject}` → subject des TODOs
- `{DaysSinceLastMail}` → Anzahl Tage seit letzter Mail (Integer)
- `{InitialText}` → initial_text des TODOs (kompletter Text)

**Replacement-Prozess:**
1. Hole Template-String (Subject oder Text)
2. Ersetze alle Platzhalter mit aktuellen Werten
3. Wenn Platzhalter-Wert nicht vorhanden → ersetze mit leerem String
4. Resultat = finaler Email-Subject/Body

**Wichtig:** 
- `{InitialText}` Platzhalter ist verfügbar, wird aber NICHT automatisch in Default-Templates verwendet
- User kann eigene Templates mit `{InitialText}` erstellen wenn gewünscht
- Default-Templates referenzieren Initial-Mail nur indirekt via {InitialSubject} und {DateLastMail}

---

## SMTP Email Send Process

### Email Senden (Kompletter Ablauf)
```
Voraussetzungen:
- TODO ist nicht pausiert
- TODO ist nicht completed
- next_send_datetime <= current_datetime
- SMTP Settings sind konfiguriert

Prozess:
1. Lade TODO aus DB
2. Lade Settings aus DB
3. Lade letzten sent_email Eintrag (für {DateLastMail} Platzhalter)

4. Berechne Template Index:
   send_count = COUNT(sent_emails WHERE todo_id = X)
   template_index = send_count (oder send_count + 1 wenn already_sent_first)

5. Hole Subject Template:
   - Basierend auf language: subjects_de oder subjects_en
   - Index aus selected_subject_indices[template_index]
   - Falls template_index >= Länge: nimm letzten

6. Hole Text Template:
   - Basierend auf language: texts_de oder texts_en  
   - Index aus selected_text_indices[template_index]
   - Falls template_index >= Länge: nimm letzten

7. Replace Platzhalter:
   final_subject = replacePlaceholders(subject_template, todo, last_email)
   final_body = replacePlaceholders(text_template, todo, last_email)

8. Erstelle Email Message:
   - From: settings.smtp_username
   - To: todo.recipient_email
   - Subject: final_subject
   - Body: final_body
   - Content-Type: text/plain; charset=utf-8

9. SMTP Verbindung:
   - Host: settings.smtp_host
   - Port: settings.smtp_port
   - Security: STARTTLS (außer Custom mit deaktiviert)
   - Username: settings.smtp_username
   - Password: decrypt(settings.smtp_password_hash, settings.smtp_salt)

10. Sende Email via SMTP

11. Bei ERFOLG:
    a. Erstelle sent_email Eintrag:
       - todo_id = todo.id
       - subject = final_subject
       - body = final_body
       - sent_at = current_datetime
       - send_number = send_count + 1
    
    b. Berechne next_send_datetime:
       next_send = current_date + interval_days + randomized_send_time
    
    c. Update TODO in DB (next_send_datetime)
    
    d. Zeige Push Notification:
       Title: "LetMeDoMyWork"
       Body: "Email sent to {first_name} {last_name}" 
             (oder "Email sent to {email}" wenn Namen leer)
    
    e. Berechne nächstes globales Send-Event neu
    f. Update Background Alarms

12. Bei FEHLER:
    a. Log Error (timestamp, todo_id, error_message)
    
    b. Zeige Error Notification:
       Title: "LetMeDoMyWork - Send Failed"
       Body: "Failed to send email to {recipient_email}. Tap to retry."
       Action: Tap → Öffne TODO Detail
    
    c. Markiere TODO visuell (roter Rahmen um Eintrag)
    
    d. next_send_datetime bleibt UNVERÄNDERT
    
    e. User kann manuell retry via Manual Send Button
```

---

## Background Service Logic

### Wake-Up Strategy (Intelligentes Dual-Alarm System)
**Ziel:** Maximale Präzision + Fallback-Sicherheit
```
Bei jedem TODO Create/Update/Send/Resume/Interval-Change:
  1. Finde nächstes globales Send-Event:
     min_next_send = MIN(next_send_datetime) 
     FROM todos 
     WHERE is_paused = false AND is_completed = false
  
  2. Setze Exact Alarm:
     AlarmManager.setExactAndAllowWhileIdle(
       triggerAtMillis: min_next_send.toMillis(),
       operation: SendEmailPendingIntent
     )
  
  3. Setze Backup Alarm (Fallback):
     AlarmManager.setExactAndAllowWhileIdle(
       triggerAtMillis: now + 15 Minuten,
       operation: CheckPendingTODOsPendingIntent
     )

Beim Alarm-Trigger (beide Typen):
  1. Wake Lock aquirieren (max 30 Sekunden)
  
  2. Prüfe alle TODOs:
     SELECT * FROM todos 
     WHERE next_send_datetime <= current_datetime
       AND is_paused = false 
       AND is_completed = false
  
  3. Für jeden fälligen TODO:
     - Führe SMTP Email Send Process aus
     - Update next_send_datetime
  
  4. Berechne nächstes globales Send-Event neu
  
  5. Setze neue Alarme (Exact + Backup)
  
  6. Release Wake Lock
```

### Offline Handling
```
Beim Alarm-Trigger:
  IF (Gerät offline):
    - Markiere alle fälligen TODOs als "pending_send"
    - Registriere ConnectivityManager Listener
  
Beim ConnectivityChange zu "Online":
  1. Hole alle TODOs mit "pending_send"
  2. Sende alle sofort (ohne Randomisierung)
  3. Entferne "pending_send" Flag
  4. Update next_send_datetime normal
  5. Setze Alarme neu

Technisch:
  - "pending_send" = neues Boolean Feld in todos Table
  - ConnectivityManager.NetworkCallback für Online-Detection
```

### 7-Tage Inaktivitäts-Check
```
Bei JEDEM App-Start (onCreate von MainActivity):
  1. Lade settings.last_opened aus DB
  
  2. Berechne Differenz:
     days_since_opened = (current_date - last_opened).days
  
  3. IF (days_since_opened >= 7):
     a. UPDATE todos SET is_paused = true 
        WHERE is_completed = false
     
     b. Zeige Notification:
        Title: "LetMeDoMyWork"
        Body: "App was inactive for 7 days. All TODOs have been paused."
        Action: Tap → Öffne App
     
     c. Zeige In-App Dialog:
        "Your app was inactive for 7 days.
         All active TODOs have been paused automatically.
         
         Would you like to resume them?
         [Resume All]  [Keep Paused]"
     
     Bei "Resume All":
       - UPDATE todos SET is_paused = false, 
                         next_send_datetime = <neu berechnet>
       - Setze Alarme neu
  
  4. Update settings.last_opened = current_date
```

---

## Email Parsing Logic

### Auto-Extract First/Last Name from Email
```
Input: recipient_email (z.B. "john.doe@example.com")

Algorithmus:
1. Split Email bei '@' → nehme local-part ("john.doe")

2. Definiere Trennzeichen: ['.', '-', '_', ',']

3. Suche erstes Trennzeichen in local-part:
   - Wenn gefunden:
       parts = local-part.split(trennzeichen, limit=2)
       first_name = capitalize(parts[0])
       last_name = capitalize(parts[1]) wenn parts.length > 1, sonst ""
   
   - Wenn nicht gefunden:
       first_name = capitalize(local-part)
       last_name = ""

4. Return (first_name, last_name)

Beispiele:
- "john.doe@mail.com" → ("John", "Doe")
- "jane-smith@mail.com" → ("Jane", "Smith")
- "max_mueller@mail.com" → ("Max", "Mueller")
- "user@mail.com" → ("User", "")
- "first.middle.last@mail.com" → ("First", "Middle.last")  // nur erstes Trennzeichen

Capitalize Funktion:
  - Erster Buchstabe uppercase
  - Rest lowercase
  - "john" → "John"
```

**Wichtig:** User kann Namen nachträglich:
- Manuell bearbeiten
- Mit Swap-Button (⇄) tauschen
```
  onClick Swap Button:
    temp = first_name
    first_name = last_name
    last_name = temp
    update UI
```

---

## TODO List Sorting & Filtering

### Active Tab
**Sortierung (Multi-Level):**
```sql
SELECT * FROM todos 
WHERE is_completed = false
ORDER BY 
  is_paused ASC,           -- Pausierte ans Ende (0 vor 1)
  (SELECT COUNT(*) 
   FROM sent_emails 
   WHERE todo_id = todos.id) DESC,  -- Meiste Sends zuerst
  created_at ASC           -- Bei gleicher Send-Anzahl: Älteste zuerst
```

**Färbung (White → Red Gradient):**
```
Für jeden TODO in der Liste:
  send_count = COUNT(sent_emails WHERE todo_id = X)
  max_sends = settings.max_follow_ups
  
  color_intensity = min(send_count / max_sends, 1.0)  // Cap bei 1.0
  
  // RGB Interpolation
  R = 255
  G = 255 * (1 - color_intensity)
  B = 255 * (1 - color_intensity)
  
  text_color = RGB(R, G, B)

Beispiele (max_sends = 10):
  send_count = 0  → RGB(255, 255, 255) = Weiß
  send_count = 3  → RGB(255, 178, 178) = Hellrot
  send_count = 6  → RGB(255, 102, 102) = Mittelrot
  send_count = 10 → RGB(255, 0, 0) = Vollrot
  send_count = 15 → RGB(255, 0, 0) = Vollrot (capped)
```

**Visuelle Darstellung pro TODO-Eintrag:**
```
┌──────────────────────────────────────────────────┐
│ [⏸️] Subject Name                      (3/10)   │  ← Wenn pausiert: Icon + grauer BG
│     recipient@email.com                          │
│     Last: 29.01.2026 | Next: 31.01.2026    [📤] │  ← Manual Send Button
└──────────────────────────────────────────────────┘

Elemente:
- [⏸️]: Nur wenn is_paused = true
- Subject Name: Gefärbt basierend auf send_count
- (3/10): send_count / max_sends, rechtsbündig neben Subject
- recipient@email.com: Immer volle Email
- Last: Letztes sent_at (oder "Never" wenn send_count = 0)
- Next: next_send_datetime formatiert
- [📤]: Send-Icon Button für manuelles Senden
- Ganzer Hintergrund: Grau (#EEEEEE) wenn pausiert, weiß sonst
```

### Completed Tab
**Sortierung:**
```sql
SELECT * FROM todos 
WHERE is_completed = true
ORDER BY completed_at DESC  -- Neueste Completions zuerst
```

**Visuelle Darstellung:**
```
┌──────────────────────────────────────────────────┐
│ ✓ Subject Name                         (5/10)   │
│   recipient@email.com                            │
│   Completed: 28.01.2026                          │
└──────────────────────────────────────────────────┘

Elemente:
- ✓: Checkmark Icon
- Text: Grau (#9E9E9E)
- Kein Send-Button
- Completed-Datum statt Last/Next
```

---

## User Actions & Effects

### Create TODO Screen

**UI-Reihenfolge (Top → Bottom):**
```
1. Language Toggle
   [DE] [EN]  ← Zwei Toggle Buttons, einer aktiv
   Default: DE

2. Subject
   [________________________________]

3. Recipient Email
   [________________________________]
   (onChange → auto-parse Namen)

4. First Name    [⇄]    Last Name
   [___________]  ↔️   [___________]
   (Swap-Button in der Mitte)

5. Start Date
   [📅 29.01.2026]  ← Date Picker

6. Send Time
   [🕐 09:00]  ← Time Picker, Default 09:00

7. Interval (days)
   [___] days  ← Number Input, min=1

8. ☐ Already sent first email
   Checkbox, default unchecked

9. Initial Email Text
   [                                    ]
   [                                    ]
   [____________________________________]
   (Multi-line Text Input)

10. ───── Follow-Up Subjects (10) ─────
    Label: "First subject will be used for 1st send"
    
    1. [Follow-Up: {InitialSubject}        ] [🔄]
    2. [Nochmal bzgl.: {InitialSubject}    ] [🔄]
    3. ...
    10. [Letzte Chance: {InitialSubject}   ] [🔄]
    
    Reload Button (🔄) Logic:
      - Zeigt aktuell gewähltes Template
      - Bei Click: Wähle zufälliges anderes Template aus verfügbaren
      - Verfügbare = alle 30 Templates minus bereits verwendete

11. ───── Follow-Up Texts (10) ─────
    Label: "First text will be used for 1st send"
    
    1. [Hallo {Vorname}, ich wollte...    ] [🔄]
    2. [Hi {Vorname}, nur eine kurze...   ] [🔄]
    3. ...
    10. [ÄUSSERST DRINGEND - Dies ist...  ] [🔄]
    
    (Gleiche Reload-Logic wie Subjects)

12. Buttons
    [Cancel]  [Save TODO]
```

**Reload Button (🔄) Detailed Logic:**
```
State:
  selected_indices = [0, 1, 5, 7, ...]  // Aktuell gewählte Template-Indices
  all_indices = [0..29]  // Alle verfügbaren Template-Indices

Beim Click auf Reload bei Position P:
  1. current_index = selected_indices[P]
  
  2. available_indices = all_indices - selected_indices + [current_index]
     // Alle außer bereits verwendete, aber inkl. aktuellem (zum Re-Roll)
  
  3. IF (available_indices.length <= 1):
       // Alle Templates bereits verwendet
       Zeige Toast: "All templates in use. Add more in Settings."
       Return
  
  4. available_for_random = available_indices - [current_index]
     // Entferne aktuellen, damit ein anderer gewählt wird
  
  5. new_index = random_choice(available_for_random)
  
  6. selected_indices[P] = new_index
  
  7. Update UI (zeige neues Template)
```

**Language Toggle Behavior:**
```
Beim Wechsel DE ↔ EN:
  1. Lade entsprechende Templates aus Settings:
     - DE: settings.subjects_de, settings.texts_de
     - EN: settings.subjects_en, settings.texts_en
  
  2. Reset selected_indices zu Default:
     - selected_subject_indices = settings.selected_subjects_de (oder _en)
     - selected_text_indices = settings.selected_texts_de (oder _en)
  
  3. Update UI (zeige neue Templates)
  
  4. Platzhalter bleiben gleich ({Vorname} in DE, {Vorname} in EN)
```

**"Already Sent First Email" Checkbox Behavior:**
```
Wenn gechecked:
  - Label-Änderung bei Follow-Ups:
    "First subject/text will be SKIPPED (used for 2nd send)"
  
  - Visueller Hinweis:
    Template 1 bekommt durchgestrichenen Text oder "SKIPPED" Label
  
  - Bei Save:
    send_count wird auf 1 gesetzt (nicht 0)
    next_send_datetime = start_date + interval_days + randomized_time
  
  - Beim nächsten Send:
    Template Index startet bei 1 (nicht 0)

Wenn unchecked (default):
  - Normal: Erste Mail wird gesendet
  - send_count = 0
  - next_send_datetime = start_date + randomized_time
```

**Validierung beim Save:**
```
Required Fields:
- Subject: nicht leer
- Recipient Email: valid email format (regex: ^[^@]+@[^@]+\.[^@]+$)
- Start Date: >= current_date
- Send Time: valid HH:MM (00:00 - 23:59)
- Interval: integer >= 1
- Initial Text: nicht leer
- Language: ausgewählt (DE oder EN)

Bei Validierungsfehler:
  - Highlight fehlerhafte Felder in rot
  - Zeige Error Message unter Feld
  - Scroll zu erstem Fehler
  - Verhindere Save
```

---

### Edit TODO Screen

**Zusätzlich zu Create-Feldern:**
```
Ganz oben (vor Language Toggle):

───── Sent Email History (Read-Only) ─────
1. 25.01.2026 09:15 - Follow-Up: Project Update
2. 27.01.2026 09:08 - Nochmal bzgl.: Project Update  
3. 29.01.2026 09:23 - Kurze Erinnerung: Project Update

───────────────────────────────────────────

(Dann folgen editierbare Felder wie in Create)
```

**Edit-Logik:**
```
Was kann geändert werden:
  ✅ Subject
  ✅ Recipient Email (+ Namen)
  ✅ Language (wechselt Templates)
  ✅ Start Date (nur Anzeige, beeinflusst nichts mehr)
  ✅ Send Time (beeinflusst nächsten Send)
  ✅ Interval (triggers next_send Neuberechnung)
  ✅ Already Sent First (nur Anzeige-Zweck)
  ✅ Initial Text
  ✅ Follow-Up Subjects (zukünftige Sends)
  ✅ Follow-Up Texts (zukünftige Sends)

Was NICHT geändert wird:
  ❌ Sent Email History (read-only, DB-gespeichert)
  ❌ send_count (automatisch aus DB berechnet)
  ❌ created_at

Bei Interval-Änderung:
  IF (next_send_datetime in Zukunft):
    next_send = current_date + neuer_interval + randomized_time
  ELSE:
    // Überfälliger Send bleibt überfällig
    next_send = current_datetime (sofort fällig)
  
  Update Background Alarms
```

---

### Manual Send (📤 Button)

**UI Flow:**
```
1. User klickt Send-Button im TODO-Eintrag

2. Zeige Confirmation Dialog:
   ┌────────────────────────────────────────┐
   │ Send Next Reminder Now?                │
   │                                        │
   │ This will send the next follow-up     │
   │ email to {recipient_email}            │
   │ immediately.                           │
   │                                        │
   │        [Cancel]  [Send Now]            │
   └────────────────────────────────────────┘

3a. Bei "Cancel":
    - Dialog schließen
    - Keine Aktion

3b. Bei "Send Now":
    - Dialog schließen
    - Zeige Loading Indicator auf TODO-Eintrag
    - Führe SMTP Email Send Process aus (OHNE Randomisierung)
    - Berechne next_send = current_datetime + interval_days + randomized_time
    - Bei Erfolg:
        * Zeige Success Toast: "Email sent!"
        * Update TODO-Eintrag Anzeige (Last/Next Dates)
        * Zeige Push Notification
    - Bei Fehler:
        * Zeige Error Dialog mit Fehlerdetails
        * "Retry" Button im Dialog
        * Roter Rahmen um TODO-Eintrag
```

---

### Complete TODO

**Swipe Right auf Active Tab:**
```
1. User swipet TODO nach rechts

2. Animation: Eintrag gleitet nach rechts raus

3. Setze in DB:
   - is_completed = true
   - completed_at = current_datetime

4. Entferne aus Active Tab Liste

5. Füge zu Completed Tab hinzu (an Position basierend auf completed_at)

6. Zeige Undo Snackbar am unteren Bildschirmrand:
   ┌─────────────────────────────────────────┐
   │ TODO completed       [UNDO]             │
   └─────────────────────────────────────────┘
   
   Timer: 5 Sekunden

7a. Wenn User auf [UNDO] klickt (innerhalb 5 Sek):
    - Setze is_completed = false
    - Setze completed_at = null
    - Entferne aus Completed Tab
    - Füge zurück zu Active Tab (an ursprünglicher Position)
    - Schließe Snackbar
    - Zeige Toast: "TODO restored"

7b. Wenn 5 Sekunden ablaufen ohne UNDO:
    - Snackbar verschwindet
    - Aktion ist final
    - Background Alarm wird neu berechnet (ohne dieses TODO)
```

---

### Pause/Resume TODO

**Swipe Left auf Active Tab:**
```
1. User swipet TODO nach links

2. Prüfe aktuellen Zustand:
   
   Fall A: is_paused = false (TODO ist aktiv)
     → PAUSE Aktion:
       a. Setze is_paused = true
       b. UI-Update:
          - Füge Stoppuhr-Icon (⏸️) vor Subject hinzu
          - Ändere Hintergrund zu grau (#EEEEEE)
          - Verschiebe Eintrag ans Ende der Liste
       c. Entferne aus Background Alarm Calculation
       d. Zeige Toast: "TODO paused"
   
   Fall B: is_paused = true (TODO ist pausiert)
     → RESUME Aktion:
       a. Setze is_paused = false
       b. Berechne next_send_datetime:
          next_send = current_date + interval_days + randomized_time
       c. UI-Update:
          - Entferne Stoppuhr-Icon
          - Ändere Hintergrund zu weiß
          - Verschiebe Eintrag basierend auf send_count (re-sort)
       d. Setze Background Alarm neu
       e. Zeige Toast: "TODO resumed"

3. Swipe-Animation zurück zur Ursprungsposition
```

---

### Reopen TODO

**Swipe Left auf Completed Tab:**
```
1. User swipet completed TODO nach links

2. Zeige Confirmation Dialog:
   ┌────────────────────────────────────────┐
   │ Reopen this TODO?                      │
   │                                        │
   │ Subject: {subject}                     │
   │ Recipient: {email}                     │
   │                                        │
   │ Next send will be scheduled for:      │
   │ {current_date + interval + time}      │
   │                                        │
   │        [Cancel]  [Reopen]              │
   └────────────────────────────────────────┘

3a. Bei "Cancel":
    - Dialog schließen
    - Swipe-Animation zurück

3b. Bei "Reopen":
    - Setze in DB:
        is_completed = false
        completed_at = null
        next_send_datetime = current_date + interval_days + randomized_time
    
    - Entferne aus Completed Tab
    
    - Füge zu Active Tab hinzu (Position basierend auf send_count)
    
    - Setze Background Alarm neu
    
    - Zeige Toast: "TODO reopened. Next send: {next_send_datetime}"
```

---

### Delete TODO

**Long Press → Options Menu → Delete:**
```
1. User long-presst auf TODO-Eintrag

2. Zeige Context Menu:
   ┌────────────────────────┐
   │ Edit                   │
   │ Delete                 │  ← Rot eingefärbt
   │ (Pause/Resume)         │  ← Je nach Zustand
   │ (Complete)             │  ← Nur bei Active
   │ Cancel                 │
   └────────────────────────┘

3. Bei "Delete" Click:
   Zeige Confirmation Dialog:
   ┌────────────────────────────────────────┐
   │ ⚠️ Delete TODO?                        │
   │                                        │
   │ This will permanently delete:         │
   │ • TODO: {subject}                     │
   │ • All {count} sent email records      │
   │                                        │
   │ This action cannot be undone.         │
   │                                        │
   │        [Cancel]  [Delete]              │  ← Delete in rot
   └────────────────────────────────────────┘

4a. Bei "Cancel":
    - Dialog schließen
    - Keine Aktion

4b. Bei "Delete":
    - DELETE FROM sent_emails WHERE todo_id = X  (CASCADE)
    - DELETE FROM todos WHERE id = X
    - Entferne aus UI-Liste (Animation: Fade out)
    - Setze Background Alarm neu
    - Zeige Toast: "TODO deleted"
```

---

## Settings Management

### First App Launch Setup
```
Beim allerersten App-Start:
  1. Prüfe: SELECT COUNT(*) FROM settings
  
  2. IF (count = 0):  // Erste Installation
     
     a. Initialisiere Default Settings:
        INSERT INTO settings (
          max_follow_ups = 10,
          randomize_minutes = 30,
          
          subjects_de = [30 Default-Subjects DE],
          subjects_en = [30 Default-Subjects EN],
          texts_de = [30 Default-Texts DE],
          texts_en = [30 Default-Texts EN],
          
          selected_subjects_de = [0,1,2,3,4,5,6,7,8,9],
          selected_subjects_en = [0,1,2,3,4,5,6,7,8,9],
          selected_texts_de = [0,1,2,3,4,5,6,7,8,9],
          selected_texts_en = [0,1,2,3,4,5,6,7,8,9],
          
          smtp_provider = null,
          smtp_host = null,
          smtp_port = null,
          smtp_username = null,
          smtp_password_hash = null,
          smtp_salt = null,
          
          last_opened = current_datetime
        )
     
     b. Zeige Welcome Screen:
        ┌────────────────────────────────────────┐
        │                                        │
        │       Welcome to LetMeDoMyWork!        │
        │                                        │
        │   Automate your follow-up emails      │
        │   with human-like reminders           │
        │                                        │
        │   Before you start, please configure  │
        │   your email settings.                │
        │                                        │
        │         [Get Started]                  │
        │                                        │
        └────────────────────────────────────────┘
     
     c. Bei "Get Started" Click:
        Navigate zu Settings Screen → SMTP Section
        Highlight SMTP-Felder
        Zeige Tooltip: "Configure these fields to send emails"
  
  3. ELSE:
     // Settings existieren bereits
     Normal App-Start (Main Screen mit TODO-Liste)
```

### SMTP Configuration

**Provider Selection:**
```
UI: Dropdown/Radio Buttons

Optionen:
  1. Gmail
     - smtp_host = "smtp.gmail.com"
     - smtp_port = 587
     - TLS = true (fest)
     - Help Link: https://support.google.com/accounts/answer/185833
     - Help Text: "You need an App Password. Click '?' for instructions."
  
  2. Outlook  
     - smtp_host = "smtp-mail.outlook.com"
     - smtp_port = 587
     - TLS = true (fest)
     - Help Link: https://support.microsoft.com/account-billing/...
     - Help Text: "You need an App Password. Click '?' for instructions."
  
  3. Custom
     - smtp_host = [User Input Feld]
     - smtp_port = [Number Input Feld]
     - TLS = [Checkbox] (default: true)
     - Help Text: "Enter your mail provider's SMTP settings"

Bei Provider-Wechsel:
  - Host/Port werden automatisch gesetzt (Gmail/Outlook)
  - Bei Custom: Zeige Input-Felder
  - Username/Password bleiben erhalten
```

**Password Storage (Encryption):**
```
Verwendete Packages:
  - flutter_secure_storage (Platform-native Encryption)
  - crypto (für PBKDF2 Hashing)

Beim Speichern eines Passworts:
  1. User gibt Passwort ein (plain text)
  
  2. Generate random salt:
     salt = generateRandomBytes(16)  // 16 bytes = 128 bit
  
  3. Hash Passwort mit PBKDF2:
     hash = PBKDF2(
       password: user_input,
       salt: salt,
       iterations: 10000,
       keyLength: 32,  // 256 bit
       hashAlgorithm: SHA256
     )
  
  4. Speichere in flutter_secure_storage:
     await storage.write(key: "smtp_password_hash", value: base64(hash))
     await storage.write(key: "smtp_salt", value: base64(salt))
  
  5. Speichere Referenz in SQLite:
     UPDATE settings SET 
       smtp_password_hash = "[ENCRYPTED]",  // Marker, nicht echter Hash
       smtp_salt = "[ENCRYPTED]"

Beim Abrufen (für SMTP-Login):
  1. Lade aus flutter_secure_storage:
     hash_b64 = await storage.read(key: "smtp_password_hash")
     salt_b64 = await storage.read(key: "smtp_salt")
  
  2. Decode:
     hash = base64_decode(hash_b64)
     salt = base64_decode(salt_b64)
  
  3. Für SMTP Login wird ORIGINAL PASSWORT benötigt!
     Problem: Wir haben nur den Hash, nicht das Original
     
     Lösung: Passwort symmetrisch verschlüsseln, nicht hashen
     
KORREKTUR - Richtige Encryption:
  
  Beim Speichern:
    1. Generate random encryption key aus Device Keystore
       (flutter_secure_storage macht das automatisch)
    
    2. Encrypt Passwort:
       encrypted = AES_encrypt(password, device_key)
    
    3. Speichere encrypted in flutter_secure_storage:
       await storage.write(key: "smtp_password", value: encrypted)
  
  Beim Abrufen:
    1. Lade encrypted:
       encrypted = await storage.read(key: "smtp_password")
    
    2. Decrypt:
       password = AES_decrypt(encrypted, device_key)
    
    3. Verwende für SMTP-Login

Sicherheit:
  - flutter_secure_storage nutzt:
    * iOS: Keychain
    * Android: KeyStore + EncryptedSharedPreferences
  - Encryption-Key verlässt nie das Gerät
  - Bei Geräte-Reset: Passwort ist verloren (Feature, kein Bug)
```

**Help Links (Provider App-Passwort Anleitungen):**
```
Gmail Help Link:
  URL: https://support.google.com/accounts/answer/185833
  
  Anleitung (In-App anzeigen):
    1. Go to your Google Account
    2. Select "Security"
    3. Under "Signing in to Google," select "App Passwords"
    4. Select "Mail" and your device
    5. Copy the generated 16-character password
    6. Paste it in the Password field

Outlook Help Link:
  URL: https://support.microsoft.com/account-billing/using-app-passwords-with-apps-that-don-t-support-two-step-verification-5896ed9b-4263-e681-128a-a6f2979a7944
  
  Anleitung (In-App anzeigen):
    1. Sign in to your Microsoft account
    2. Go to "Security" > "Advanced security options"
    3. Under "App passwords," select "Create a new app password"
    4. Copy the generated password
    5. Paste it in the Password field

UI für Help:
  [?] Button neben Password-Feld
  → Öffnet Bottom Sheet mit Anleitung + "Open Help Page" Button
```

**Test Email Funktion:**
```
Button: [Send Test Email]
Position: Unter Password-Feld in SMTP Config

Beim Click:
  1. Validiere Eingaben:
     - smtp_host: nicht leer
     - smtp_port: 1-65535
     - smtp_username: nicht leer (valid email)
     - smtp_password: nicht leer
  
  2. Zeige Loading Dialog:
     "Sending test email..."
     (Spinner Animation)
  
  3. Versuche SMTP-Verbindung + Send:
     To: smtp_username (eigene Adresse)
     Subject: "LetMeDoMyWork - Test Email"
     Body: """
     This is a test email from LetMeDoMyWork app.
     
     Your SMTP configuration is working correctly!
     
     Provider: {smtp_provider}
     Host: {smtp_host}
     Port: {smtp_port}
     
     Sent at: {current_datetime}
     """
  
  4a. Bei Erfolg:
      - Schließe Loading Dialog
      - Zeige Success Dialog:
        ┌────────────────────────────────────┐
        │ ✅ Test Email Sent!                │
        │                                    │
        │ Check your inbox at:              │
        │ {smtp_username}                   │
        │                                    │
        │           [OK]                     │
        └────────────────────────────────────┘
      - Speichere Settings in DB
  
  4b. Bei Fehler:
      - Schließe Loading Dialog
      - Zeige Error Dialog:
        ┌────────────────────────────────────┐
        │ ❌ Test Email Failed                │
        │                                    │
        │ Error: {error_message}            │
        │                                    │
        │ Common issues:                    │
        │ • Wrong password                  │
        │ • App password not enabled        │
        │ • SMTP settings incorrect         │
        │ • Firewall blocking connection    │
        │                                    │
        │      [Retry]  [Cancel]             │
        └────────────────────────────────────┘
      - Bei "Retry": Wiederhole ab Schritt 3
```

---

### Template Management

**Structure in Settings:**
```
Settings Table speichert:
  - subjects_de: JSON Array [String, String, ...] (30 Elemente)
  - subjects_en: JSON Array [String, String, ...] (30 Elemente)
  - texts_de: JSON Array [String, String, ...] (30 Elemente)
  - texts_en: JSON Array [String, String, ...] (30 Elemente)
  
  - selected_subjects_de: JSON Array [Int, Int, ...] (10 Indices)
  - selected_subjects_en: JSON Array [Int, Int, ...] (10 Indices)
  - selected_texts_de: JSON Array [Int, Int, ...] (10 Indices)
  - selected_texts_en: JSON Array [Int, Int, ...] (10 Indices)

Beispiel selected_subjects_de:
  [0, 3, 7, 2, 15, 8, 20, 25, 28, 29]
  
  Bedeutet:
    1. Send → subjects_de[0]
    2. Send → subjects_de[3]
    3. Send → subjects_de[7]
    ...
```

**Template Selection Screen:**
```
Navigation: Settings → "German Subjects (30)" → Template Selection Screen

UI:
┌────────────────────────────────────────────┐
│ ← German Subjects                          │
│                                            │
│ Select 10 templates for follow-ups        │
│ (Drag to reorder)                          │
│                                            │
│ ═══════ Selected (10) ═══════             │
│                                            │
│ 🟢 1. Follow-Up: {InitialSubject}     ≡   │ ← Drag Handle
│ 🟢 2. Nochmal bzgl.: {InitialSubject} ≡   │
│ 🟢 3. Kurze Erinnerung: ...           ≡   │
│ 🟢 4. Rückmeldung zu: ...             ≡   │
│ 🟢 5. Nachfrage: ...                  ≡   │
│ 🟢 6. Re: ...                         ≡   │
│ 🟢 7. Freundliche Erinnerung: ...     ≡   │
│ 🟢 8. Zweite Erinnerung: ...          ≡   │
│ 🟢 9. Status-Update erbeten: ...      ≡   │
│ 🟢 10. Dringend - ...                 ≡   │
│                                            │
│ Label: "1" = First send, "10" = Last send │
│                                            │
│ ═══════ Available (20) ═══════            │
│                                            │
│ ⚪ Wichtig: {InitialSubject}          [+] │ ← Add Button
│ ⚪ Bitte um Rückmeldung: ...          [+] │
│ ⚪ Noch offen: ...                    [+] │
│ ...                                        │
│                                            │
│         [Cancel]  [Save Selection]         │
└────────────────────────────────────────────┘

Funktionalität:
  - Selected Section: Drag & Drop zum Reordern
  - Available Section: [+] Button zum Hinzufügen
  - Beim [+] Click:
      * Template zu Selected hinzufügen (ans Ende)
      * Aus Available entfernen
      * Wenn Selected.length > max_follow_ups:
          Zeige Warning: "Maximum {max} templates. Remove one first."
  
  - Selected Template Click:
      * Zeige [-] Button
      * Bei Click: Zurück zu Available verschieben
  
  - Drag & Drop in Selected:
      * Ändert Reihenfolge in selected_*_indices Array
      * Erste Position = Index 0 (wird bei erstem Send verwendet)
```

**Add New Template:**
```
In Template Selection Screen:
  Button: [+ Add Custom Template] (unten)

Click → Zeige Dialog:
┌────────────────────────────────────────────┐
│ Add Custom Subject Template                │
│                                            │
│ Template Text:                             │
│ [_____________________________________]    │
│ [_____________________________________]    │
│                                            │
│ Available Placeholders:                   │
│ • {Vorname}                               │
│ • {Nachname}                              │
│ • {InitialSubject}                        │
│ • {DateToday}                             │
│ • {DateLastMail}                          │
│ • {DaysSinceLastMail}                     │
│ • {InitialText}                           │
│                                            │
│ Preview:                                   │
│ [Auto-Update Preview mit Beispiel-Daten]  │
│                                            │
│        [Cancel]  [Add Template]            │
└────────────────────────────────────────────┘

Bei "Add Template":
  1. Validiere: nicht leer
  2. Füge zu subjects_de (oder _en) Array hinzu
  3. Update Settings in DB
  4. Zeige in Available Section
  5. User kann es dann zu Selected hinzufügen
```

**Edit Existing Template:**
```
Long Press auf Template (in Selected oder Available):
  → Context Menu: [Edit] [Delete]

Edit:
  - Gleicher Dialog wie "Add New"
  - Pre-filled mit aktuellem Text
  - Bei Save: Update im subjects_*/texts_* Array
  
Delete:
  - Zeige Confirmation: "Delete this template?"
  - Check ob in selected_*_indices verwendet:
      IF (in_use):
        Error: "Template is in use. Remove from selection first."
      ELSE:
        Lösche aus subjects_*/texts_* Array
        Update indices in selected_*_* (alle > deleted_index -= 1)
```

---

### Other Settings

**Max Follow-Ups:**
```
UI: Number Input (Stepper)
Range: 1 - 30
Default: 10

Label: "Maximum Follow-Ups"
Help Text: "How many follow-up emails to send before repeating the last template"

onChange:
  - Update settings.max_follow_ups
  - Beeinflusst TODO Creation (wie viele Templates pre-selected)
  - Beeinflusst Färbung (send_count / max_follow_ups)
  
  - IF (new_value < current_selected_count):
      Zeige Warning:
      "You have {count} templates selected but max is now {new_value}.
       Please update your template selections."
```

**Randomize Send Times:**
```
UI: Number Input (Slider + Text Field)
Range: 0 - 120 Minuten
Default: 30

Label: "Randomize send times (±minutes)"
Help Text: "Adds random variation to send times to appear more human"

Example Display:
  "Send time 09:00 ± 30 min = 08:45 - 09:15"

onChange:
  - Update settings.randomize_minutes
  - Beeinflusst alle zukünftigen Send-Zeit-Berechnungen
  - Bestehende next_send_datetime werden NICHT neu berechnet
```

---

## Statistics Calculation

### Overall Statistics

**Total Emails Sent:**
```sql
SELECT COUNT(*) FROM sent_emails
```

**Active TODOs:**
```sql
SELECT COUNT(*) FROM todos 
WHERE is_completed = false
```

**Completed TODOs:**
```sql
SELECT COUNT(*) FROM todos 
WHERE is_completed = true
```

**Average Response Time:**
```sql
-- Nur completed TODOs
SELECT AVG(
  (completed_at - created_at) / 86400000.0  -- milliseconds zu Tage
) AS avg_response_days
FROM todos
WHERE is_completed = true

-- Anzeige: "4.2 days" (gerundet auf 1 Dezimal)
```

**Average Sends Until Response:**
```sql
WITH send_counts AS (
  SELECT 
    todo_id,
    COUNT(*) as sends
  FROM sent_emails
  WHERE todo_id IN (
    SELECT id FROM todos WHERE is_completed = true
  )
  GROUP BY todo_id
)
SELECT AVG(sends) AS avg_sends
FROM send_counts

-- Anzeige: "2.8 sends" (gerundet auf 1 Dezimal)
```

---

### By Recipient Statistics

**Query:**
```sql
SELECT 
  recipient_email,
  recipient_first_name,
  recipient_last_name,
  COUNT(*) as completed_count,
  AVG((completed_at - created_at) / 86400000.0) as avg_response_days,
  AVG(
    (SELECT COUNT(*) FROM sent_emails WHERE todo_id = todos.id)
  ) as avg_sends
FROM todos
WHERE is_completed = true
GROUP BY recipient_email
ORDER BY completed_count DESC
LIMIT 20
```

**UI Display:**
```
─── By Recipient ───

john.doe@example.com (John Doe)
  • Avg. Response: 3.1 days
  • Sends/Response: 2.3
  • Completed: 5

jane.smith@company.com (Jane Smith)
  • Avg. Response: 6.7 days
  • Sends/Response: 4.1
  • Completed: 3

...
```

---

### Best Follow-Up Texts

**Logic:**
```
Für jeden completed TODO:
  1. Finde letzten sent_email BEFORE completion:
     SELECT * FROM sent_emails
     WHERE todo_id = X
       AND sent_at < (SELECT completed_at FROM todos WHERE id = X)
     ORDER BY sent_at DESC
     LIMIT 1
  
  2. Extrahiere body (= text template mit replacements)
  
  3. Berechne response_time:
     response_days = (completed_at - last_sent_at) / 86400000.0
  
  4. Speichere: (body_text, response_days)

Gruppierung:
  GROUP BY body_text (exakter Match)
  → Problem: Platzhalter sind replaced, Texte unterschiedlich
  
  Lösung: Speichere original template_index in sent_emails
  → Gruppe nach template_index statt body

KORREKTUR - Neues sent_emails Feld:
  - template_index: INTEGER (welches Template wurde verwendet)

Query:
SELECT 
  template_index,
  AVG(
    (todos.completed_at - sent_emails.sent_at) / 86400000.0
  ) as avg_response_days,
  COUNT(*) as usage_count
FROM sent_emails
JOIN todos ON sent_emails.todo_id = todos.id
WHERE todos.is_completed = true
  AND sent_emails.sent_at = (
    -- Letzter Send vor Completion
    SELECT MAX(sent_at) FROM sent_emails se2
    WHERE se2.todo_id = sent_emails.todo_id
      AND se2.sent_at < todos.completed_at
  )
GROUP BY template_index
ORDER BY avg_response_days ASC
LIMIT 10
```

**UI Display:**
```
─── Best Follow-Up Texts ───
(Based on average response time)

1. "Hi {Vorname}, kurze Erinnerung..."
   Avg. Response: 2.1 days
   Used: 12 times

2. "Hallo {Vorname}, hast du meine..."  
   Avg. Response: 2.8 days
   Used: 8 times

3. "Sehr geehrte/r {Vorname} {Nachname}..."
   Avg. Response: 3.5 days
   Used: 5 times

...
```

---

### Response Heatmap (Wochentage)

**Query:**
```sql
-- Wochentag der Completion ermitteln
-- Monday = 1, Sunday = 7
SELECT 
  CASE CAST(strftime('%w', completed_at / 1000, 'unixepoch') AS INTEGER)
    WHEN 0 THEN 7  -- Sunday
    WHEN 1 THEN 1  -- Monday
    WHEN 2 THEN 2  -- Tuesday
    WHEN 3 THEN 3  -- Wednesday
    WHEN 4 THEN 4  -- Thursday
    WHEN 5 THEN 5  -- Friday
    WHEN 6 THEN 6  -- Saturday
  END AS weekday,
  COUNT(*) as count
FROM todos
WHERE is_completed = true
GROUP BY weekday
ORDER BY weekday
```

**Percentage Calculation:**
```
total_completions = SUM(counts)

FOR each weekday:
  percentage = (count / total_completions) * 100
```

**UI Display:**
```
─── Response Heatmap ───
Best days for responses:

Mon ████████ 23% (15 responses)
Tue ██████████ 31% (20 responses)
Wed ███████ 19% (12 responses)
Thu ██████ 15% (10 responses)
Fri ████ 12% (8 responses)
Sat - 0% (0 responses)
Sun - 0% (0 responses)

Bar Length: (percentage / max_percentage) * max_bar_length
```

---

## Data Export/Import

### Export

**Button:** In Settings → "Export Backup"

**Process:**
```
1. User klickt "Export Backup"

2. Zeige Loading Dialog: "Preparing backup..."

3. Sammle alle Daten:
   a. Settings (komplett)
   b. Alle TODOs
   c. Alle sent_emails
   
   JSON Structure:
   {
     "version": "1.0.0",
     "app": "LetMeDoMyWork",
     "export_date": "2026-01-29T10:30:00Z",
     "device": "Android 14",
     
     "settings": {
       "max_follow_ups": 10,
       "randomize_minutes": 30,
       "smtp_provider": "gmail",
       "smtp_username": "user@gmail.com",
       // Passwort NICHT exportieren (Sicherheit)
       "subjects_de": [...],
       "subjects_en": [...],
       "texts_de": [...],
       "texts_en": [...],
       "selected_subjects_de": [0,1,2,...],
       "selected_subjects_en": [0,1,2,...],
       "selected_texts_de": [0,1,2,...],
       "selected_texts_en": [0,1,2,...]
     },
     
     "todos": [
       {
         "id": 1,
         "subject": "...",
         "recipient_email": "...",
         // alle Felder
       },
       ...
     ],
     
     "sent_emails": [
       {
         "id": 1,
         "todo_id": 1,
         "subject": "...",
         "body": "...",
         "sent_at": "2026-01-25T09:15:00Z",
         "send_number": 1,
         "template_index": 0
       },
       ...
     ]
   }

4. Serialize zu JSON String
   json_string = JSON.encode(data)

5. Komprimiere (optional, nur wenn > 1MB):
   compressed = GZIP.compress(json_string)
   use_compression = true

6. Generate Filename:
   timestamp = DateFormat("yyyyMMdd_HHmmss").format(DateTime.now())
   filename = "LetMeDoMyWork_backup_${timestamp}.json"
   // oder .json.gz wenn komprimiert

7. Speichere File:
   path = "/storage/emulated/0/Download/${filename}"
   await File(path).writeAsBytes(compressed oder json_string)

8. Berechne File Size:
   size_bytes = File(path).lengthSync()
   size_mb = size_bytes / (1024 * 1024)

9. IF (size_mb < 10):
   
   a. Sende Email an settings.smtp_username:
      Subject: "LetMeDoMyWork Backup - ${DateFormat('dd.MM.yyyy').format(now)}"
      Body: """
      Your LetMeDoMyWork backup is attached.
      
      Backup Details:
      - Date: ${export_date}
      - TODOs: ${todos.length}
      - Sent Emails: ${sent_emails.length}
      - File Size: ${size_mb.toStringAsFixed(2)} MB
      
      Keep this file safe. You can import it on any device.
      """
      Attachment: backup file
   
   b. Bei Email-Erfolg:
      success_message = "Backup saved and emailed to you!"
   
   c. Bei Email-Fehler:
      success_message = "Backup saved to Downloads. Email failed to send."

   ELSE (size >= 10 MB):
     success_message = "Backup saved to Downloads (too large to email)"

10. Schließe Loading Dialog

11. Zeige Success Dialog:
    ┌────────────────────────────────────────┐
    │ ✅ Backup Created!                     │
    │                                        │
    │ {success_message}                     │
    │                                        │
    │ Location:                             │
    │ /Download/{filename}                  │
    │                                        │
    │ Size: {size_mb} MB                    │
    │                                        │
    │     [Open Folder]  [OK]                │
    └────────────────────────────────────────┘
    
    "Open Folder" → Öffnet File Manager zu Downloads
```

---

### Import

**Button:** In Settings → "Import Backup"

**Process:**
```
1. User klickt "Import Backup"

2. Öffne File Picker:
   - Filter: .json, .json.gz
   - Start Directory: Downloads

3. User wählt File

4. Validiere File:
   a. Prüfe Extension (.json oder .json.gz)
   b. Prüfe Lesbarkeit
   c. Falls .gz: Dekomprimiere erst
   d. Parse JSON
   e. Validiere Structure:
      - version exists
      - app == "LetMeDoMyWork"
      - settings, todos, sent_emails keys exist

5. Bei Validierungsfehler:
   Zeige Error Dialog:
   "Invalid backup file. Please select a valid LetMeDoMyWork backup."
   → Zurück zu Schritt 2

6. Zeige Import Preview Dialog:
   ┌────────────────────────────────────────┐
   │ Import Backup?                         │
   │                                        │
   │ ⚠️ This will REPLACE all current data: │
   │                                        │
   │ Current Data:                         │
   │ • {current_todos_count} TODOs         │
   │ • {current_emails_count} Sent Emails  │
   │                                        │
   │ Backup Contains:                      │
   │ • {backup_todos_count} TODOs          │
   │ • {backup_emails_count} Sent Emails   │
   │ • Created: {backup_export_date}       │
   │                                        │
   │ Note: SMTP password is NOT included   │
   │ in backups. You'll need to            │
   │ reconfigure it after import.          │
   │                                        │
   │        [Cancel]  [Import]              │
   └────────────────────────────────────────┘

7a. Bei "Cancel":
    - Schließe Dialog
    - Keine Aktion

7b. Bei "Import":
    a. Zeige Loading: "Importing backup..."
    
    b. Database Transaction BEGIN
    
    c. Lösche alle bestehenden Daten:
       DELETE FROM sent_emails;
       DELETE FROM todos;
       UPDATE settings SET ...;  // Reset zu Defaults
    
    d. Importiere neue Daten:
       INSERT INTO settings (...) VALUES (...);
       // Note: smtp_password bleibt leer, User muss neu eingeben
       
       FOR each todo in backup:
         INSERT INTO todos (...) VALUES (...);
       
       FOR each email in backup:
         INSERT INTO sent_emails (...) VALUES (...);
    
    e. Database Transaction COMMIT
    
    f. Berechne alle next_send_datetime neu:
       // Falls bereits überfällig → setze auf "jetzt"
       FOR each active TODO:
         IF (next_send_datetime < current_datetime):
           next_send_datetime = current_datetime
    
    g. Setze Background Alarms neu
    
    h. Schließe Loading Dialog
    
    i. Zeige Success Dialog:
       ┌────────────────────────────────────────┐
       │ ✅ Import Successful!                  │
       │                                        │
       │ Imported:                             │
       │ • {imported_todos} TODOs              │
       │ • {imported_emails} Sent Emails       │
       │                                        │
       │ ⚠️ Please reconfigure your SMTP        │
       │    password in Settings.              │
       │                                        │
       │  [Go to Settings]  [OK]                │
       └────────────────────────────────────────┘
    
    j. Bei "Go to Settings":
       Navigate zu Settings → SMTP Section

8. Bei Import-Fehler (Exception während Transaction):
   a. ROLLBACK Transaction
   b. Zeige Error Dialog:
      "Import failed: {error_message}
       Your existing data is unchanged."
```

---

## Edge Cases & Error Handling

### Email Send Failures

**Scenario:** SMTP-Fehler beim Senden
```
Mögliche Fehler:
  - Netzwerk nicht verfügbar
  - SMTP Server nicht erreichbar
  - Authentication fehlgeschlagen
  - Timeout
  - Invalide Email-Adresse
  - Rate Limit überschritten

Error Handling:
  1. Catch Exception im SMTP Send Process
  
  2. Log Error:
     timestamp = current_datetime
     error_entry = {
       "todo_id": X,
       "error_type": exception.type,
       "error_message": exception.message,
       "timestamp": timestamp
     }
     // Speichere in separater error_log Table oder File
  
  3. Markiere TODO visuell:
     - Roter Rahmen um Eintrag
     - Rotes Warn-Icon neben Subject
     - Hover/Long-Press zeigt Error-Message
  
  4. next_send_datetime bleibt UNVERÄNDERT
     → Beim nächsten Alarm-Trigger wird erneut versucht
  
  5. Zeige Error Notification:
     Title: "LetMeDoMyWork - Send Failed"
     Body: "Failed to send email to {recipient}. Tap to retry."
     Persistent: true (nicht auto-dismiss)
     Action: Tap → Navigate zu TODO Detail Screen
  
  6. TODO Detail Screen zeigt:
     ┌────────────────────────────────────────┐
     │ ⚠️ Last Send Failed                    │
     │                                        │
     │ Error: {error_message}                │
     │ Time: {error_timestamp}               │
     │                                        │
     │         [Retry Send Now]               │
     │                                        │
     │ Common Solutions:                     │
     │ • Check internet connection           │
     │ • Verify SMTP settings                │
     │ • Check email recipient               │
     └────────────────────────────────────────┘
  
  7. [Retry Send Now] Button:
     → Triggert Manual Send Process
     → Bei Erfolg: Entferne Fehler-Markierung, Update next_send
```

---

### Database Corruption

**Scenario:** SQLite DB beschädigt
```
Bei App-Start (vor Main UI):
  1. Prüfe DB Integrität:
     result = db.rawQuery("PRAGMA integrity_check")
  
  2. IF (result != "ok"):
     
     a. Suche nach letztem Auto-Backup:
        // Optional: App erstellt täglich Auto-Backup
        latest_backup = findLatestBackup("/data/.../backups/")
     
     b. Zeige Critical Error Dialog:
        ┌────────────────────────────────────────┐
        │ ⚠️ Database Corruption Detected        │
        │                                        │
        │ Your database is corrupted and        │
        │ cannot be used.                       │
        │                                        │
        │ IF (latest_backup exists):            │
        │   Last backup: {backup_date}          │
        │   [Restore Backup]  [Start Fresh]     │
        │                                        │
        │ ELSE:                                 │
        │   [Start Fresh]                       │
        │                                        │
        │ Warning: "Start Fresh" will delete    │
        │ all data!                             │
        └────────────────────────────────────────┘
     
     c. Bei "Restore Backup":
        → Importiere latest_backup
        → Navigate zu Main Screen
     
     d. Bei "Start Fresh":
        → DELETE DATABASE
        → Erstelle neue leere DB
        → Initialisiere Default Settings
        → Navigate zu Welcome Screen
```

---

### Invalid Template Placeholders

**Scenario:** Template enthält unbekannten Platzhalter
```
Beim Email-Senden:
  1. Replace alle BEKANNTEN Platzhalter:
     - {Vorname}, {Nachname}, {DateToday}, etc.
  
  2. Prüfe ob noch {*} Pattern im Text:
     remaining = Regex.find(text, r'\{[^}]+\}')
  
  3. IF (remaining not empty):
     
     a. Log Warning:
        "Unknown placeholders in template: {remaining}"
     
     b. Ersetze unbekannte mit Fallback:
        text = text.replaceAll(r'\{[^}]+\}', '[UNKNOWN]')
        
        // Besser: Zeige Original-Platzhalter
        // Lasse {UnknownPlaceholder} stehen
     
     c. Sende Email trotzdem
        // User wird in sent_emails_history den Fehler sehen
     
     d. Optional: Nach Send Warnung anzeigen
        "Email sent, but contained unknown placeholders"
```

---

### Timezone Changes

**Scenario:** User reist, Timezone ändert sich
```
Strategie: Alle Timestamps in UTC speichern, in Local anzeigen

Storage:
  - created_at: TIMESTAMP (UTC)
  - completed_at: TIMESTAMP (UTC)
  - next_send_datetime: TIMESTAMP (UTC)
  - sent_at: TIMESTAMP (UTC)

Display:
  - Konvertiere zu Local beim Anzeigen:
    display_time = utc_time.toLocal()
  
  - Formatiere mit Local Timezone:
    DateFormat("dd.MM.yyyy HH:mm").format(display_time)

Send Time Handling:
  - send_time in TODO: "09:00" (String, keine Timezone)
  - Bedeutung: "09:00 LOCAL TIME des Geräts"
  
  - Berechnung von next_send_datetime:
    local_date = start_date.toLocal()
    local_datetime = DateTime(
      local_date.year,
      local_date.month,
      local_date.day,
      send_time.hour,
      send_time.minute
    )
    next_send_datetime = local_datetime.toUtc()  // Speichere in UTC

  - Bei Timezone-Wechsel:
    → next_send_datetime in UTC bleibt gleich
    → Display in neuer Local Timezone ändert sich automatisch
    → Alarm triggert zur korrekten UTC-Zeit
    → Keine Re-Calculation nötig
```

---

### Max Sends Reached

**Scenario:** send_count >= max_follow_ups
```
Beim Email-Senden:
  1. Berechne template_index wie gewohnt
  
  2. IF (template_index >= selected_templates.length):
     // Kein Template mehr verfügbar für diesen Index
     template_index = selected_templates.length - 1  // Letztes Template
  
  3. Verwende letztes Template (wiederholt)
  
  4. Text-Färbung:
     color_intensity = min(send_count / max_sends, 1.0)
     // Bleibt bei MAX RED auch nach Überschreitung

Keine Auto-Completion:
  - TODO bleibt aktiv
  - User muss manuell completen
  
Optionale Warnung (UI):
  - Wenn send_count == max_sends:
    Zeige Badge auf TODO: "MAX REACHED"
  
  - Oder Notification:
    "TODO '{subject}' reached maximum sends ({max_sends}).
     Consider completing or adding more templates."
```

---

### Interval Change Impact

**Scenario:** User ändert Interval von 1 Tag auf 7 Tage
```
Im Edit Screen:
  - User ändert interval_days von 1 auf 7
  - Klickt Save

Logic:
  1. Berechne neues next_send_datetime:
     
     IF (next_send_datetime in Zukunft):
       // Normal, noch nicht überfällig
       next_send = current_datetime + new_interval + randomized_time
     
     ELSE:
       // Bereits überfällig
       next_send = current_datetime + randomized_time  // Sofort fällig
  
  2. Update TODO in DB
  
  3. Update Background Alarms
  
  4. Zeige Confirmation Toast:
     "Interval updated. Next send: {next_send_datetime}"

Alternative (User Choice):
  Zeige Dialog bei Interval-Änderung:
  ┌────────────────────────────────────────┐
  │ Interval Changed                       │
  │                                        │
  │ When should the next email be sent?   │
  │                                        │
  │ [Keep Current Schedule]                │  ← next_send bleibt gleich
  │ [Recalculate from Now]                 │  ← next_send = now + interval
  │                                        │
  └────────────────────────────────────────┘
```

---

## Permissions & Security

### Required Android Permissions

**AndroidManifest.xml:**
```xml
<manifest>
  <!-- Netzwerk -->
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
  
  <!-- Alarme -->
  <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
  <uses-permission android:name="android.permission.USE_EXACT_ALARM" />
  <uses-permission android:name="android.permission.WAKE_LOCK" />
  
  <!-- Notifications -->
  <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
  
  <!-- Storage (für Export/Import) -->
  <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
                   android:maxSdkVersion="32" />
  <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
                   android:maxSdkVersion="32" />
  
  <!-- Android 13+ Storage (Scoped Storage) -->
  <!-- Keine Permission nötig für Downloads-Ordner -->
  
  <!-- Foreground Service (für Background Email Sending) -->
  <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
  <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
</manifest>
```

**Runtime Permission Requests:**
```
Bei App-Start (First Launch):
  1. Request SCHEDULE_EXACT_ALARM:
     IF (Android >= 12):
       IF (!AlarmManager.canScheduleExactAlarms()):
         Zeige Dialog:
         "LetMeDoMyWork needs permission to schedule exact alarms
          for sending emails at precise times.
          
          Please grant this permission in the next screen."
         
         → Open Settings: ACTION_REQUEST_SCHEDULE_EXACT_ALARM

  2. Request POST_NOTIFICATIONS:
     IF (Android >= 13):
       Request permission: Manifest.permission.POST_NOTIFICATIONS
       
       Rationale:
       "Notifications keep you informed when emails are sent
        and alert you of any issues."

  3. Storage Permissions:
     IF (Android < 13):
       Request WRITE_EXTERNAL_STORAGE für Export-Funktion
     ELSE:
       Keine Permission nötig (Scoped Storage)
```

---

### Data Security

**SMTP Password:**
```
Encryption: flutter_secure_storage
  - iOS: Keychain (AES-256)
  - Android: EncryptedSharedPreferences (AES-256-GCM)
  
  Encryption Key:
    - Generiert von System
    - Gespeichert in Hardware Keystore (wenn verfügbar)
    - Niemals exportiert
    - Bei Factory Reset: Verloren (Feature, nicht Bug)
```

**Alle anderen Daten:**
```
SQLite Database:
  - Location: /data/data/com.letmedomywork.app/databases/letmedomywork.db
  - Encryption: KEINE (Standard SQLite)
  - Zugriff: Nur durch App (Android Sandbox)
  
  Sensitive Daten:
    - recipient_email: Gespeichert in Klartext
    - initial_text: Gespeichert in Klartext
    - sent_emails body: Gespeichert in Klartext
  
  Begründung:
    - Lokale App, keine Cloud-Sync
    - Android Sandbox Protection ausreichend
    - Export liegt in User-Verantwortung
```

**Export Files:**
```
Unverschlüsselt:
  - JSON in Klartext
  - Liegt in öffentlichem Downloads-Ordner
  - Jede App mit Storage-Permission kann lesen
  
Warning an User (bei Export):
  "Backup files are NOT encrypted.
   Store them securely or delete after import."
```

---

## Performance Considerations

### Database Optimization

**Indices:**
```sql
-- Schnelle Suche nach fälligen TODOs
CREATE INDEX idx_todos_next_send 
  ON todos(next_send_datetime, is_paused, is_completed);

-- Schnelle Filterung Active/Completed
CREATE INDEX idx_todos_completed 
  ON todos(is_completed, created_at);

-- Schnelle Filterung Pausiert
CREATE INDEX idx_todos_paused 
  ON todos(is_paused);

-- Schnelle sent_emails für TODO
CREATE INDEX idx_sent_emails_todo 
  ON sent_emails(todo_id, sent_at);

-- Schnelle sent_emails Suche nach Datum
CREATE INDEX idx_sent_emails_date 
  ON sent_emails(sent_at);

-- Schnelle Statistics-Queries
CREATE INDEX idx_todos_recipient 
  ON todos(recipient_email, is_completed);
```

**Query Optimization:**
```
Statt N+1 Queries:
  FOR each todo:
    send_count = COUNT(sent_emails WHERE todo_id = todo.id)

Besser: Joined Query:
  SELECT 
    todos.*,
    COUNT(sent_emails.id) as send_count
  FROM todos
  LEFT JOIN sent_emails ON sent_emails.todo_id = todos.id
  GROUP BY todos.id
```

---

### Memory Management

**Liste Pagination:**
```
IF (todos.length > 100):
  Implementiere Lazy Loading:
  
  - Initial Load: 50 TODOs
  - Bei Scroll zu Ende: Lade weitere 50
  - Entlade TODOs außerhalb Viewport
```

**Template Caching:**
```
Settings-Templates ändern sich selten:
  - Lade bei App-Start
  - Cache in Memory (Singleton)
  - Update nur bei Settings-Änderung
```

**Image/Asset Optimization:**
```
Icons:
  - Verwende Vector Icons (Flutter Icons, Material Icons)
  - Keine PNG/JPG für UI-Elemente
  - Reduziert APK-Größe
```

---

### Background Service Optimization

**WorkManager statt AlarmManager für Checks:**
```
Problem: AlarmManager alle 15min = Battery Drain

Bessere Lösung:
  1. ExactAlarm nur für konkrete Send-Events
     (wenn next_send_datetime bekannt)
  
  2. PeriodicWorkRequest für Fallback-Checks:
     PeriodicWorkRequestBuilder<CheckTODOsWorker>(
       repeatInterval = 15,
       repeatIntervalTimeUnit = TimeUnit.MINUTES,
       flexTimeInterval = 5,  // Kann 5 Min variieren
       flexTimeIntervalUnit = TimeUnit.MINUTES
     )
     
     → Android optimiert Ausführung (batching)
     → Bessere Battery Life
```

**Wake Lock Minimierung:**
```
Bei Email-Send:
  1. Acquire Wake Lock (PARTIAL)
  2. Sende Email (max 30 Sekunden Timeout)
  3. Release Wake Lock sofort
  
  Timeout-Protection:
    acquireWakeLock(timeout: 30 seconds)
    → Falls Code hängt, auto-release nach 30 Sek
```

---

## Future Enhancements (Out of Scope für v1.0)

**Features für zukünftige Versionen:**

1. **Multi-Language UI:**
   - App-Sprache: Deutsch, Englisch, weitere
   - Aktuell: Nur English UI

2. **Dark Mode:**
   - Theme-Toggle in Settings
   - Auto Dark Mode (System Setting)

3. **Email Response Detection:**
   - IMAP Integration
   - Auto-Complete bei erkannter Antwort
   - Requires: Additional Permissions, IMAP Config

4. **Batch Operations:**
   - Multi-Select in TODO Liste
   - Batch Complete/Pause/Delete

5. **Template Sharing:**
   - Export Templates als separates File
   - Import von Community-Templates
   - Template Marketplace

6. **Cloud Backup:**
   - Google Drive Auto-Backup
   - Dropbox Integration
   - Auto-Sync zwischen Geräten

7. **Home Screen Widget:**
   - Zeige nächste fällige TODOs
   - Quick Actions (Complete, Send)

8. **Email Preview:**
   - Zeige final Email vor Send
   - Edit-Option für Einzelfall-Änderungen

9. **Email Recall:**
   - Undo sent email (wenn Provider unterstützt)
   - Gmail: Unsend innerhalb 30 Sekunden

10. **Advanced Statistics:**
    - Success Rate per Recipient
    - Best Send Times (Hour of Day)
    - Template A/B Testing

11. **Notifications Customization:**
    - Custom Notification Sounds
    - Vibration Patterns
    - Do Not Disturb Hours

12. **Email Attachments:**
    - Anhänge zu Follow-Ups hinzufügen
    - PDF, Images, Dokumente

---

## Version History

**v1.0.0 - Initial Release:**
- Core TODO Management (Create, Edit, Delete, Complete, Pause)
- Automated Email Sending via SMTP
- 30 DE + 30 EN Default Templates
- Customizable Templates
- Statistics Dashboard
- Data Export/Import
- Background Service mit Intelligent Wake-Up
- Material Design UI (Blue-Gray Theme)

---

## Technical Stack Summary

**Framework:** Flutter (Dart)

**Database:** SQLite (sqflite package)

**Key Packages:**
- `sqflite` - Local Database
- `flutter_secure_storage` - SMTP Password Encryption
- `mailer` - SMTP Email Sending
- `workmanager` - Background Tasks
- `shared_preferences` - Simple Key-Value Storage
- `intl` - Date/Time Formatting, Localization
- `path_provider` - File System Paths
- `file_picker` - Import File Selection
- `permission_handler` - Runtime Permissions
- `flutter_local_notifications` - Push Notifications

**Architecture:**
- Clean Architecture (Domain, Data, Presentation)
- Repository Pattern für DB-Access
- BLoC/Provider für State Management
- Dependency Injection (get_it)

---

**Ende BusinessLogik.md**