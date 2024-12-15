# Algorytm Określania Poziomu Gotowości SGRW-N

## 1. Struktura Danych

### 1.1 Zmienne Wejściowe (Stan Grupy):
* `liczba_ratowników`: Liczba dostępnych strażaków/ratowników w grupie. (Typ: Integer)
* `liczba_młodszych_nurków`: Liczba dostępnych młodszych nurków. (Typ: Integer)
* `liczba_nurków`: Liczba dostępnych nurków. (Typ: Integer)
* `liczba_nurków_kierujących`: Liczba dostępnych nurków kierujących pracami podwodnymi. (Typ: Integer)
* `czy_sternik`: Czy jest dostępny sternik motorowodny lub stermotorzysta. (Typ: Boolean)
* `czy_strażak_logistyk`: Czy jest dostępny strażak obsługujący sprzęt logistyczny i pomocniczy. (Typ: Boolean)
* `czy_wyposazenie_abc_chem`: Czy jest dostępne wyposażenie ABC-chem. (Typ: Boolean)
* `liczba_slrr`: Liczba pojazdów SLRR/SLRW. (Typ: Integer)
* `liczba_lodzi`: Liczba łodzi. (Typ: Integer)
* `liczba_srchem`: Liczba pojazdów SRChem. (Typ: Integer)
* `czas_alarmowania`: Czas potrzebny od ogłoszenia alarmu do gotowości wyjazdu. (Typ: Integer, jednostka: minuty)

### 1.2 Dane Identyfikacyjne Grupy:
* `nr_id`: Numer identyfikacyjny grupy. (Typ: String)
* `nazwa_SGR`: Nazwa grupy specjalistycznej. (Typ: String)
* `kw`: Komenda Wojewódzka PSP. (Typ: String)
* `kp_km`: Komenda Powiatowa/Miejska PSP. (Typ: String)
* `gotowosc_rozkaz`: Poziom gotowości wskazany rozkazem. (Typ: String)
* `lat`: Szerokość geograficzna lokalizacji jednostki. (Typ: Float)
* `long`: Długość geograficzna lokalizacji jednostki. (Typ: Float)

## 2. Wymagania Minimalne dla Poziomów Gotowości

### 2.1 Poziom A:
* Minimalna liczba ratowników: 2
* Minimalna liczba młodszych nurków: 2
* Wymagany sternik: Tak
* Wymagany strażak logistyk: Tak
* Minimalna liczba SLRR/SLRW: 1
* Minimalna liczba łodzi: 1
* Czas alarmowania: Niezwłoczny

### 2.2 Poziom AB:
* Minimalna liczba ratowników: 3
* Minimalna liczba młodszych nurków: 2
* Minimalna liczba nurków kierujących: 1
* Wymagany sternik: Tak
* Wymagany strażak logistyk: Tak
* Minimalna liczba SLRR/SLRW: 1
* Minimalna liczba łodzi: 1
* Czas alarmowania: Niezwłoczny

### 2.3 Poziom ABC:
* Minimalna liczba ratowników: 5
* Minimalna liczba młodszych nurków: 2
* Minimalna liczba nurków: 2
* Minimalna liczba nurków kierujących: 1
* Wymagany sternik: Tak
* Wymagany strażak logistyk: Tak
* Minimalna liczba SLRR/SLRW: 2
* Minimalna liczba łodzi: 2
* Czas alarmowania: 60 minut

### 2.4 Poziom ABCchem:
* Minimalna liczba ratowników: 5
* Minimalna liczba młodszych nurków: 2
* Minimalna liczba nurków: 2
* Minimalna liczba nurków kierujących: 1
* Wymagany sternik: Tak
* Wymagany strażak logistyk: Tak
* Minimalna liczba SLRR/SLRW: 2
* Minimalna liczba łodzi: 2
* Minimalna liczba SRChem: 1
* Wyposażenie ABC-chem: Wymagane
* Czas alarmowania: 60 minut

## 3. Funkcjonalności Systemu

### 3.1 Interfejs Użytkownika:
1. Wybór jednostki:
   * Wybór Komendy Wojewódzkiej
   * Wybór Komendy Miejskiej/Powiatowej
   * Wybór nazwy grupy

2. Informacje o grupie:
   * Wyświetlanie numeru identyfikacyjnego
   * Wyświetlanie poziomu gotowości wskazanego rozkazem

3. Mapa zasięgu czasowego:
   * Wizualizacja lokalizacji jednostki
   * Okręgi zasięgu czasowego:
     - 5 minut (czerwony)
     - 10 minut (pomarańczowy)
     - 15 minut (żółto-pomarańczowy)
     - 25 minut (żółto-pomarańczowy jasny)
     - 60 minut (żółty)
   * Obliczenia bazują na średniej prędkości 60 km/h dla pojazdu ciężarowego

4. Wprowadzanie danych:
   * Dane osobowe (ratownicy, nurkowie)
   * Dane sprzętowe (pojazdy, łodzie)
   * Dane czasowe (czas alarmowania)

### 3.2 Funkcje Sprawdzające:
1. Sprawdzanie poziomu gotowości:
   * Weryfikacja spełnienia wymagań dla każdego poziomu
   * Wyświetlanie osiągniętych poziomów
   * Porównanie z poziomem wymaganym rozkazem

2. Automatyczne wypełnianie:
   * Możliwość automatycznego wypełnienia minimalnych wymagań dla wybranego poziomu

## 4. Implementacja

System został zaimplementowany w języku Python z wykorzystaniem następujących technologii:
* Streamlit - framework do tworzenia interfejsu użytkownika
* Pandas - obsługa danych tabelarycznych
* Folium - tworzenie interaktywnych map
* Streamlit-folium - integracja map z interfejsem

### 4.1 Struktura Plików:
* `app.py` - główny plik aplikacji
* `grupy_sgr.csv` - baza danych grup specjalistycznych
* `requirements.txt` - lista wymaganych bibliotek

### 4.2 Wymagania Systemowe:
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

## 5. Uwagi Końcowe

* System umożliwia dynamiczne sprawdzanie poziomu gotowości grup
* Wizualizacja zasięgu czasowego pomaga w planowaniu operacyjnym
* Interfejs jest intuicyjny i pozwala na szybkie wprowadzanie danych
* Automatyczne wypełnianie minimalnych wymagań usprawnia pracę
* System może być rozbudowywany o dodatkowe funkcjonalności
