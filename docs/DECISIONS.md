# DECISIONS.md - Architektur & Workflow-Entscheidungen

## Storage Model

| Quelle | Rolle | Vertrauen |
|--------|-------|-----------|
| GitHub | Kanonische Versionskontrolle | AUTORITATIV |
| Time Machine | Lokales Disaster-Recovery Backup | BACKUP ONLY |
| iCloud | Nicht verwenden | NICHT AUTORITATIV |

## Workflow-Regeln

1. **Keine Arbeit ohne Git-Schutz**
   - Vor jeder Änderung: `git status` prüfen
   - Bei Änderungen: erst commit/stash

2. **Branch-Workflow**
   - Feature-Branches für neue Funktionen
   - Fix-Branches für Bugfixes
   - main = production-ready

3. **Recovery-Prozess**
   - Time Machine → Quarantäne-Ordner (`_recovered_from_tm/`)
   - Diff gegen GitHub
   - Additive Merge (keine Überschreibungen)

4. **Session-Ende**
   - Clean git status
   - Pushed to GitHub
   - HANDOFF.md aktualisiert

## Technische Entscheidungen

- Django 4.2.1 + SQLite (lokal) / PostgreSQL (prod)
- Bootstrap 4 + Font Awesome 4.7
- emergentintegrations für KI-Features
- i18n_patterns für Mehrsprachigkeit (12 Sprachen)
