#!/usr/bin/env python3
"""
Generiert alle 96 Marktberichte (8 Regionen × 12 Sprachen)
Geschätzte Zeit: ~20-30 Minuten
Geschätzte Kosten: ~$2-3
"""

import os
import json
import time
from datetime import datetime
from main.market_reports import generate_market_report, REGIONS, LANGUAGES

def main():
    print("=" * 60)
    print("🏆 MARKTBERICHT-GENERATOR - KÖNIGSKLASSE")
    print("=" * 60)
    print(f"\n📊 8 Regionen × 12 Sprachen = 96 Berichte")
    print(f"⏱️  Geschätzte Zeit: ~20-30 Minuten")
    print(f"💰 Geschätzte Kosten: ~$2-3\n")
    
    # Output-Verzeichnis erstellen
    output_dir = 'main/market_reports_data'
    os.makedirs(output_dir, exist_ok=True)
    
    year = 2025
    total = len(REGIONS) * len(LANGUAGES)
    count = 0
    success = 0
    failed = []
    
    start_time = time.time()
    
    for region_key, region in REGIONS.items():
        print(f"\n{'='*50}")
        print(f"📍 Region: {region['name_de']}")
        print(f"{'='*50}")
        
        for lang_code, lang_config in LANGUAGES.items():
            count += 1
            print(f"\n[{count}/{total}] 🌍 {lang_code.upper()}...", end=" ")
            
            try:
                report = generate_market_report(region_key, lang_code, year)
                
                if report:
                    # Speichern
                    filename = f"{region_key}_{year}_{lang_code}.json"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(report, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ {filename}")
                    success += 1
                else:
                    print("❌ Fehler")
                    failed.append(f"{region_key}_{lang_code}")
                    
            except Exception as e:
                print(f"❌ {e}")
                failed.append(f"{region_key}_{lang_code}")
            
            # Pause für API-Rate-Limit
            time.sleep(1.5)
    
    # Zusammenfassung
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"✅ Erfolgreich: {success}/{total}")
    print(f"❌ Fehlgeschlagen: {len(failed)}")
    print(f"⏱️  Dauer: {minutes} Min {seconds} Sek")
    print(f"💾 Gespeichert in: {output_dir}/")
    
    if failed:
        print(f"\n⚠️  Fehlgeschlagene Berichte:")
        for f in failed:
            print(f"   - {f}")
    
    print("\n🎉 FERTIG!")
    print("=" * 60)

if __name__ == "__main__":
    main()
