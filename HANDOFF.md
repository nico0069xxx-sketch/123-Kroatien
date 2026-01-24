# Handoff - 24. Januar 2026 (Final)

## ✅ Erledigt (diese Session)
- Globaler Sprachumschalter für 12 Sprachen (P0 Bug)
- Hero-Übersetzungen wiederhergestellt
- Chatbot URL-Fix + zeigt jetzt Dienstleister-Karten mit Logo
- KI-Immobiliensuche funktioniert
- Expertenfinder aktiviert und funktioniert
- Cookie-Banner Übersetzungen
- Logo-Styling fix (object-fit: contain)
- **Security: translate.py nutzt jetzt .env statt hardcodierten Key**

## ⚠️ OFFEN: Sitemap 12-Sprach-Übersetzungen
Die Sitemap-Links sind nur in DE/EN/HR übersetzt:
- Immobilienmakler, Bauunternehmen, etc.
- Partner werden, Registrieren, Anmelden
- Glossar, Marktberichte, Nachrichten
- KI Schnellsuche, Expertenfinder
- "Sprachen" Label

**MUSS für alle 12 Sprachen übersetzt werden!**

## 📁 Wichtige Dateien
- `main/context_processors.py` - Übersetzungen & URL-Mapping
- `main/chatbot.py` - Chatbot mit KI-Matching
- `main/chatbot_views.py` - API gibt auch Professionals zurück
- `main/ki_matching.py` - Expertenfinder Logik
- `templates/main/sitemap.html` - BRAUCHT 12 SPRACHEN!
- `listings/translate.py` - Übersetzungen (jetzt sicher!)

## 🔑 Branch
`feature/glossary` - alle Commits gepusht
