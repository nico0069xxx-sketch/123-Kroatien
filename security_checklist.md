# Sicherheits-Checkliste für Django-Projekt
# Vor dem Deployment durchgehen!

## 🔒 KRITISCH (MUSS gemacht werden):

- [ ] SECRET_KEY in .env verschoben (nicht im Code!)
- [ ] DEBUG = False in Produktion
- [ ] ALLOWED_HOSTS richtig konfiguriert (keine '*')
- [ ] Email-Passwort in .env verschoben
- [ ] .env in .gitignore hinzugefügt
- [ ] .env NIEMALS committet!
- [ ] Neuen SECRET_KEY generiert
- [ ] HTTPS aktiviert (SSL-Zertifikat)

## 🔐 WICHTIG (Sollte gemacht werden):

- [ ] SECURE_SSL_REDIRECT = True (HTTPS erzwingen)
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_HSTS aktiviert
- [ ] X_FRAME_OPTIONS = 'DENY'
- [ ] SECURE_CONTENT_TYPE_NOSNIFF = True
- [ ] PostgreSQL statt SQLite in Produktion
- [ ] Logging aktiviert
- [ ] Fehler-Monitoring (z.B. Sentry)

## ✅ EMPFOHLEN (Best Practice):

- [ ] Regelmäßige Django-Updates
- [ ] Dependencies aktuell halten (requirements.txt)
- [ ] Backups automatisiert
- [ ] Rate-Limiting für API
- [ ] Admin-URL ändern (nicht /admin/)
- [ ] Starke Passwörter erzwingen
- [ ] 2FA für Admin-Accounts
- [ ] CORS richtig konfiguriert
- [ ] SQL-Injection-Schutz (Django ORM nutzen)
- [ ] XSS-Schutz (Template-Engine nutzen)

## 🧪 TESTING:

- [ ] Security Headers testen: https://securityheaders.com/
- [ ] SSL-Konfiguration testen: https://www.ssllabs.com/
- [ ] Django Check ausführen: python manage.py check --deploy
- [ ] Penetration-Tests durchführen

## 📝 DOKUMENTATION:

- [ ] .env.example erstellt
- [ ] README mit Setup-Anleitung
- [ ] Deployment-Anleitung
- [ ] Backup-Prozess dokumentiert

## 🚨 NOTFALL-PLAN:

- [ ] Backup-Strategie definiert
- [ ] Recovery-Plan dokumentiert
- [ ] Kontakt-Informationen hinterlegt
- [ ] Incident-Response-Plan
