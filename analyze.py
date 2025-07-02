import csv
import os
from datetime import datetime

DATUM_FORMAT = "%d. %B %Y, %H:%M:%S"
MONATE = {
    "Januar": "January", "Februar": "February", "März": "March",
    "April": "April", "Mai": "May", "Juni": "June",
    "Juli": "July", "August": "August", "September": "September",
    "Oktober": "October", "November": "November", "Dezember": "December"
}
BLACKLIST = {""}
# Directory for the logfiles 
PFAD = "2/"

def ersetze_monat(datum_str):
    """Ersetzt deutsche Monatsnamen durch englische für datetime parsing."""
    for de, en in MONATE.items():
        if de in datum_str:
            return datum_str.replace(de, en)
    return datum_str

def verarbeite_datei(dateipfad):
    """
    Verarbeitet eine CSV-Logdatei und extrahiert Statistiken.
    Unterstützt verschiedene Kodierungen und robuste Gast-Erkennung.
    """
    gaeste_ips = set()
    nutzer = set()
    kursname = ""
    fruehestes_datum = None
    
    # Verschiedene Gast-Bezeichnungen definieren
    gast_begriffe = ['gast', 'guest user', 'guest']
    
    # Verschiedene Kodierungen ausprobieren
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(dateipfad, encoding=encoding) as f:
                reader = csv.reader(f, delimiter=',')
                next(reader, None)  # Kopfzeile überspringen
                
                for row in reader:
                    if len(row) <= 2:
                        continue
                    
                    # Datum extrahieren und vergleichen
                    datum_str = ersetze_monat(row[0])
                    try:
                        aktuelles_datum = datetime.strptime(datum_str, DATUM_FORMAT)
                        if fruehestes_datum is None or aktuelles_datum < fruehestes_datum:
                            fruehestes_datum = aktuelles_datum
                    except Exception:
                        pass  # Fehlerhafte Zeile ignorieren
                    
                    # Kursname extrahieren
                    if not kursname and len(row) > 3 and 'Kurs:' in row[3]:
                        kursname = row[3].replace("Kurs:", "").strip()
                    
                    # Gäste und Nutzer*innen zählen - OPTIMIERT
                    if any(begriff in row[1].lower() for begriff in gast_begriffe):
                        # IP-Adresse für eindeutige Gast-Zählung (falls verfügbar)
                        if len(row) > 8:
                            gaeste_ips.add(row[8])
                        else:
                            gaeste_ips.add(row[1])  # Fallback auf Benutzername
                    else:
                        loginname = row[1]
                        if loginname not in BLACKLIST and len(loginname) > 4:
                            nutzer.add(loginname)
                
                print(f"Erfolgreich gelesen mit Kodierung: {encoding}")
                break
                
        except UnicodeDecodeError:
            print(f"Kodierung {encoding} fehlgeschlagen für {dateipfad}, versuche nächste...")
            continue
        except Exception as e:
            print(f"Fehler mit Kodierung {encoding} für {dateipfad}: {e}")
            continue
    else:
        raise ValueError(f"Konnte keine passende Kodierung für {dateipfad} finden")
    
    return fruehestes_datum, kursname, len(gaeste_ips), len(nutzer)

def main():
    """
    Hauptfunktion: Verarbeitet alle CSV-Dateien im Verzeichnis und exportiert Ergebnisse.
    """
    print(f"Verarbeite Dateien aus Verzeichnis: {PFAD}")
    
    if not os.path.exists(PFAD):
        print(f"Verzeichnis {PFAD} existiert nicht!")
        return
    
    csv_dateien = [f for f in os.listdir(PFAD) if f.endswith('.csv')]
    
    if not csv_dateien:
        print(f"Keine CSV-Dateien in {PFAD} gefunden!")
        return
    
    print(f"Gefunden: {len(csv_dateien)} CSV-Dateien")
    print("-" * 60)
    
    with open('export.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        # Header schreiben
        writer.writerow(['Datum', 'Kurs', 'Gäste', 'Nutzer'])
        
        gesamt_gaeste = 0
        gesamt_nutzer = 0
        verarbeitete_dateien = 0
        
        for dateiname in csv_dateien:
            dateipfad = os.path.join(PFAD, dateiname)
            try:
                datum, kurs, gaeste, nutzer = verarbeite_datei(dateipfad)
                print(f"{dateiname}: Gäste={gaeste}, Nutzer={nutzer}, Kurs='{kurs}'")
                writer.writerow([datum, kurs, gaeste, nutzer])
                
                gesamt_gaeste += gaeste
                gesamt_nutzer += nutzer
                verarbeitete_dateien += 1
                
            except Exception as e:
                print(f"FEHLER bei {dateiname}: {e}")
                continue
        
        print("-" * 60)
        print(f"Verarbeitete Dateien: {verarbeitete_dateien}/{len(csv_dateien)}")
        print(f"Gesamt: Gäste={gesamt_gaeste}, Nutzer={gesamt_nutzer}")
        print(f"Export nach 'export.csv' abgeschlossen!")

if __name__ == "__main__":
    main()
