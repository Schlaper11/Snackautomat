# Snackautomat

`main.py` enthält ein MicroPython-Beispiel für den Raspberry Pi Pico:

- Produktauswahl per Zahl (`1 = Cola`)
- Anzeige des Preises (`1,50 €`)
- Warten auf Geldeinwurf (Münzsignal)
- Motorsteuerung nach vollständiger Bezahlung

## Pin-Belegung

- Münzsignal: `GP14` (Eingang mit Pull-Up)
- Motorsteuerung: `GP15` (Ausgang)

## Start

1. `main.py` auf den Pico kopieren.
2. Pico mit Münzsignal und Motor-Treiber verbinden.
3. Script starten und Produktnummer eingeben.
