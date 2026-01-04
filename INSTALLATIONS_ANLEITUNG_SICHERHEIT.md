# =============================================
# INSTALLATIONS-ANLEITUNG: SICHERHEIT
# Django-Projekt absichern
# =============================================

## ✅ WAS WURDE VERBESSERT:
===========================

✅ SECRET_KEY ausgelagert (nicht mehr im Code)
✅ Umgebungsvariablen für sensible Daten
✅ DEBUG-Modus-Handling (Development vs. Production)
✅ ALLOWED_HOSTS richtig konfiguriert
✅ HTTPS-Erzwingung für Produktion
✅ Security Headers (XSS, Clickjacking, HSTS)
✅ Sichere Cookie-Einstellungen
✅ Logging-System für Fehler
✅ PostgreSQL-Support (empfohlen für Produktion)
✅ .gitignore zum Schutz sensibler Daten


## 📦 DATEIEN, DIE SIE ERHALTEN HABEN:
======================================

1. **settings_secure.py** - Verbesserte settings.py
2. **env_example.txt** - Beispiel für .env Datei
3. **generate_secret_key.py** - Tool zum Generieren eines SECRET_KEY
4. **gitignore_example.txt** - .gitignore für Ihr Projekt
5. **security_checklist.md** - Checkliste vor Deployment


## 🎯 SCHRITT-FÜR-SCHRITT-ANLEITUNG:
=====================================

### SCHRITT 1: Backup erstellen
--------------------------------

**WICHTIG:** Bevor Sie Änderungen vornehmen!

1. Kopieren Sie Ihre komplette Projekt-Ordner als Backup
2. Oder committen Sie alles in Git (falls Sie Git nutzen)

```bash
# Git Backup
git add .
git commit -m "Backup vor Sicherheits-Updates"
```


### SCHRITT 2: .gitignore erstellen/aktualisieren
--------------------------------------------------

1. Öffnen Sie (oder erstellen Sie): `.gitignore` im Hauptordner

2. Kopieren Sie den Inhalt aus `gitignore_example.txt`

3. Speichern Sie die Datei

**Zweck:** Verhindert, dass sensible Dateien (.env, Passwörter) in Git landen!


### SCHRITT 3: .env Datei erstellen
------------------------------------

1. Erstellen Sie eine neue Datei: `.env` im Hauptordner (neben manage.py)

2. Kopieren Sie den Inhalt aus `env_example.txt`

3. **Neuen SECRET_KEY generieren:**

   **Option A - Mit Python-Script:**
   ```bash
   python generate_secret_key.py
   ```
   Kopieren Sie den generierten Key

   **Option B - Online:**
   - Gehen Sie zu: https://djecrety.ir/
   - Kopieren Sie den generierten Key

4. Füllen Sie die .env Datei aus:

```env
# Django Sicherheit
SECRET_KEY=IHR-GENERIERTER-KEY-HIER
DEBUG=False
ALLOWED_HOSTS=123-kroatien.eu,www.123-kroatien.eu

# Email
EMAIL_HOST_USER=ihre-email@gmail.com
EMAIL_HOST_PASSWORD=ihr-app-passwort

# Optional: Datenbank (wenn Sie PostgreSQL nutzen)
DB_NAME=immobilien_kroatien
DB_USER=immobilien_user
DB_PASSWORD=sicheres-passwort
```

5. **WICHTIG:** .env sollte in .gitignore sein (Schritt 2)!


### SCHRITT 4: settings.py ersetzen
------------------------------------

1. **Backup der alten settings.py:**
   ```bash
   cp realstate/settings.py realstate/settings_old.py
   ```

2. **Ersetzen Sie** `realstate/settings.py` mit dem Inhalt aus `settings_secure.py`

3. **Prüfen Sie die Pfade:**
   - Stellen Sie sicher, dass `realstate/` der richtige Ordner ist
   - Falls Ihr Projekt-Ordner anders heißt, passen Sie an


### SCHRITT 5: python-dotenv installieren
------------------------------------------

Damit Django die .env Datei lesen kann:

```bash
pip install python-dotenv
```

Dann fügen Sie am **Anfang** von `settings.py` hinzu:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
# ... rest of settings
```

**Alternative ohne python-dotenv:**
Sie können auch direkt Umgebungsvariablen setzen:

```bash
# Linux/Mac
export SECRET_KEY="ihr-key"
export DEBUG="False"

# Windows CMD
set SECRET_KEY=ihr-key
set DEBUG=False

# Windows PowerShell
$env:SECRET_KEY="ihr-key"
$env:DEBUG="False"
```


### SCHRITT 6: Requirements aktualisieren
------------------------------------------

Fügen Sie zu `requirements.txt` hinzu:

```bash
python-dotenv==1.0.0
```

Und installieren:

```bash
pip install -r requirements.txt
```


### SCHRITT 7: Testen (Entwicklungs-Modus)
-------------------------------------------

1. **Setzen Sie DEBUG=True in .env** (für lokale Tests):
   ```env
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. **Server starten:**
   ```bash
   python manage.py runserver
   ```

3. **Prüfen Sie:**
   - ✅ Server startet ohne Fehler
   - ✅ Admin-Login funktioniert
   - ✅ Immobilien werden angezeigt
   - ✅ Keine Fehler in der Konsole

4. **Django Security Check:**
   ```bash
   python manage.py check --deploy
   ```
   Prüft Sicherheits-Einstellungen


### SCHRITT 8: Produktion vorbereiten
--------------------------------------

**Für Live-Server (Produktion):**

1. **.env für Produktion:**
   ```env
   DEBUG=False
   SECRET_KEY=ihr-produktions-secret-key
   ALLOWED_HOSTS=123-kroatien.eu,www.123-kroatien.eu
   
   SECURE_SSL_REDIRECT=True
   CSRF_COOKIE_SECURE=True
   SESSION_COOKIE_SECURE=True
   
   EMAIL_HOST_USER=ihre-produktions-email@gmail.com
   EMAIL_HOST_PASSWORD=ihr-app-passwort
   ```

2. **PostgreSQL einrichten** (empfohlen statt SQLite):
   
   In .env hinzufügen:
   ```env
   DB_NAME=immobilien_kroatien
   DB_USER=immobilien_user
   DB_PASSWORD=sehr-sicheres-passwort
   DB_HOST=localhost
   DB_PORT=5432
   ```

   PostgreSQL installieren:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # Python-Package
   pip install psycopg2-binary
   ```

3. **Static Files sammeln:**
   ```bash
   python manage.py collectstatic
   ```

4. **Migrations ausführen:**
   ```bash
   python manage.py migrate
   ```


### SCHRITT 9: HTTPS einrichten (SSL)
--------------------------------------

**Für Produktions-Server:**

1. **SSL-Zertifikat erhalten:**
   - Kostenlos: Let's Encrypt (https://letsencrypt.org/)
   - Oder von Ihrem Hosting-Provider

2. **Nginx/Apache konfigurieren:**
   - SSL-Zertifikat einbinden
   - HTTPS aktivieren
   - HTTP → HTTPS Weiterleitung

3. **In .env aktivieren:**
   ```env
   SECURE_SSL_REDIRECT=True
   ```


## 🔐 SICHERHEITS-FEATURES ERKLÄRT:
====================================

### 1. SECRET_KEY
- **Was:** Kryptographischer Schlüssel für Django
- **Warum:** Wird für Sessions, CSRF, Passwort-Hashing verwendet
- **Sicher:** In .env, nicht im Code!

### 2. DEBUG = False
- **Was:** Debug-Modus ausschalten
- **Warum:** Debug-Modus zeigt sensible Informationen (Stacktraces, Passwörter)
- **Produktion:** Immer False!

### 3. ALLOWED_HOSTS
- **Was:** Erlaubte Domain-Namen
- **Warum:** Schützt vor Host-Header-Attacken
- **Niemals:** '*' in Produktion!

### 4. HTTPS-Erzwingung
- **Was:** Alle Anfragen über HTTPS
- **Warum:** Schutz vor Man-in-the-Middle Attacken
- **Cookies:** Nur über HTTPS senden

### 5. Security Headers
- **XSS-Schutz:** Verhindert Cross-Site-Scripting
- **Clickjacking:** Verhindert iframe-Einbettung
- **HSTS:** Browser erzwingt HTTPS (1 Jahr)
- **Content-Type-Sniffing:** Verhindert MIME-Type-Attacken

### 6. CSRF-Schutz
- **Was:** Cross-Site Request Forgery Schutz
- **Warum:** Verhindert gefälschte Anfragen
- **Django:** Automatisch aktiviert

### 7. SQL-Injection-Schutz
- **Was:** Django ORM schützt automatisch
- **Niemals:** Raw SQL ohne Escaping!


## 🧪 TESTING:
===============

### Lokales Testing:

```bash
# Security Check
python manage.py check --deploy

# Sollte keine kritischen Warnungen zeigen
```

### Online Testing (nach Deployment):

1. **Security Headers:**
   - https://securityheaders.com/
   - Testen Sie Ihre Domain

2. **SSL-Konfiguration:**
   - https://www.ssllabs.com/ssltest/
   - Sollte A+ Rating haben


## 🐛 HÄUFIGE FEHLER:
=====================

**Fehler: "SECRET_KEY not found"**
→ Lösung:
  - .env Datei erstellt?
  - python-dotenv installiert?
  - load_dotenv() in settings.py?

**Fehler: "DisallowedHost at /"**
→ Lösung:
  - ALLOWED_HOSTS in .env korrekt?
  - Domain-Name richtig geschrieben?
  - Keine Anführungszeichen in .env!

**Fehler: "Static files not found"**
→ Lösung:
  - python manage.py collectstatic ausgeführt?
  - STATIC_ROOT korrekt konfiguriert?

**Fehler: HTTPS-Redirect-Loop**
→ Lösung:
  - SECURE_PROXY_SSL_HEADER korrekt?
  - Reverse Proxy (Nginx) richtig konfiguriert?


## 📝 CHECKLISTE VOR DEPLOYMENT:
=================================

Verwenden Sie: `security_checklist.md`

**KRITISCH:**
- [ ] SECRET_KEY in .env
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS konfiguriert
- [ ] .env in .gitignore
- [ ] HTTPS aktiviert
- [ ] Email-Passwort in .env

**WICHTIG:**
- [ ] PostgreSQL statt SQLite
- [ ] Logging aktiviert
- [ ] Backups eingerichtet
- [ ] Security Check ausgeführt


## 💡 TIPPS:
=============

1. **Niemals .env committen!**
   - Prüfen Sie .gitignore
   - `git status` vor jedem Commit

2. **Verschiedene .env für Dev/Prod:**
   - `.env.development` (lokal)
   - `.env.production` (Server)

3. **Regelmäßige Updates:**
   ```bash
   pip list --outdated
   pip install --upgrade django
   ```

4. **Backups automatisieren:**
   - Datenbank täglich sichern
   - Media-Dateien wöchentlich

5. **Monitoring einrichten:**
   - Sentry für Fehler-Tracking
   - Uptime-Monitoring


## 🚀 DEPLOYMENT:
==================

Nach diesen Sicherheits-Updates:

1. **Code auf Server deployen**
2. **.env auf Server erstellen** (nicht mit Git!)
3. **Requirements installieren**
4. **Migrations ausführen**
5. **Static Files sammeln**
6. **Server neu starten**
7. **Testen!**


## ✅ FERTIG!
==============

Ihr Django-Projekt ist jetzt sicherer!

**Was Sie erreicht haben:**
✅ Sensible Daten geschützt
✅ HTTPS erzwungen
✅ Security Headers aktiviert
✅ Produktionsreife Konfiguration
✅ Logging eingerichtet


## 📞 SUPPORT:
===============

Bei Fragen:
1. `python manage.py check --deploy` ausführen
2. Logs prüfen: `logs/django_errors.log`
3. .env Datei prüfen (Syntax korrekt?)
4. Browser-Konsole (F12) auf Fehler prüfen
