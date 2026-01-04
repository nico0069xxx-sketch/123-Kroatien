# ==============================================
# INSTALLATIONS-ANLEITUNG: SMS-OTP ZWEI-FAKTOR-AUTHENTIFIZIERUNG
# Makler-Registrierung mit Email + SMS Verifizierung
# ==============================================

## ✅ WAS WURDE ENTWICKELT:
===========================

✅ **Zwei-Faktor-Authentifizierung:**
   1. Email-OTP (wie bisher)
   2. SMS-OTP (neu, über Twilio)

✅ **Mobilnummer Pflichtfeld** bei Registrierung

✅ **SMS-OTP beim Login** (zusätzliche Sicherheit)

✅ **Twilio-Integration** (SMS-Versand)

✅ **Rate-Limiting** (Schutz vor Missbrauch)

✅ **Fehlerbehandlung** (OTP abgelaufen, zu viele Versuche, etc.)


## 📦 DATEIEN, DIE SIE ERHALTEN HABEN:
======================================

1. **sms_service.py** - SMS-Service mit Twilio
2. **accounts_models_extended.py** - Erweiterte Models (SMSOTPVerification)
3. **accounts_views_with_sms.py** - Views mit SMS-OTP-Logik
4. **template_verifySMS.html** - Template für SMS-Verifizierung
5. **INSTALLATIONS_ANLEITUNG_SMS_OTP.md** (diese Datei)


## 🎯 ABLAUF DER REGISTRIERUNG:
================================

### **Schritt 1: Registrierungsformular**
- Makler füllt Formular aus
- **Mobilnummer ist PFLICHTFELD** (kroatisch: +385...)
- Formular wird validiert

### **Schritt 2: Email-OTP**
- 6-stelliger Code wird per Email gesendet
- Makler gibt Code ein
- Email wird verifiziert

### **Schritt 3: SMS-OTP**
- 6-stelliger Code wird per SMS gesendet
- Makler gibt Code ein
- Mobilnummer wird verifiziert

### **Schritt 4: Account aktiviert**
- Beide Verifizierungen erfolgreich
- Makler-Account ist aktiv
- Login möglich


## 🔐 ABLAUF BEIM LOGIN:
=========================

### **Schritt 1: Passwort-Eingabe**
- Makler gibt Username/Email + Passwort ein
- Passwort wird geprüft

### **Schritt 2: SMS-OTP**
- 6-stelliger Code wird per SMS gesendet
- Makler gibt Code ein
- Login erfolgreich


## 📋 SCHRITT-FÜR-SCHRITT-INSTALLATION:
========================================

### SCHRITT 1: Twilio-Account erstellen
----------------------------------------

1. **Gehen Sie zu:** https://www.twilio.com/try-twilio

2. **Registrieren Sie sich:**
   - Email-Adresse
   - Passwort
   - Firmenname: "123 Kroatien Immobilien"

3. **Verifizieren Sie Ihre Email** (Bestätigungsmail von Twilio)

4. **Verifizieren Sie Ihre Telefonnummer** (wird von Twilio gefordert)

5. **Kostenloses Testguthaben erhalten** (~$15)


### SCHRITT 2: Twilio-Credentials holen
----------------------------------------

Nach der Registrierung sehen Sie Ihr Twilio-Dashboard:

1. **Account SID** (finden Sie auf dem Dashboard)
   - Sieht aus wie: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

2. **Auth Token** (finden Sie auf dem Dashboard)
   - Klicken Sie auf "Show" um ihn zu sehen
   - Sieht aus wie: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Telefonnummer kaufen:**
   - Im Twilio-Dashboard: "Phone Numbers" → "Buy a Number"
   - Wählen Sie ein Land (Kroatien oder International)
   - Wählen Sie eine Nummer mit SMS-Fähigkeit
   - "Buy" klicken (kostet ~$1-2/Monat)
   - Ihre Nummer: z.B. `+385...` oder `+1...`


### SCHRITT 3: Python-Pakete installieren
------------------------------------------

```bash
# Twilio SDK installieren
pip install twilio==8.10.0

# Requirements aktualisieren
pip freeze > requirements.txt
```


### SCHRITT 4: .env Datei aktualisieren
----------------------------------------

Öffnen Sie Ihre `.env` Datei und fügen Sie hinzu:

```env
# Twilio SMS-Service
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+385xxxxxxxxx

# Oder falls Sie internationale Nummer haben:
# TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
```

**WICHTIG:** Ersetzen Sie die XXX mit Ihren echten Twilio-Credentials!


### SCHRITT 5: settings.py aktualisieren
-----------------------------------------

Öffnen Sie `realstate/settings.py` und fügen Sie hinzu:

```python
# Twilio SMS-Konfiguration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
```


### SCHRITT 6: Models aktualisieren
------------------------------------

1. **Öffnen Sie:** `accounts/models.py`

2. **Fügen Sie das neue Model hinzu** (am Ende der Datei):

```python
class SMSOTPVerification(models.Model):
    """SMS-OTP-Verifizierung"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'SMS OTP Verifications'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() - self.sent_at > timedelta(minutes=5)
```

3. **Migrations erstellen:**

```bash
python manage.py makemigrations
python manage.py migrate
```


### SCHRITT 7: SMS-Service erstellen
-------------------------------------

1. **Erstellen Sie:** `accounts/sms_service.py`

2. **Kopieren Sie** den kompletten Inhalt aus `sms_service.py`


### SCHRITT 8: Views aktualisieren
-----------------------------------

1. **Backup erstellen:**
```bash
cp accounts/views.py accounts/views_backup.py
```

2. **Ersetzen Sie** die Views:
   - `register()` mit der neuen Version
   - `verifyEmail()` mit der neuen Version
   - `login_view()` mit der neuen Version
   
3. **Fügen Sie neue Views hinzu:**
   - `verify_sms()`
   - `verify_login_sms()`

(Siehe `accounts_views_with_sms.py` für den vollständigen Code)


### SCHRITT 9: URLs aktualisieren
----------------------------------

Öffnen Sie `accounts/urls.py` und fügen Sie hinzu:

```python
urlpatterns = [
    # ... bestehende URLs ...
    
    # NEU: SMS-OTP URLs
    path('verify-sms/', views.verify_sms, name='verify_sms'),
    path('verify-login-sms/', views.verify_login_sms, name='verify_login_sms'),
]
```


### SCHRITT 10: Templates erstellen
------------------------------------

1. **Erstellen Sie:** `templates/account/verifySMS.html`

2. **Kopieren Sie** den Inhalt aus `template_verifySMS.html`

3. **Erstellen Sie:** `templates/account/verifyLoginSMS.html`

4. **Kopieren Sie** den gleichen Inhalt (verifySMS.html), ändern Sie nur:
   - `{% url 'account:verify_sms' %}` → `{% url 'account:verify_login_sms' %}`


### SCHRITT 11: Registrierungs-Template anpassen
-------------------------------------------------

Öffnen Sie `templates/account/signup.html` und fügen Sie das Mobilnummer-Feld hinzu:

```html
<!-- Nach dem Email-Feld -->
<div class="form-group">
    <label for="mobile">Mobilnummer *</label>
    <input 
        type="tel" 
        class="form-control" 
        id="mobile" 
        name="mobile" 
        placeholder="+385 91 234 5678"
        required
        pattern="^\+?385[0-9]{8,10}$"
    >
    <small class="form-text text-muted">
        Kroatische Mobilnummer (z.B. +385 91 234 5678)
    </small>
</div>
```


### SCHRITT 12: Testen (mit Twilio Test-Modus)
-----------------------------------------------

**WICHTIG:** Im Twilio Test-Modus können Sie NUR an verifizierte Nummern SMS senden!

1. **Verifizieren Sie Ihre Test-Nummer:**
   - Twilio Dashboard → Phone Numbers → Verified Caller IDs
   - Fügen Sie Ihre Mobilnummer hinzu
   - Verifizierungscode eingeben

2. **Server starten:**
```bash
python manage.py runserver
```

3. **Testen Sie die Registrierung:**
   - Gehen Sie zu `/accounts/register`
   - Füllen Sie das Formular aus
   - **WICHTIG:** Verwenden Sie Ihre verifizierte Nummer!
   - Email-OTP sollte ankommen
   - SMS-OTP sollte ankommen

4. **Prüfen Sie Twilio-Logs:**
   - Dashboard → Monitor → Logs → Messaging
   - Sehen Sie, ob SMS gesendet wurde


## 💰 TWILIO-KOSTEN:
=====================

### **Test-Modus (Kostenlos):**
- $15 Testguthaben inklusive
- Nur an verifizierte Nummern
- Perfekt zum Testen

### **Produktions-Modus:**
- SMS-Kosten: ~€0.07 pro SMS (Kroatien)
- Telefonnummer: ~€1-2 pro Monat
- Pay-as-you-go (nur bezahlen was Sie nutzen)

### **Beispiel-Rechnung:**
- 100 Registrierungen/Monat = 200 SMS (Email + Login) = ~€14
- Telefonnummer = €2
- **Total: ~€16/Monat**


## 🔧 TWILIO IN PRODUKTION AKTIVIEREN:
=======================================

Wenn Sie bereit sind live zu gehen:

1. **Twilio-Account upgraden:**
   - Dashboard → Billing
   - Kreditkarte hinzufügen
   - Auto-Recharge aktivieren (z.B. €20)

2. **Account verifizieren:**
   - Identität bestätigen (Twilio-Anforderung)
   - Geschäftsdokumente hochladen

3. **Produktions-Nummer:**
   - Sie können Ihre Test-Nummer behalten
   - Oder neue kaufen

4. **Test-Einschränkungen aufheben:**
   - Jetzt können SMS an ALLE Nummern gesendet werden


## 🐛 HÄUFIGE FEHLER:
=====================

**Fehler: "The number +385... is unverified"**
→ Lösung: Nummer in Twilio verifizieren (Verified Caller IDs)

**Fehler: "Unable to create record: The 'To' number is not a valid phone number"**
→ Lösung: 
  - Nummer muss mit + beginnen
  - Format: +385912345678
  - Keine Leerzeichen oder Bindestriche

**Fehler: "Authentication Error"**
→ Lösung:
  - TWILIO_ACCOUNT_SID korrekt in .env?
  - TWILIO_AUTH_TOKEN korrekt in .env?
  - Keine Leerzeichen oder Anführungszeichen!

**Fehler: SMS kommt nicht an**
→ Lösung:
  - Prüfen Sie Twilio-Logs (Dashboard → Logs)
  - Nummer verifiziert? (im Test-Modus)
  - Account-Guthaben vorhanden?


## ✅ CHECKLISTE:
=================

- [ ] Twilio-Account erstellt
- [ ] Account SID + Auth Token notiert
- [ ] Telefonnummer gekauft
- [ ] Test-Nummer verifiziert
- [ ] twilio Python-Package installiert
- [ ] .env mit Twilio-Credentials aktualisiert
- [ ] settings.py mit Twilio-Config aktualisiert
- [ ] SMSOTPVerification Model hinzugefügt
- [ ] Migrations ausgeführt
- [ ] sms_service.py erstellt
- [ ] Views aktualisiert (register, login, verify_sms)
- [ ] URLs aktualisiert
- [ ] Templates erstellt (verifySMS.html)
- [ ] Registrierungs-Formular mit Mobilnummer
- [ ] Server neu gestartet
- [ ] Mit Test-Nummer getestet
- [ ] Email-OTP funktioniert
- [ ] SMS-OTP funktioniert
- [ ] Login mit SMS-OTP funktioniert


## 🎉 FERTIG!
==============

Ihre Makler-Registrierung hat jetzt:
✅ Email-OTP-Verifizierung
✅ SMS-OTP-Verifizierung
✅ Zwei-Faktor-Authentifizierung beim Login
✅ Mobilnummer als Pflichtfeld
✅ Maximale Sicherheit!


## 📞 TWILIO SUPPORT:
=====================

- Dokumentation: https://www.twilio.com/docs/sms
- Support: https://support.twilio.com/
- API-Referenz: https://www.twilio.com/docs/api


## 💡 TIPPS:
=============

1. **Im Test-Modus bleiben** bis Sie sicher sind
2. **Twilio-Logs prüfen** bei Problemen
3. **Rate-Limiting** ist bereits eingebaut (2 Min)
4. **OTP-Gültigkeit** ist 5 Minuten
5. **Anzahl Versuche** limitiert (5 bei Registrierung, 3 beim Login)


## 🚀 NÄCHSTE SCHRITTE:
========================

1. **Jetzt:** Im Test-Modus mit verifizierten Nummern testen
2. **Dann:** Account upgraden für Produktion
3. **Optional:** SMS-Texte in mehreren Sprachen (aktuell Deutsch)
4. **Optional:** WhatsApp-Integration (Twilio unterstützt auch WhatsApp!)


Viel Erfolg! 🎉
