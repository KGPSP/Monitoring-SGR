# System Monitorowania Gotowości SGRW-N

## O Projekcie

System Monitorowania Gotowości SGRW-N to aplikacja testowa służąca do weryfikacji i monitorowania poziomu gotowości Specjalistycznych Grup Ratownictwa Wodno-Nurkowego. System umożliwia:

- Monitorowanie stanu gotowości grup SGRW-N
- Weryfikację spełnienia wymagań dla poziomów A, AB, ABC i ABCchem
- Wizualizację zasięgu czasowego grup na mapie
- Automatyczne wypełnianie minimalnych wymagań
- Porównywanie aktualnego stanu z wymaganiami rozkazów

### Główne Funkcjonalności

1. **Monitoring SGRW-N**
   - Wybór jednostki (KW PSP, KM/KP PSP, nazwa grupy)
   - Wprowadzanie aktualnego stanu osobowego i sprzętowego
   - Weryfikacja poziomu gotowości
   - Wizualizacja zasięgu czasowego na mapie

2. **Algorytmika SGRW-N**
   - Dokumentacja algorytmów weryfikacji gotowości
   - Specyfikacja wymagań dla poszczególnych poziomów
   - Opis zmiennych i struktur danych

3. **Mapa Zasięgu**
   - Wizualizacja lokalizacji jednostki
   - Okręgi zasięgu czasowego (5, 10, 15, 25, 60 minut)
   - Obliczenia bazujące na średniej prędkości pojazdu ciężarowego

## Wymagania Techniczne

```
streamlit==1.29.0
pandas==2.1.4
folium==0.15.0
streamlit-folium==0.15.0
numpy>=1.24.3
jinja2>=3.1.2
branca>=0.6.0
protobuf>=3.20.0
```

## Instalacja i Uruchomienie

1. Klonowanie repozytorium:
```bash
git clone [adres-repozytorium]
cd Monitoring-SGR
```

2. Instalacja zależności:
```bash
pip install -r requirements.txt
```

3. Uruchomienie aplikacji:
```bash
streamlit run app.py
```

## Kierownictwo Projektu

### st. bryg. Michał Kłosiński
* Komenda Główna Państwowej Straży Pożarnej
* Biuro Informatyki i Łączności
* Główny architekt systemu
* Odpowiedzialny za koncepcję i implementację algorytmów weryfikacji gotowości

### st. bryg. Marcin Kucharski
* Komenda Główna Państwowej Straży Pożarnej
* Biuro KCKR
* Ekspert ds. operacyjnych
* Odpowiedzialny za specyfikację wymagań operacyjnych

## Wsparcie Merytoryczne

Projekt powstał przy współpracy z:
* Krajowym Centrum Koordynacji Ratownictwa i Ochrony Ludności KG PSP
* Wydziałem Informatyki i Łączności KG PSP
* Specjalistycznymi Grupami Ratownictwa Wodno-Nurkowego

## Status Projektu

⚠️ **UWAGA**: To jest wersja testowa systemu, służąca do weryfikacji algorytmów i koncepcji. Nie należy używać w środowisku produkcyjnym.

## Licencja

© 2024 Komenda Główna Państwowej Straży Pożarnej. Wszelkie prawa zastrzeżone.

---

*System został opracowany w ramach projektu modernizacji systemów informatycznych wspierających działania ratownicze Państwowej Straży Pożarnej.*
