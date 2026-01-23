# 🏠 PROJEKT-SITEMAP & ÜBERSICHT
## Kroatien Immobilienportal (123-kroatien.eu)
**Stand:** Dezember 2024 | **Django 4.2.1** | **12 Sprachen**

---

## 🌍 SPRACH-ÜBERSICHT

| Code | Sprache | Land-Slug | Glossar-Pfad |
|------|---------|-----------|--------------|
| `ge` | Deutsch | kroatien | glossar |
| `en` | English | croatia | glossary |
| `hr` | Hrvatski | hrvatska | pojmovnik |
| `fr` | Français | croatie | glossaire |
| `nl` | Nederlands | kroatie | woordenlijst |
| `pl` | Polski | chorwacja | slownik |
| `cz` | Čeština | chorvatsko | glosar |
| `sk` | Slovenčina | chorvatsko | slovnik |
| `ru` | Русский | horvatiya | glossarij |
| `gr` | Ελληνικά | kroatia | glossari |
| `sw` | Svenska | kroatien | ordlista |
| `no` | Norsk | kroatia | ordliste |

---

## 📍 KOMPLETTE URL-STRUKTUR

### 🏠 HAUPTSEITEN (Öffentlich)

| URL | View | Template | Beschreibung |
|-----|------|----------|--------------|
| `/` | `home` | `main/home.html` | Startseite mit Immobilien-Suche |
| `/listing/` | `listings` | `main/listings.html` | Alle Immobilien (Alias: `/listings/`) |
| `/property-details/<id>/` | `single_details` | `main/single-detail-modern.html` | Immobilien-Detailseite |
| `/blog/` | `blog` | `main/blog.html` | Blog-Übersicht |
| `/blog/single/` | `blog_single` | `main/blog-single.html` | Blog-Artikel |
| `/contact/` | `contact` | `main/contact.html` | Kontaktseite |
| `/about/` | `about` | `main/about-us.html` | Über uns |
| `/faq/` | `faq` | `main/faq.html` | Häufige Fragen (12 Sprachen) |
| `/service` | `service` | `main/service.html` | Dienstleistungen |
| `/sitemap` | `sitemap` | `main/sitemap.html` | Visuelle Sitemap |

### 📖 RECHTLICHES (Öffentlich)

| URL | View | Template | Beschreibung |
|-----|------|----------|--------------|
| `/imprint/` | `imprint` | `main/imprint.html` | Impressum |
| `/data-protection/` | `data_protection` | `main/data-protection.html` | Datenschutz |
| `/agb` | `agb` | `main/agb.html` | AGB |
| `/cancellation-policy` | `cancellation_policy` | `main/cancellation-policy.html` | Widerrufsrecht |

---

### 📚 GLOSSAR (SEO-Fokus, 12 Sprachen)

**URL-Schema:** `/{lang}/{country}/{glossar-segment}/`

| Seite | URL-Beispiel (DE) | Beschreibung |
|-------|-------------------|--------------|
| Index | `/ge/kroatien/glossar/` | Alle Begriffe A-Z mit Suche & Filter |
| Detail | `/ge/kroatien/glossar/{slug}/` | Einzelner Begriff mit FAQ |
| Investoren | `/ge/kroatien/glossar/investors/` | Landing: Investoren |
| Ferienimmobilien | `/ge/kroatien/glossar/holiday-properties/` | Landing: Ferienhäuser |
| Luxusimmobilien | `/ge/kroatien/glossar/luxury-real-estate/` | Landing: Luxus |
| Disclaimer | `/ge/kroatien/glossar/disclaimer/` | Haftungsausschluss |
| Käufer-Guide | `/ge/kroatien/glossar/buyer-guide/` | Leitfaden für Käufer |

**Glossar-Datenmodell:**
- `GlossaryTerm` → Sprachunabhängige Identität (canonical_key)
- `GlossaryTermTranslation` → 12 Übersetzungen pro Begriff
- `GlossaryTermAlias` → 301-Redirects für Synonyme
- `TermCategory` → Taxonomien (audience, topic, asset_type)

---

### 👤 BENUTZER-KONTEN

| URL | View | Beschreibung |
|-----|------|--------------|
| `/accounts/login` | `login_view` | Anmeldung |
| `/accounts/register` | `register` | Registrierung |
| `/accounts/logout` | `logout_view` | Abmeldung |
| `/accounts/dashboard` | `dashboard` | Benutzer-Dashboard |
| `/accounts/verify-email/` | `verifyEmail` | E-Mail-Verifizierung |
| `/accounts/verify-otp/` | `verifyOTP` | OTP-Verifizierung |

**Passwort-Reset (Sicher mit Token):**
| URL | View | Beschreibung |
|-----|------|--------------|
| `/accounts/password-reset/` | `password_reset_request` | Anfrage |
| `/accounts/password-reset/done/` | `password_reset_done` | Bestätigung |
| `/accounts/password-reset/confirm/<uidb64>/<token>/` | `password_reset_confirm` | Token-Link |
| `/accounts/password-reset/complete/` | `password_reset_complete` | Abgeschlossen |

---

### 🏢 MAKLER-PORTAL (Login erforderlich)

**Zugang:** Für `real_estate_agent` und `construction_company`

| URL | View | Beschreibung |
|-----|------|--------------|
| `/makler-dashboard/` | `makler_dashboard` | Übersicht aller Objekte |
| `/makler-portal/objekt/neu/` | `makler_objekt_neu` | Neues Objekt anlegen |
| `/makler-portal/objekt/<id>/bearbeiten/` | `makler_objekt_bearbeiten` | Objekt bearbeiten |
| `/makler-portal/xml-import/` | `makler_xml_import` | XML-Import |
| `/makler-portal/xml-dokumentation/` | `makler_xml_dokumentation` | XML-Dokumentation |
| `/makler-portal/anleitung/` | `makler_anleitung` | Bedienungsanleitung |

**API-Endpunkte (Makler):**
| URL | Methode | Beschreibung |
|-----|---------|--------------|
| `/api/makler/verkauft/<id>/` | POST | Status: Verkauft |
| `/api/makler/pausieren/<id>/` | POST | Status: Pausiert |
| `/api/makler/aktivieren/<id>/` | POST | Status: Aktiv |
| `/ge/api/m/gen/` | POST | KI-Textgenerierung |
| `/ge/api/m/gen/<id>/` | POST | KI-Text für Listing |

---

### 🏛️ PROFESSIONAL PORTAL (Gruppe B)

**Zugang:** Für `lawyer`, `tax_advisor`, `architect`

| URL | View | Beschreibung |
|-----|------|--------------|
| `/portal/dashboard/` | `dashboard_gruppe_b` | Dashboard |
| `/portal/profil/bearbeiten/` | `edit_profile` | Profil bearbeiten |
| `/portal/passwort-aendern/` | `change_password` | Passwort ändern |
| `/portal/2fa-einrichten/` | `setup_2fa` | 2FA aktivieren |
| `/portal/anleitung/` | `anleitung` | Bedienungsanleitung |

---

### 🗂️ PROFESSIONAL DIRECTORY (Öffentlich)

**URL-Schema (Deutsch):** `/ge/kroatien/{kategorie}/`
**URL-Schema (Kroatisch):** `/hr/hrvatska/{kategorija}/`

| Kategorie | DE-URL | HR-URL |
|-----------|--------|--------|
| Immobilienmakler | `/ge/kroatien/immobilienmakler/` | `/hr/hrvatska/agenti-za-nekretnine/` |
| Bauunternehmen | `/ge/kroatien/bauunternehmen/` | `/hr/hrvatska/gradevinske-tvrtke/` |
| Rechtsanwälte | `/ge/kroatien/rechtsanwaelte/` | `/hr/hrvatska/odvjetnici/` |
| Steuerberater | `/ge/kroatien/steuerberater/` | `/hr/hrvatska/porezni-savjetnici/` |
| Architekten | `/ge/kroatien/architekten/` | `/hr/hrvatska/arhitekti/` |

**Detail & Registrierung:**
| URL | Beschreibung |
|-----|--------------|
| `/ge/kroatien/{kategorie}/{slug}/` | Profil-Detailseite |
| `/ge/kroatien/registrierung/` | Professional-Registrierung DE |
| `/hr/hrvatska/registracija/` | Professional-Registrierung HR |
| `/ge/kroatien/partner-werden/` | Partner-Landing DE |
| `/hr/hrvatska/postanite-partner/` | Partner-Landing HR |

---

### 🔧 TECHNISCHE ENDPUNKTE

| URL | Beschreibung |
|-----|--------------|
| `/admin/` | Django Admin |
| `/ckeditor/` | CKEditor Upload |
| `/i18n/` | Django Sprachauswahl |
| `/set-language/<lang>/` | Sprache setzen |
| `/rss/listings/` | RSS-Feed Immobilien |
| `/sitemap.xml` | XML-Sitemap |
| `/robots.txt` | Robots.txt |

---

## 📊 DATENMODELLE

### Haupt-Models

| Model | App | Beschreibung |
|-------|-----|--------------|
| `Listing` | listings | Immobilien-Anzeigen |
| `Agent` | accounts | Makler (Legacy) |
| `Professional` | main | Alle Dienstleister (neu) |
| `ReferenceProject` | main | Referenzprojekte |
| `GlossaryTerm` | main | Glossar-Begriffe |
| `GlossaryTermTranslation` | main | Übersetzungen |
| `User` | Django Auth | Benutzer |
| `OTPVerification` | accounts | OTP für Verifizierung |

### Professional-Typen

| Typ | Portal-Zugang | Kann Objekte posten |
|-----|---------------|---------------------|
| `real_estate_agent` | Makler-Portal | ✅ Ja |
| `construction_company` | Makler-Portal | ✅ Ja |
| `lawyer` | Professional Portal | ❌ Nein (Directory) |
| `tax_advisor` | Professional Portal | ❌ Nein (Directory) |
| `architect` | Professional Portal | ❌ Nein (Directory) |

---

## 🎨 FRONTEND-STRUKTUR

### Templates Hierarchie
```
templates/
├── include/
│   ├── base.html          # Haupt-Layout (Navbar, Footer, Cookie-Banner)
│   ├── footer.html
│   └── card_*.html        # Immobilien-Karten
├── account/               # Login, Signup, Password Reset
├── main/                  # Hauptseiten
├── glossary/              # Glossar-Seiten
├── legal/                 # Rechtliche Seiten
├── makler_portal/         # Makler-Dashboard
└── professional_portal/   # Professionals-Dashboard
```

### CSS-Dateien
| Datei | Beschreibung |
|-------|--------------|
| `bootstrap.css` | Bootstrap Framework |
| `styles.css` | Haupt-Styles (Legacy) |
| `modern-theme.css` | Modernes Theme |
| `custom.css` | Eigene Anpassungen |
| `external.css` | Externe Styles |

---

## 🔐 SICHERHEITS-FEATURES

| Feature | Status | Beschreibung |
|---------|--------|--------------|
| HTTPS | ✅ Aktiv | SSL/TLS Verschlüsselung |
| CSRF-Schutz | ✅ Aktiv | Django Standard |
| XSS-Schutz | ✅ Aktiv | Security Headers |
| 2FA | ✅ Verfügbar | TOTP & E-Mail Code |
| Token-basierter Reset | ✅ Aktiv | Sicherer Passwort-Reset |
| Rate Limiting | ⚠️ Teilweise | Empfohlen für Login |

---

## 🔄 MIDDLEWARE & FEATURES

| Middleware | Status | Beschreibung |
|------------|--------|--------------|
| `RedirectRegistryMiddleware` | ✅ Aktiv | DB-basierte 301-Redirects |
| `SmartRedirectMiddleware` | ✅ Aktiv | Intelligente URL-Umleitung |
| Custom 404 Handler | ✅ Aktiv | Smart-404 mit Vorschlägen |

---

## 📁 DATEI-STRUKTUR

```
real-estate-django-main/
├── accounts/              # Benutzer-Verwaltung
├── contacts/              # Kontaktformulare
├── listings/              # Immobilien-Anzeigen
├── main/                  # Hauptlogik
│   ├── glossary_*.py      # Glossar-System
│   ├── professional_*.py  # Professional-System
│   ├── makler_views.py    # Makler-Portal
│   └── middleware/        # Custom Middleware
├── pages/                 # Statische Seiten
├── realtors/              # Makler (Legacy)
├── realstate/             # Django Settings
├── static/                # CSS, JS, Images
├── templates/             # HTML Templates
├── locale/                # Übersetzungen
├── fixtures/              # Seed-Daten
└── manage.py
```

---

## 🚀 DEPLOYMENT

| Umgebung | Status | URL |
|----------|--------|-----|
| Entwicklung | ✅ Aktiv | localhost:8000 |
| Produktion | 🎯 Ziel | 123-kroatien.eu |

**Render.yaml:** Konfiguriert für Render.com Deployment

---

## 📈 SEO-FEATURES

| Feature | Status | Beschreibung |
|---------|--------|--------------|
| Hreflang Tags | ✅ Aktiv | Auf Glossar-Seiten |
| JSON-LD | ✅ Aktiv | Strukturierte Daten |
| Sitemaps | ✅ Aktiv | `/sitemaps/glossary.xml` |
| 301 Redirects | ✅ Aktiv | Alias-System |
| Meta-Tags | ✅ Aktiv | Title, Description |
| Canonical URLs | ✅ Aktiv | Auf Glossar-Seiten |

---

## 📝 BEKANNTE TECHNISCHE SCHULDEN

| Problem | Priorität | Beschreibung |
|---------|-----------|--------------|
| Django Migrations | 🔴 Hoch | Instabil wegen Professional-Models |
| CSS-Konflikte | 🟡 Mittel | Inline vs. Global Styles |
| URL-Übersetzungen | 🟡 Mittel | Einige Pfade nicht übersetzt |
| Glossar-Slugs | 🟢 Niedrig | RU/GR haben numerische Slugs |

---

*Generiert am: Dezember 2024*
*Django Version: 4.2.1*
*Python Version: 3.8+*
