import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Funkcja do wyświetlania zawartości pliku markdown
def load_markdown_file(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        return file.read()

def show_footer():
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: grey;'>
            <p>© 2024 Komenda Główna Państwowej Straży Pożarnej</p>
            <p>Biuro Informatyki i Łączności</p>
            <p>ul. Podchorążych 38, 00-463 Warszawa</p>
        </div>
        """, unsafe_allow_html=True)

def get_minimalne_wymagania(poziom):
    """Zwraca minimalne wymagania dla danego poziomu gotowości"""
    wymagania = {
        'A': {
            'liczba_ratownikow': 2,
            'liczba_mlodszych_nurkow': 2,
            'liczba_nurkow': 0,
            'liczba_nurkow_kierujacych': 0,
            'czy_sternik': True,
            'czy_strazak_logistyk': True,
            'liczba_slrr': 1,
            'liczba_lodzi': 1,
            'liczba_srchem': 0,
            'czy_wyposazenie_abc_chem': False,
            'czas_alarmowania': 0
        },
        'AB': {
            'liczba_ratownikow': 3,
            'liczba_mlodszych_nurkow': 2,
            'liczba_nurkow': 0,
            'liczba_nurkow_kierujacych': 1,
            'czy_sternik': True,
            'czy_strazak_logistyk': True,
            'liczba_slrr': 1,
            'liczba_lodzi': 1,
            'liczba_srchem': 0,
            'czy_wyposazenie_abc_chem': False,
            'czas_alarmowania': 0
        },
        'ABC': {
            'liczba_ratownikow': 5,
            'liczba_mlodszych_nurkow': 2,
            'liczba_nurkow': 2,
            'liczba_nurkow_kierujacych': 1,
            'czy_sternik': True,
            'czy_strazak_logistyk': True,
            'liczba_slrr': 2,
            'liczba_lodzi': 2,
            'liczba_srchem': 0,
            'czy_wyposazenie_abc_chem': False,
            'czas_alarmowania': 60
        },
        'ABCchem': {
            'liczba_ratownikow': 5,
            'liczba_mlodszych_nurkow': 2,
            'liczba_nurkow': 2,
            'liczba_nurkow_kierujacych': 1,
            'czy_sternik': True,
            'czy_strazak_logistyk': True,
            'liczba_slrr': 2,
            'liczba_lodzi': 2,
            'liczba_srchem': 1,
            'czy_wyposazenie_abc_chem': True,
            'czas_alarmowania': 60
        }
    }
    return wymagania.get(poziom, {})

def sprawdz_poziom_A(liczba_ratownikow, liczba_mlodszych_nurkow, czy_sternik, czy_strazak_logistyk,
                    liczba_slrr, liczba_lodzi):
    if (liczba_ratownikow >= 2 and 
        liczba_mlodszych_nurkow >= 2 and 
        czy_sternik and 
        czy_strazak_logistyk and
        liczba_slrr >= 1 and
        liczba_lodzi >= 1):
        return True
    return False

def sprawdz_poziom_AB(liczba_ratownikow, liczba_mlodszych_nurkow, liczba_nurkow_kierujacych, 
                      czy_sternik, czy_strazak_logistyk, liczba_slrr, liczba_lodzi):
    if (liczba_ratownikow >= 3 and 
        liczba_mlodszych_nurkow >= 2 and
        liczba_nurkow_kierujacych >= 1 and
        czy_sternik and 
        czy_strazak_logistyk and
        liczba_slrr >= 1 and
        liczba_lodzi >= 1):
        return True
    return False

def sprawdz_poziom_ABC(liczba_ratownikow, liczba_mlodszych_nurkow, liczba_nurkow, 
                       liczba_nurkow_kierujacych, czy_sternik, czy_strazak_logistyk, 
                       czas_alarmowania, liczba_slrr, liczba_lodzi):
    if (liczba_ratownikow >= 5 and 
        liczba_mlodszych_nurkow >= 2 and
        liczba_nurkow >= 2 and
        liczba_nurkow_kierujacych >= 1 and
        czy_sternik and 
        czy_strazak_logistyk and
        czas_alarmowania <= 60 and
        liczba_slrr >= 2 and
        liczba_lodzi >= 2):
        return True
    return False

def sprawdz_poziom_ABCchem(liczba_ratownikow, liczba_mlodszych_nurkow, liczba_nurkow, 
                          liczba_nurkow_kierujacych, czy_sternik, czy_strazak_logistyk,
                          czas_alarmowania, czy_wyposazenie_abc_chem, liczba_slrr, 
                          liczba_lodzi, liczba_srchem):
    if (sprawdz_poziom_ABC(liczba_ratownikow, liczba_mlodszych_nurkow, liczba_nurkow,
                          liczba_nurkow_kierujacych, czy_sternik, czy_strazak_logistyk,
                          czas_alarmowania, liczba_slrr, liczba_lodzi) and 
        czy_wyposazenie_abc_chem and
        liczba_srchem >= 1):
        return True
    return False

def create_time_radius_map(lat, lon, nazwa_grupy):
    """Tworzy mapę z okręgami reprezentującymi zasięg czasowy"""
    # Średnia prędkość wozu strażackiego (km/h)
    avg_speed = 60
    
    # Czasy w minutach i ich kolory
    times = [5, 10, 15, 25, 60]
    colors = ['#ff0000', '#ff6600', '#ffa500', '#ffcc00', '#ffff00']
    
    # Tworzenie mapy
    m = folium.Map(location=[lat, lon], zoom_start=10)
    
    # Dodanie znacznika lokalizacji jednostki
    folium.Marker(
        [lat, lon],
        popup=nazwa_grupy,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Dodanie okręgów dla każdego czasu
    for time, color in zip(times, colors):
        # Obliczenie promienia w kilometrach (czas w h * prędkość w km/h)
        radius = (time / 60) * avg_speed * 1000  # konwersja na metry
        
        folium.Circle(
            radius=radius,
            location=[lat, lon],
            popup=f'Zasięg {time} min',
            color=color,
            fill=True,
            opacity=0.4,
            fill_opacity=0.2
        ).add_to(m)
    
    return m

def pokaz_tabele_wymagan():
    # Tworzenie danych dla tabeli
    data = {
        'Poziom': ['A', 'AB', 'ABC', 'ABCchem'],
        'Min. liczba ratowników': [2, 3, 5, 5],
        'Min. liczba młodszych nurków': [2, 2, 2, 2],
        'Min. liczba nurków': [0, 0, 2, 2],
        'Min. liczba nurków kierujących': [0, 1, 1, 1],
        'Sternik': ['Wymagany', 'Wymagany', 'Wymagany', 'Wymagany'],
        'Strażak logistyk': ['Wymagany', 'Wymagany', 'Wymagany', 'Wymagany'],
        'Min. liczba SLRR/SLRW': [1, 1, 2, 2],
        'Min. liczba łodzi': [1, 1, 2, 2],
        'Min. liczba SRChem': [0, 0, 0, 1],
        'Czas alarmowania': ['Niezwłoczny', 'Niezwłoczny', '60 min', '60 min'],
        'Wyposażenie ABC-chem': ['Nie', 'Nie', 'Nie', 'Tak']
    }
    
    df = pd.DataFrame(data)
    
    # Stylizacja tabeli
    st.markdown("### Minimalne wymagania dla poszczególnych poziomów gotowości")
    st.dataframe(
        df.style.set_properties(**{
            'background-color': 'lightgrey',
            'color': 'black',
            'border-color': 'white'
        })
    )

def main():
    st.sidebar.title("Menu Główne")
    menu_option = st.sidebar.radio("Wybierz sekcję:", 
                                 ["Monitoring SGRW-N", 
                                  "Algorytmika SGRW-N",
                                  "Autorzy"])
    
    if menu_option == "Monitoring SGRW-N":
        st.title("System Określania Poziomu Gotowości SGRW-N")
        
        # Inicjalizacja wartości w sesji
        if 'liczba_ratownikow' not in st.session_state:
            st.session_state.liczba_ratownikow = 0
        if 'liczba_mlodszych_nurkow' not in st.session_state:
            st.session_state.liczba_mlodszych_nurkow = 0
        if 'liczba_nurkow' not in st.session_state:
            st.session_state.liczba_nurkow = 0
        if 'liczba_nurkow_kierujacych' not in st.session_state:
            st.session_state.liczba_nurkow_kierujacych = 0
        if 'czy_sternik' not in st.session_state:
            st.session_state.czy_sternik = False
        if 'czy_strazak_logistyk' not in st.session_state:
            st.session_state.czy_strazak_logistyk = False
        if 'czy_wyposazenie_abc_chem' not in st.session_state:
            st.session_state.czy_wyposazenie_abc_chem = False
        if 'czas_alarmowania' not in st.session_state:
            st.session_state.czas_alarmowania = 0
        if 'liczba_slrr' not in st.session_state:
            st.session_state.liczba_slrr = 0
        if 'liczba_lodzi' not in st.session_state:
            st.session_state.liczba_lodzi = 0
        if 'liczba_srchem' not in st.session_state:
            st.session_state.liczba_srchem = 0
        if 'nazwa_sgr' not in st.session_state:
            st.session_state.nazwa_sgr = ""
        if 'nr_id' not in st.session_state:
            st.session_state.nr_id = ""
        
        # Wczytanie danych z pliku CSV
        df_grupy = pd.read_csv('grupy_sgr.csv')
        
        # Utworzenie słownika KW -> KP/KM
        kw_kp_dict = {}
        for _, row in df_grupy.iterrows():
            if row['kw'] not in kw_kp_dict:
                kw_kp_dict[row['kw']] = []
            if row['kp_km'] not in kw_kp_dict[row['kw']]:
                kw_kp_dict[row['kw']].append(row['kp_km'])

        # Wybór KW i KP/KM
        st.header("Wybór jednostki:")
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_kw = st.selectbox("Wybierz Komendę Wojewódzką:", 
                                     options=[''] + list(kw_kp_dict.keys()))
        
        with col2:
            selected_kp_km = st.selectbox("Wybierz Komendę Miejską/Powiatową:", 
                                        options=[''] + (kw_kp_dict[selected_kw] if selected_kw else []))
        
        # Utworzenie listy dostępnych nazw grup dla wybranego KW i KM/KP
        available_groups = []
        if selected_kw and selected_kp_km:
            available_groups = df_grupy[
                (df_grupy['kw'] == selected_kw) & 
                (df_grupy['kp_km'] == selected_kp_km)
            ]['nazwa_SGR'].tolist()
        
        with col3:
            selected_nazwa = st.selectbox("Wybierz nazwę grupy:", 
                                        options=[''] + available_groups)

        # Wyświetlenie informacji o grupie i ustawienie minimalnych wymagań
        if selected_kw and selected_kp_km and selected_nazwa:
            grupa = df_grupy[
                (df_grupy['kw'] == selected_kw) & 
                (df_grupy['kp_km'] == selected_kp_km) & 
                (df_grupy['nazwa_SGR'] == selected_nazwa)
            ]
            if not grupa.empty:
                st.markdown("### Informacje o grupie:")
                
                # Wyświetlenie numeru ID i poziomu gotowości
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("Numer identyfikacyjny grupy:", 
                                value=str(grupa.iloc[0]['nr_id']), 
                                disabled=True)
                    st.session_state.nr_id = str(grupa.iloc[0]['nr_id'])
                
                with col2:
                    st.text_input("Poziom gotowości wskazany rozkazem:", 
                                 value=grupa.iloc[0]['gotowosc_rozkaz'], 
                                 disabled=True)
                
                # Wyświetlenie mapy z zasięgami czasowymi
                st.markdown("### Mapa zasięgu czasowego")
                st.markdown("Okręgi pokazują szacunkowy zasięg dojazdu dla wozu strażackiego:")
                st.markdown("- Czerwony: 5 minut")
                st.markdown("- Pomarańczowy: 10 minut")
                st.markdown("- Żółto-pomarańczowy: 15 minut")
                st.markdown("- Żółto-pomarańczowy jasny: 25 minut")
                st.markdown("- Żółty: 60 minut")
                
                # Utworzenie i wyświetlenie mapy
                mapa = create_time_radius_map(
                    grupa.iloc[0]['lat'],
                    grupa.iloc[0]['long'],
                    grupa.iloc[0]['nazwa_SGR']
                )
                folium_static(mapa)
                
                # Pobranie minimalnych wymagań dla poziomu
                min_wymagania = get_minimalne_wymagania(grupa.iloc[0]['gotowosc_rozkaz'])
                if min_wymagania and st.button("Uzupełnij minimalne wymagania"):
                    for key, value in min_wymagania.items():
                        setattr(st.session_state, key, value)
        
        st.header("Wprowadź dane:")
        
        # Dane podstawowe
        col1, col2, col3 = st.columns(3)
        with col1:
            liczba_ratownikow = st.number_input("Liczba ratowników", 
                                              min_value=0, 
                                              value=st.session_state.liczba_ratownikow)
            liczba_mlodszych_nurkow = st.number_input("Liczba młodszych nurków", 
                                                    min_value=0, 
                                                    value=st.session_state.liczba_mlodszych_nurkow)
            liczba_nurkow = st.number_input("Liczba nurków", 
                                          min_value=0, 
                                          value=st.session_state.liczba_nurkow)
            liczba_nurkow_kierujacych = st.number_input("Liczba nurków kierujących", 
                                                        min_value=0, 
                                                        value=st.session_state.liczba_nurkow_kierujacych)
        
        with col2:
            czy_sternik = st.checkbox("Czy jest dostępny sternik?", 
                                    value=st.session_state.czy_sternik)
            czy_strazak_logistyk = st.checkbox("Czy jest dostępny strażak logistyk?", 
                                             value=st.session_state.czy_strazak_logistyk)
            czy_wyposazenie_abc_chem = st.checkbox("Czy jest dostępne wyposażenie ABC-chem?", 
                                                 value=st.session_state.czy_wyposazenie_abc_chem)
            czas_alarmowania = st.number_input("Czas alarmowania (minuty)", 
                                             min_value=0, 
                                             value=st.session_state.czas_alarmowania)

        with col3:
            liczba_slrr = st.number_input("Liczba pojazdów SLRR/SLRW", 
                                        min_value=0, 
                                        value=st.session_state.liczba_slrr)
            liczba_lodzi = st.number_input("Liczba łodzi", 
                                         min_value=0, 
                                         value=st.session_state.liczba_lodzi)
            liczba_srchem = st.number_input("Liczba pojazdów SRChem", 
                                          min_value=0, 
                                          value=st.session_state.liczba_srchem)

        # Aktualizacja wartości w sesji
        st.session_state.liczba_ratownikow = liczba_ratownikow
        st.session_state.liczba_mlodszych_nurkow = liczba_mlodszych_nurkow
        st.session_state.liczba_nurkow = liczba_nurkow
        st.session_state.liczba_nurkow_kierujacych = liczba_nurkow_kierujacych
        st.session_state.czy_sternik = czy_sternik
        st.session_state.czy_strazak_logistyk = czy_strazak_logistyk
        st.session_state.czy_wyposazenie_abc_chem = czy_wyposazenie_abc_chem
        st.session_state.czas_alarmowania = czas_alarmowania
        st.session_state.liczba_slrr = liczba_slrr
        st.session_state.liczba_lodzi = liczba_lodzi
        st.session_state.liczba_srchem = liczba_srchem

        if st.button("Sprawdź poziom gotowości"):
            poziomy = []
            
            # Sprawdzanie kolejnych poziomów
            if sprawdz_poziom_A(liczba_ratownikow, liczba_mlodszych_nurkow, 
                               czy_sternik, czy_strazak_logistyk, liczba_slrr, liczba_lodzi):
                poziomy.append("A")
                
            if sprawdz_poziom_AB(liczba_ratownikow, liczba_mlodszych_nurkow,
                                liczba_nurkow_kierujacych, czy_sternik, czy_strazak_logistyk,
                                liczba_slrr, liczba_lodzi):
                poziomy.append("AB")
                
            if sprawdz_poziom_ABC(liczba_ratownikow, liczba_mlodszych_nurkow, liczba_nurkow,
                                 liczba_nurkow_kierujacych, czy_sternik, czy_strazak_logistyk,
                                 czas_alarmowania, liczba_slrr, liczba_lodzi):
                poziomy.append("ABC")
                
            if sprawdz_poziom_ABCchem(liczba_ratownikow, liczba_mlodszych_nurkow, liczba_nurkow,
                                     liczba_nurkow_kierujacych, czy_sternik, czy_strazak_logistyk,
                                     czas_alarmowania, czy_wyposazenie_abc_chem, liczba_slrr,
                                     liczba_lodzi, liczba_srchem):
                poziomy.append("ABCchem")

            if poziomy:
                st.success(f"Grupa spełnia wymagania dla poziomów: {', '.join(poziomy)}")
                st.info(f"Najwyższy osiągnięty poziom gotowości: {poziomy[-1]}")
                
                # Porównanie z gotowością wg rozkazu
                if selected_kw and selected_kp_km:
                    grupa = df_grupy[(df_grupy['kw'] == selected_kw) & (df_grupy['kp_km'] == selected_kp_km)]
                    if not grupa.empty:
                        gotowosc_rozkaz = grupa.iloc[0]['gotowosc_rozkaz']
                        if poziomy[-1] == gotowosc_rozkaz:
                            st.success("✅ Grupa utrzymuje poziom gotowości zgodny z rozkazem")
                        elif poziomy[-1] > gotowosc_rozkaz:
                            st.success("✅ Grupa przekracza wymagany poziom gotowości")
                        else:
                            st.warning("⚠️ Grupa nie osiąga wymaganego poziomu gotowości")
            else:
                st.error("Grupa nie spełnia wymagań żadnego poziomu gotowości")
        
        # Wyświetlenie tabeli z wymaganiami
        st.markdown("---")
        pokaz_tabele_wymagan()
    
    elif menu_option == "Algorytmika SGRW-N":
        st.title("Algorytmika SGRW-N")
        algorytmika_content = load_markdown_file('algorytmika.md')
        st.markdown(algorytmika_content)
        
    else:  # Autorzy
        st.title("Autorzy Systemu")
        autorzy_content = load_markdown_file('autorzy.md')
        st.markdown(autorzy_content)
    
    # Wyświetlenie stopki
    show_footer()

if __name__ == "__main__":
    # Konfiguracja strony
    st.set_page_config(
        page_title="System Monitorowania SGRW-N",
        page_icon="🚒",
        layout="wide"
    )
    main() 