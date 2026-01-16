# 123-Kroatien.eu - Real Estate Portal

Django-basierter Immobilienmarktplatz fuer Kroatien mit 12-sprachiger Unterstuetzung.

## Tech Stack

- Django 4.2.1 (Python)
- Bootstrap 4 + jQuery (Frontend)
- SQLite (Development) / PostgreSQL (Production)
- Server-side rendered Templates

## Quick Start

### 1. Repository klonen

    git clone https://github.com/nico0069xxx-sketch/123-Kroatien.git
    cd 123-Kroatien

### 2. Virtual Environment erstellen

    python3 -m venv venv
    source venv/bin/activate

### 3. Dependencies installieren

    pip install -r requirements.txt

### 4. Environment konfigurieren

    cp .env.example .env
    # .env editieren und SECRET_KEY setzen

### 5. Datenbank migrieren

    python manage.py migrate

### 6. Server starten

    python manage.py runserver

Oeffne: http://localhost:8000/

## Tests

    python manage.py test

## CI/CD

GitHub Actions fuehrt bei jedem Push/PR aus:
- Syntax-Check (compileall)
- Django System Check
- Migration Check
- Unit Tests

## Governance

Siehe docs/ Ordner:
- STATE.md - Aktueller Projektstatus
- DECISIONS.md - Architektur-Entscheidungen
- HANDOFF.md - Session-Logs
