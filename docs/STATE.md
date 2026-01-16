# STATE.md - Aktueller Projektstatus

## Letzte Aktualisierung: 16. Januar 2026

### Git Status
- Branch: feature/ci-and-settings-baseline
- Baseline: 9b78c8c (main)
- Status: In Arbeit

### Enforced Quality Gates

1. **GitHub Actions CI**
   - Syntax-Check (compileall)
   - Django System Check
   - Migration Check
   - Unit Tests (Smoke Tests)

2. **Environment-basierte Settings**
   - SECRET_KEY via env
   - DEBUG via env (default: False)
   - DATABASE via DATABASE_URL oder SQLite

3. **Gitignore Schutz**
   - db.sqlite3 ausgeschlossen
   - .env ausgeschlossen
   - media/ ausgeschlossen

### Bekannte Risiken
1. SQLite Migration Fragility (LOW)
2. OpenAI API Key ungueltig (MEDIUM)
3. Duplizierte XML-Import Logik (LOW)

### Naechste Schritte
1. Branch mergen nach main
2. Bauunternehmen-Funktionalitaet testen
3. Gutscheincode-Feld bei Registrierung
