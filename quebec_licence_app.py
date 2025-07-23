import streamlit as st
import random

def soundex_standard(name):
    """
    Soundex standard comme sur searchforancestors.com
    """
    name = name.upper()
    soundex_mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2',
        'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }

    first_letter = name[0]
    encoded = []

    previous_digit = ''
    for char in name[1:]:
        digit = soundex_mapping.get(char, '')
        if digit and digit != previous_digit:
            encoded.append(digit)
            previous_digit = digit
        elif digit == '':
            previous_digit = ''  # reset on vowels

    soundex_code = first_letter + ''.join(encoded)
    return (soundex_code + '000')[:4]

def quebec_drivers_licence(name, first_name, year, month, day, sex='M'):
    # Utilise Soundex identique à searchforancestors
    code_nom = soundex_standard(name)

    # Ajout d'un chiffre fixe à la fin pour compléter le bloc de nom
    fixed_digit = '4'
    code_nom = code_nom + fixed_digit

    yy = str(year)[-2:]
    mm = int(month)
    if sex.upper() == 'F':
        mm += 50
    mm = f"{mm:02d}"
    dd = f"{int(day):02d}"

    return f"{code_nom}-{yy}{mm}{dd}"

# STREAMLIT
st.set_page_config(page_title="License generator", page_icon="🚙", layout="centered")
st.title("SAAQlick Pas du tout!")
st.markdown("Trouve ton permis en 30 secondes")

with st.form("licence_form"):
    last_name = st.text_input("Nom de famille")
    first_name = st.text_input("Prénom")

    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("Année de naissance", min_value=1900, max_value=2100)
    with col2:
        month = st.selectbox("Mois", list(range(1, 13)))
    with col3:
        day = st.number_input("Jour", min_value=1, max_value=31)

    sex = st.radio("Sexe", ['M', 'F'], horizontal=True)
    submit = st.form_submit_button("🔐 Générer le permis")

    if submit:
        if not last_name or not first_name:
            st.warning("Entrer le prénom et nom.")
        else:
            base_code = quebec_drivers_licence(last_name, first_name, year, month, day, sex)
            final = f"{random.randint(0, 99):02d}"
            full = f"{base_code}-{final}"
            st.success(f"✅ Numéro de permis : **{full}**")
            st.caption("⚠️ les 2 derniers peut ne pas etre exacte")