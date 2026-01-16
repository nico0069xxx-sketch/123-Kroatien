# DECISIONS.md - Architektur, Workflow & Daten-Regeln

## Storage Model (VERBINDLICH)

| Quelle | Rolle | Vertrauen | Verwendung |
|--------|-------|-----------|------------|
| **GitHub** | Kanonische Versionskontrolle | AUTORITATIV | Code, Config, Migrations, Docs |
| **Time Machine** | Disaster-Recovery Backup | BACKUP ONLY | Lokale Arbeitskopie + SQLite + Media |
| **iCloud** | Convenience-Sync | NICHT AUTORITATIV | Niemals für Merge/Restore verwenden |

## Workflow-Regeln (VERBINDLICH)

### 1. Git-Schutz
- **Vor jeder Arbeit**: `git status` prüfen
- **Bei uncommitted changes**: Erst commit oder stash
- **Niemals auf main arbeiten ohne Grund**: Feature-Branches für größere Änderungen

### 2. Commit-Regeln
- Kleine, atomare Commits
- Klare Commit-Messages (DE oder EN)
- Push nach jedem stabilen Milestone

### 3. Recovery-Prozess
- Time Machine → Quarantäne-Ordner (`_recovered_from_tm/`)
- Diff gegen GitHub-Version
- Additive Merge (keine Überschreibungen ohne Prüfung)
- Quarantäne-Ordner NICHT committen (.gitignore)

### 4. Session-Ende (PFLICHT)
- [ ] `git status` = clean
- [ ] Changes pushed to GitHub
- [ ] HANDOFF.md aktualisiert

## Django-spezifische Daten-Regeln

### SQLite (db.sqlite3)
- **NICHT in Git** - via .gitignore ausgeschlossen
- **NICHT kanonisch** - Migrations definieren Schema
- **Backup via Time Machine** - nicht via Git
- **Produktionsdaten niemals committen**

### Media/Uploads
- **NICHT in Git** - via .gitignore ausgeschlossen
- **Backup via Time Machine** oder externem Storage
- Produktions-Media über S3/Cloud Storage

### Migrations
- **IMMER in Git** - definieren das Schema
- **Niemals manuell editieren** ohne Grund
- **Reihenfolge beachten** - keine Konflikte erzeugen

### Secrets (.env)
- **NIEMALS in Git** - via .gitignore ausgeschlossen
- **.env.example** = Template für neue Entwickler
- Produktions-Secrets via Umgebungsvariablen/Vault

## Tech Stack

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Backend | Django | 4.2.1 |
| Frontend | Bootstrap + jQuery | 4.x |
| Database (Dev) | SQLite | 3.x |
| Database (Prod) | PostgreSQL | 13+ |
| Templates | Django Templates | Server-side |
| KI-Features | OpenAI/Emergent | - |

## Verzeichnisstruktur

real-estate-django-ALTmain/ ├── accounts/ # User Auth ├── contacts/ # Kontaktformulare ├── docs/ # Governance-Dateien ├── listings/ # Immobilien-Models ├── main/ # Haupt-App (Views, etc.) ├── pages/ # Statische Seiten ├── realtors/ # Makler-Models (Legacy) ├── realstate/ # Django Settings, URLs ├── static/ # CSS, JS, Images ├── staticfiles/ # Collected Static (generated) ├── templates/ # HTML Templates ├── .env # Secrets (NICHT in Git) ├── .env.example # Template für .env ├── .gitignore # Git-Ausschlüsse ├── db.sqlite3 # SQLite (NICHT in Git) ├── manage.py # Django CLI └── requirements.txt # Python Dependencies

