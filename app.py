import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def show_footer():
    st.markdown("""
        <div class="footer">
            <p>© 2024 Komenda Główna Państwowej Straży Pożarnej</p>
            <p>Biuro Informatyki i Łączności</p>
            <p>ul. Podchorążych 38, 00-463 Warszawa</p>
        </div>
    """, unsafe_allow_html=True)

def load_markdown_file(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        return file.read()

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

def get_minimalne_wymagania_sgrw(poziom):
    """Zwraca minimalne wymagania dla danego poziomu gotowości SGRW"""
    wymagania = {
        'A': {
            'liczba_ratownikow': 18,
            'liczba_ratownikow_wysokosciowych': 3,
            'liczba_ratownikow_wysokosciowych_dowodcow': 1,
            'czy_wyposazenie_standardowe': True,
            'czas_alarmowania': 0
        },
        'B': {
            'liczba_ratownikow': 30,
            'liczba_ratownikow_wysokosciowych': 5,
            'liczba_ratownikow_wysokosciowych_dowodcow': 1,
            'czy_wyposazenie_standardowe': True,
            'czas_alarmowania': 0
        },
        'AS': {
            'liczba_ratownikow': 12,
            'liczba_ratownikow_smiglowcowych': 3,
            'liczba_ratownikow_smiglowcowych_operatorow': 1,
            'czy_wyposazenie_standardowe': True,
            'czas_alarmowania': 0
        },
        'BS': {
            'liczba_ratownikow': 12,
            'liczba_ratownikow_smiglowcowych': 5,
            'liczba_ratownikow_smiglowcowych_operatorow': 1,
            'czy_wyposazenie_standardowe': True,
            'czas_alarmowania': 0
        }
    }
    return wymagania.get(poziom, {})

def sprawdz_poziom_sgrw_A(liczba_ratownikow, liczba_ratownikow_wysokosciowych, 
                         liczba_ratownikow_wysokosciowych_dowodcow, czy_wyposazenie_standardowe):
    if (liczba_ratownikow >= 18 and 
        liczba_ratownikow_wysokosciowych >= 3 and
        liczba_ratownikow_wysokosciowych_dowodcow >= 1 and
        czy_wyposazenie_standardowe):
        return True
    return False

def sprawdz_poziom_sgrw_B(liczba_ratownikow, liczba_ratownikow_wysokosciowych,
                         liczba_ratownikow_wysokosciowych_dowodcow, czy_wyposazenie_standardowe):
    if (liczba_ratownikow >= 30 and 
        liczba_ratownikow_wysokosciowych >= 5 and
        liczba_ratownikow_wysokosciowych_dowodcow >= 1 and
        czy_wyposazenie_standardowe):
        return True
    return False

def sprawdz_poziom_sgrw_AS(liczba_ratownikow, liczba_ratownikow_smiglowcowych,
                          liczba_ratownikow_smiglowcowych_operatorow, czy_wyposazenie_standardowe):
    if (liczba_ratownikow >= 12 and 
        liczba_ratownikow_smiglowcowych >= 3 and
        liczba_ratownikow_smiglowcowych_operatorow >= 1 and
        czy_wyposazenie_standardowe):
        return True
    return False

def sprawdz_poziom_sgrw_BS(liczba_ratownikow, liczba_ratownikow_smiglowcowych,
                          liczba_ratownikow_smiglowcowych_operatorow, czy_wyposazenie_standardowe):
    if (liczba_ratownikow >= 12 and 
        liczba_ratownikow_smiglowcowych >= 5 and
        liczba_ratownikow_smiglowcowych_operatorow >= 1 and
        czy_wyposazenie_standardowe):
        return True
    return False

def pokaz_tabele_wymagan_sgrw():
    # Tworzenie danych dla tabeli
    data = {
        'Poziom': ['A', 'B', 'AS', 'BS'],
        'Min. liczba ratowników': [18, 30, 12, 12],
        'Min. liczba ratowników wysokościowych': [3, 5, '-', '-'],
        'Min. liczba ratowników wysokościowych dowódców': [1, 1, '-', '-'],
        'Min. liczba ratowników śmigłowcowych': ['-', '-', 3, 5],
        'Min. liczba ratowników śmigłowcowych operatorów': ['-', '-', 1, 1],
        'Wyposażenie standardowe': ['Wymagane', 'Wymagane', 'Wymagane', 'Wymagane'],
        'Czas alarmowania': ['Niezwłoczny', 'Niezwłoczny', 'Niezwłoczny', 'Niezwłoczny']
    }
    
    df = pd.DataFrame(data)
    
    st.markdown("### Minimalne wymagania dla poszczególnych poziomów gotowości SGRW")
    st.dataframe(
        df.style.set_properties(**{
            'background-color': 'lightgrey',
            'color': 'black',
            'border-color': 'white'
        })
    )

def main():
    # Wczytanie stylów CSS
    load_css()
    
    # Logo i menu w pasku bocznym
    st.sidebar.markdown("""
        <div class="sidebar-logo" style="background: transparent;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b4/Logo-psp-nowe-wrzesien-2017.svg" 
                 width="60" 
                 style="background: transparent; mix-blend-mode: multiply;">
            <h4 style='margin-top:1rem;'>System Monitorowania<br>SGRW-N</h4>
        </div>
    """, unsafe_allow_html=True)

    menu_option = st.sidebar.radio("", 
                                 ["Monitoring SGRW-N",
                                  "Monitoring SGRW", 
                                  "Algorytm SGRW-N",
                                  "Algorytm SGRW",
                                  "Autorzy"])
    
    # Link do GitHub
    st.sidebar.markdown("""
        <div style='text-align: center; margin-top: 2rem;'>
            <a href='https://github.com/KGPSP/Monitoring-SGR' target='_blank' 
               style='text-decoration: none; color: #666;'>
                <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' 
                     width='30px' style='margin-bottom: 0.5rem;'>
                <br>
                Kod źródłowy na GitHub
            </a>
        </div>
    """, unsafe_allow_html=True)

    if menu_option == "Monitoring SGRW-N":
        st.markdown('<h1>System Określania Poziomu Gotowości SGRW-N</h1>', unsafe_allow_html=True)
        
        # Dodanie opisu systemu
        st.markdown("""
            <div class="system-description">
                <p>System służy do monitorowania i określania poziomu gotowości operacyjnej Specjalistycznych Grup Ratownictwa Wodno-Nurkowego (SGRW-N).
                Umożliwia weryfikację spełnienia wymagań dla poszczególnych poziomów gotowości (A, AB, ABC, ABCchem) poprzez analizę:</p>
                <ul>
                    <li>Stanu osobowego (ratownicy, nurkowie)</li>
                    <li>Dostępnego sprzętu (pojazdy, łodzie)</li>
                    <li>Czasu alarmowania</li>
                    <li>Dodatkowych wymagań specjalistycznych</li>
                </ul>
                <p>Program automatycznie określa aktualny poziom gotowości grupy na podstawie wprowadzonych danych
                i porównuje go z poziomem wymaganym zgodnie z rozkazem.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Inicjalizacja sesji (bez zmian)
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

        # Sekcja wyboru jednostki
        with st.container():
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-header">Wybór jednostki</h2>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_kw = st.selectbox("Komenda Wojewódzka:", 
                                         options=[''] + list(kw_kp_dict.keys()))
            with col2:
                selected_kp_km = st.selectbox("Komenda Miejska/Powiatowa:", 
                                            options=[''] + (kw_kp_dict[selected_kw] if selected_kw else []))
            
            # Utworzenie listy dostępnych nazw grup dla wybranego KW i KM/KP
            available_groups = []
            if selected_kw and selected_kp_km:
                available_groups = df_grupy[
                    (df_grupy['kw'] == selected_kw) & 
                    (df_grupy['kp_km'] == selected_kp_km)
                ]['nazwa_SGR'].tolist()
            
            with col3:
                selected_nazwa = st.selectbox("Nazwa grupy:", 
                                            options=[''] + available_groups)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Sekcja informacji o grupie
        if selected_kw and selected_kp_km and selected_nazwa:
            grupa = df_grupy[
                (df_grupy['kw'] == selected_kw) & 
                (df_grupy['kp_km'] == selected_kp_km) & 
                (df_grupy['nazwa_SGR'] == selected_nazwa)
            ]
            if not grupa.empty:
                st.markdown('<div class="section">', unsafe_allow_html=True)
                st.markdown('<h2 class="section-header">Informacje o grupie</h2>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="form-field">', unsafe_allow_html=True)
                    st.text_input("Numer identyfikacyjny:", 
                                value=str(grupa.iloc[0]['nr_id']), 
                                disabled=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="form-field">', unsafe_allow_html=True)
                    st.text_input("Poziom gotowości:", 
                                 value=grupa.iloc[0]['gotowosc_rozkaz'], 
                                 disabled=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Mapa
                st.markdown('<h3>Mapa zasięgu czasowego</h3>', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                with col1:
                    mapa = create_time_radius_map(
                        grupa.iloc[0]['lat'],
                        grupa.iloc[0]['long'],
                        grupa.iloc[0]['nazwa_SGR']
                    )
                    folium_static(mapa)
                
                with col2:
                    st.markdown("""
                        <div class="map-legend">
                            <h4>Legenda</h4>
                            <p>🔴 5 minut</p>
                            <p>🟠 10 minut</p>
                            <p>🟡 15 minut</p>
                            <p>🟨 25 minut</p>
                            <p>💛 60 minut</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Sekcja wprowadzania danych
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Wprowadź dane</h2>', unsafe_allow_html=True)
        
        # Pobranie minimalnych wymagań dla wybranej grupy
        min_wymagania = None
        if selected_kw and selected_kp_km and selected_nazwa:
            grupa = df_grupy[
                (df_grupy['kw'] == selected_kw) & 
                (df_grupy['kp_km'] == selected_kp_km) & 
                (df_grupy['nazwa_SGR'] == selected_nazwa)
            ]
            if not grupa.empty:
                min_wymagania = get_minimalne_wymagania(grupa.iloc[0]['gotowosc_rozkaz'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<h3>Stan osobowy</h3>', unsafe_allow_html=True)
            st.markdown('<div class="form-field">', unsafe_allow_html=True)
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
            czy_sternik = st.checkbox("Czy jest dostępny sternik?", 
                                    value=st.session_state.czy_sternik)
            czy_strazak_logistyk = st.checkbox("Czy jest dostępny strażak logistyk?", 
                                             value=st.session_state.czy_strazak_logistyk)
            czy_wyposazenie_abc_chem = st.checkbox("Czy jest dostępne wyposażenie ABC-chem?", 
                                                 value=st.session_state.czy_wyposazenie_abc_chem)
            czas_alarmowania = st.number_input("Czas alarmowania (minuty)", 
                                             min_value=0, 
                                             value=st.session_state.czas_alarmowania)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            liczba_slrr = st.number_input("Liczba pojazdów SLRR/SLRW", 
                                        min_value=0, 
                                        value=st.session_state.liczba_slrr)
            liczba_lodzi = st.number_input("Liczba łodzi", 
                                         min_value=0, 
                                         value=st.session_state.liczba_lodzi)
            liczba_srchem = st.number_input("Liczba pojazdów SRChem", 
                                          min_value=0, 
                                          value=st.session_state.liczba_srchem)
        
        # Przyciski akcji
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sprawdź poziom gotowości", key='check_button'):
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
        
        with col2:
            if min_wymagania and st.button("Uzupełnij minimalne wymagania", key='fill_button'):
                for key, value in min_wymagania.items():
                    setattr(st.session_state, key, value)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabela wymagań
        st.markdown('<div class="section">', unsafe_allow_html=True)
        pokaz_tabele_wymagan()
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif menu_option == "Monitoring SGRW":
        st.markdown('<h1>System Określania Poziomu Gotowości SGRW</h1>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="system-description">
                <p>System służy do monitorowania i określania poziomu gotowości operacyjnej Specjalistycznych Grup Ratownictwa Wysokościowego (SGRW).
                Umożliwia weryfikację spełnienia wymagań dla poszczególnych poziomów gotowości (A, B, AS, BS) poprzez analizę:</p>
                <ul>
                    <li>Stanu osobowego (ratownicy, ratownicy wysokościowi, ratownicy śmigłowcowi)</li>
                    <li>Kwalifikacji personelu (dowódcy, operatorzy)</li>
                    <li>Dostępnego wyposażenia standardowego</li>
                    <li>Czasu alarmowania</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        # Inicjalizacja zmiennych sesji dla SGRW
        if 'sgrw_liczba_ratownikow' not in st.session_state:
            st.session_state.sgrw_liczba_ratownikow = 0
        if 'sgrw_liczba_ratownikow_wysokosciowych' not in st.session_state:
            st.session_state.sgrw_liczba_ratownikow_wysokosciowych = 0
        if 'sgrw_liczba_ratownikow_wysokosciowych_dowodcow' not in st.session_state:
            st.session_state.sgrw_liczba_ratownikow_wysokosciowych_dowodcow = 0
        if 'sgrw_liczba_ratownikow_smiglowcowych' not in st.session_state:
            st.session_state.sgrw_liczba_ratownikow_smiglowcowych = 0
        if 'sgrw_liczba_ratownikow_smiglowcowych_operatorow' not in st.session_state:
            st.session_state.sgrw_liczba_ratownikow_smiglowcowych_operatorow = 0
        if 'sgrw_czy_wyposazenie_standardowe' not in st.session_state:
            st.session_state.sgrw_czy_wyposazenie_standardowe = False

        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">Wprowadź dane SGRW</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3>Stan osobowy podstawowy</h3>', unsafe_allow_html=True)
            liczba_ratownikow = st.number_input("Liczba ratowników", 
                                              min_value=0, 
                                              value=st.session_state.sgrw_liczba_ratownikow,
                                              key='sgrw_ratownicy')
            liczba_ratownikow_wysokosciowych = st.number_input("Liczba ratowników wysokościowych", 
                                                             min_value=0, 
                                                             value=st.session_state.sgrw_liczba_ratownikow_wysokosciowych,
                                                             key='sgrw_wysokosciowi')
            liczba_ratownikow_wysokosciowych_dowodcow = st.number_input("Liczba ratowników wysokościowych dowódców", 
                                                                       min_value=0, 
                                                                       value=st.session_state.sgrw_liczba_ratownikow_wysokosciowych_dowodcow,
                                                                       key='sgrw_wysokosciowi_dowodcy')

        with col2:
            st.markdown('<h3>Stan osobowy śmigłowcowy</h3>', unsafe_allow_html=True)
            liczba_ratownikow_smiglowcowych = st.number_input("Liczba ratowników śmigłowcowych", 
                                                            min_value=0, 
                                                            value=st.session_state.sgrw_liczba_ratownikow_smiglowcowych,
                                                            key='sgrw_smiglowcowi')
            liczba_ratownikow_smiglowcowych_operatorow = st.number_input("Liczba ratowników śmigłowcowych operatorów", 
                                                                        min_value=0, 
                                                                        value=st.session_state.sgrw_liczba_ratownikow_smiglowcowych_operatorow,
                                                                        key='sgrw_smiglowcowi_operatorzy')
            czy_wyposazenie_standardowe = st.checkbox("Czy jest dostępne wyposażenie standardowe?", 
                                                    value=st.session_state.sgrw_czy_wyposazenie_standardowe,
                                                    key='sgrw_wyposazenie')

        if st.button("Sprawdź poziom gotowości SGRW", key='check_button_sgrw'):
            poziomy = []
            
            # Sprawdzanie kolejnych poziomów
            if sprawdz_poziom_sgrw_A(liczba_ratownikow, liczba_ratownikow_wysokosciowych,
                                   liczba_ratownikow_wysokosciowych_dowodcow, czy_wyposazenie_standardowe):
                poziomy.append("A")
                
            if sprawdz_poziom_sgrw_B(liczba_ratownikow, liczba_ratownikow_wysokosciowych,
                                   liczba_ratownikow_wysokosciowych_dowodcow, czy_wyposazenie_standardowe):
                poziomy.append("B")
                
            if sprawdz_poziom_sgrw_AS(liczba_ratownikow, liczba_ratownikow_smiglowcowych,
                                    liczba_ratownikow_smiglowcowych_operatorow, czy_wyposazenie_standardowe):
                poziomy.append("AS")
                
            if sprawdz_poziom_sgrw_BS(liczba_ratownikow, liczba_ratownikow_smiglowcowych,
                                    liczba_ratownikow_smiglowcowych_operatorow, czy_wyposazenie_standardowe):
                poziomy.append("BS")

            if poziomy:
                st.success(f"Grupa spełnia wymagania dla poziomów: {', '.join(poziomy)}")
                st.info(f"Najwyższy osiągnięty poziom gotowości: {poziomy[-1]}")
            else:
                st.error("Grupa nie spełnia wymagań żadnego poziomu gotowości")

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabela wymagań
        st.markdown('<div class="section">', unsafe_allow_html=True)
        pokaz_tabele_wymagan_sgrw()
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif menu_option == "Algorytm SGRW":
        st.markdown('<h1>Algorytm SGRW</h1>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        sgrw_content = load_markdown_file('sgrwys.md')
        st.markdown(sgrw_content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif menu_option == "Algorytm SGRW-N":
        st.markdown('<h1>Algorytm SGRW-N</h1>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        algorytmika_content = load_markdown_file('algorytmika.md')
        st.markdown(algorytmika_content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # Autorzy
        st.markdown('<h1>Autorzy Systemu</h1>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        autorzy_content = load_markdown_file('autorzy.md')
        st.markdown(autorzy_content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    show_footer()

if __name__ == "__main__":
    st.set_page_config(
        page_title="System Monitorowania SGRW-N",
        page_icon="🚒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main() 