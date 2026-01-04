# TEST-BEISPIEL: So sieht das XML aus
# Dies ist ein Beispiel, wie Ihre XML-Schnittstelle aussehen wird

## BEISPIEL: OpenImmo XML
==========================

<?xml version="1.0" encoding="utf-8"?>
<openimmo xmlns="http://www.openimmo.de" 
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:schemaLocation="http://www.openimmo.de openimmo_127b.xsd">
  
  <uebertragung>
    <art>ONLINE</art>
    <umfang>VOLL</umfang>
    <modus>NEW</modus>
    <version>1.2.7</version>
    <sendersoftware>Kroatien Immobilien Marktplatz</sendersoftware>
    <senderversion>1.0</senderversion>
    <techn_email>office@123-kroatien.eu</techn_email>
    <timestamp>2025-01-04 20:00:00</timestamp>
  </uebertragung>
  
  <anbieter>
    <anbieternr>12345678901</anbieternr>
    
    <firma>
      <name>Immobilien Kroatien GmbH</name>
      <lizenzkennung>12345678901</lizenzkennung>
    </firma>
    
    <anhang>
      <anhangtitel>Logo</anhangtitel>
      <format>jpg</format>
      <daten>
        <pfad>https://IhreDomain.com/media/company/logo.jpg</pfad>
      </daten>
    </anhang>
    
    <immobilie>
      <verwaltung_techn>
        <objektnr_intern>1001</objektnr_intern>
        <objektnr_extern>uuid-123-456</objektnr_extern>
        <aktion>CHANGE</aktion>
        <aktiv_von>2025-01-01</aktiv_von>
        <openimmo_obid>uuid-123-456</openimmo_obid>
        <sprache>HRV</sprache>
      </verwaltung_techn>
      
      <objektkategorie>
        <nutzungsart>
          <wohnen HAUS="true"/>
        </nutzungsart>
        <vermarktungsart>
          <kauf kauf="true"/>
        </vermarktungsart>
        <objektart>
          <haus haustyp="EINFAMILIENHAUS"/>
        </objektart>
      </objektkategorie>
      
      <geo>
        <plz>21000</plz>
        <ort>Split</ort>
        <strasse>Obala Hrvatskog narodnog preporoda 10</strasse>
        <land iso_land="HRV"/>
        <regionaler_zusatz>Dalmatien</regionaler_zusatz>
      </geo>
      
      <kontaktperson>
        <name>Max Mustermann</name>
        <email_zentrale>max@immobilien-kroatien.eu</email_zentrale>
        <tel_handy>+385 91 123 4567</tel_handy>
        <firma>Immobilien Kroatien GmbH</firma>
      </kontaktperson>
      
      <preise>
        <kaufpreis>350000</kaufpreis>
        <waehrung iso_waehrung="EUR"/>
      </preise>
      
      <flaechen>
        <wohnflaeche>150.0</wohnflaeche>
        <grundstuecksflaeche>500</grundstuecksflaeche>
        <anzahl_zimmer>4</anzahl_zimmer>
        <anzahl_badezimmer>2</anzahl_badezimmer>
      </flaechen>
      
      <ausstattung>
        <anzahl_stellplaetze>2</anzahl_stellplaetze>
      </ausstattung>
      
      <freitexte>
        <objekttitel>Wunderschönes Haus mit Meerblick in Split</objekttitel>
        <objektbeschreibung>
          Traumhafte Villa direkt am Meer mit herrlichem Panoramablick.
          Das Haus verfügt über 4 Schlafzimmer, 2 Badezimmer, moderne Küche
          und großen Garten. Perfekt für Familien!
        </objektbeschreibung>
        <lage>Split, Dalmatien - Kroatien</lage>
      </freitexte>
      
      <anhang>
        <anhangtitel>Hauptbild</anhangtitel>
        <format>jpg</format>
        <gruppe>BILD</gruppe>
        <daten>
          <pfad>https://IhreDomain.com/media/photos/2025/01/04/hauptbild.jpg</pfad>
        </daten>
      </anhang>
      
      <anhang>
        <anhangtitel>Bild 1</anhangtitel>
        <format>jpg</format>
        <gruppe>BILD</gruppe>
        <daten>
          <pfad>https://IhreDomain.com/media/photos/2025/01/04/bild1.jpg</pfad>
        </daten>
      </anhang>
      
    </immobilie>
    
  </anbieter>
  
</openimmo>


## BEISPIEL: Einfaches XML
============================

<?xml version="1.0" encoding="utf-8"?>
<listings version="1.0" generated="2025-01-04T20:00:00" count="1">
  
  <listing id="uuid-123-456" published="true">
    <property_id>1001</property_id>
    <title>Wunderschönes Haus mit Meerblick in Split</title>
    <description>Traumhafte Villa direkt am Meer mit herrlichem Panoramablick...</description>
    <type>House</type>
    <status>For Sale</status>
    <location>Split, Dalmatien - Kroatien</location>
    
    <price currency="EUR">350000</price>
    
    <details>
      <bedrooms>4</bedrooms>
      <bathrooms>2</bathrooms>
      <floors>2</floors>
      <garage>2</garage>
      <area>500</area>
      <size>150.0</size>
    </details>
    
    <address>
      <street>Obala Hrvatskog narodnog preporoda 10</street>
      <city>Split</city>
      <state>Dalmatien</state>
      <zipcode>21000</zipcode>
      <country>Croatia</country>
      <neighborhood>Altstadt</neighborhood>
    </address>
    
    <agent>
      <name>Max Mustermann</name>
      <email>max@immobilien-kroatien.eu</email>
      <company>Immobilien Kroatien GmbH</company>
      <oib_number>12345678901</oib_number>
      <domain>immobilien-kroatien.eu</domain>
      <phone>+385 91 123 4567</phone>
    </agent>
    
    <images>
      <image type="main">https://IhreDomain.com/media/photos/2025/01/04/hauptbild.jpg</image>
      <image type="photo_1">https://IhreDomain.com/media/photos/2025/01/04/bild1.jpg</image>
      <image type="photo_2">https://IhreDomain.com/media/photos/2025/01/04/bild2.jpg</image>
    </images>
    
    <video_url>https://www.youtube.com/watch?v=example</video_url>
    <list_date>2025-01-01T10:00:00</list_date>
  </listing>
  
</listings>


## WIE MAKLER DAS XML NUTZEN:
==============================

1. **Immobilien-Portale**
   Makler geben die XML-URL in Portale wie:
   - Immoscout24
   - ImmoWelt
   - Lokale kroatische Portale
   
2. **Automatischer Import**
   Die Portale rufen die URL regelmäßig auf (z.B. täglich)
   und importieren automatisch neue/geänderte Immobilien

3. **Mehrere Portale gleichzeitig**
   Ein Makler kann seine XML-URL an mehrere Portale geben
   und alle werden automatisch synchronisiert


## VORTEILE FÜR IHRE MAKLER:
==============================

✅ Einmal Immobilie eintragen → überall verfügbar
✅ Automatische Updates ohne manuellen Upload
✅ Standard-Format = kompatibel mit allen Portalen
✅ Zeit- und Kostenersparnis
✅ Kroatische OIB-Nummer enthalten (rechtlich korrekt)
✅ Alle Bilder automatisch übertragen
