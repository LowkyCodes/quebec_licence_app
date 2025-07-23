import streamlit as st
import random


def soundex(name):
    name = name.upper()
    soundex_mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
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

    soundex_code = first_letter + ''.join(encoded)
    return (soundex_code + '000')[:4]



def quebec_drivers_licence(last_name, first_name, year, month, day, sex='M'):
    soundex_code = soundex(last_name)
    yy = str(year)[-2:]
    mm = int(month)
    if sex.upper() == 'F':
        mm += 50
    mm = f"{mm:02d}"
    dd = f"{int(day):02d}"
    return f"{soundex_code}-{yy}{mm}{dd}"



st.set_page_config(page_title="License generator", page_icon="🚗", layout="centered")

st.title("🚗 QUEBEC LICENCE GENERATOR")
st.markdown("This tool will save you a bunch of time no cap")

with st.form("licence_form"):
    last_name = st.text_input("Nom de famille")
    first_name = st.text_input("Prénom")

    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("Année de naissance", min_value=1900, max_value=2100, step=1)
    with col2:
        month = st.selectbox("Mois", list(range(1, 13)))
    with col3:
        day = st.number_input("Jour", min_value=1, max_value=31, step=1)

    sex = st.radio("Sexe", ['M', 'F'], horizontal=True)

    generate = st.form_submit_button("🔐 Générer le permis")

    if generate:
        if not last_name or not first_name:
            st.warning("Veuillez entrer le prénom et le nom.")
        else:
            base_code = quebec_drivers_licence(last_name, first_name, year, month, day, sex)
            final_digits = f"{random.randint(0, 99):02d}"
            licence_full = f"{base_code}-{final_digits}"

            st.success(f"✅ Numéro de permis : **{licence_full}**")
            st.caption("⚠️ Note : les deux derniers chiffres ne sont pas valide mais le reste oui.")
