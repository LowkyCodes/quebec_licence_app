import streamlit as st
import random

# SAAQ
def saaq_soundex(last_name, first_name):

    mapping = {
        'A': '', 'E': '', 'I': '', 'O': '', 'U': '', 'H': '', 'W': '', 'Y': '',
        'B': '1', 'P': '1', 'F': '1', 'V': '1',
        'C': '2', 'S': '2', 'K': '2', 'G': '2', 'J': '2', 'Q': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }

    name = last_name.upper()
    first_letter = name[0]
    encoded = []

    for char in name[1:]:
        if char in mapping:
            code = mapping[char]
            if code != '' and (not encoded or code != encoded[-1]):
                encoded.append(code)

    code = first_letter + ''.join(encoded)
    code = (code + '000')[:4]

    # Adjust the 4th character using the first name initial (approximation)
    prenom_initial = first_name[0].upper()
    lettre_map = {
        'A': '1', 'B': '1', 'C': '1',
        'D': '2', 'E': '2', 'F': '2',
        'G': '3', 'H': '3', 'I': '3',
        'J': '4', 'K': '4', 'L': '4',
        'M': '5', 'N': '5', 'O': '5',
        'P': '6', 'Q': '6', 'R': '6',
        'S': '7', 'T': '7', 'U': '7',
        'V': '8', 'W': '8', 'X': '8',
        'Y': '9', 'Z': '9'
    }

    last_digit = lettre_map.get(prenom_initial, '0')
    code = code[:3] + last_digit
    return code


def quebec_drivers_licence(last_name, first_name, year, month, day, sex='M'):
    soundex_code = saaq_soundex(last_name, first_name)
    yy = str(year)[-2:]
    mm = int(month)
    if sex.upper() == 'F':
        mm += 50
    mm = f"{mm:02d}"
    dd = f"{int(day):02d}"
    return f"{soundex_code}-{yy}{mm}{dd}"


# Streamlit App
st.set_page_config(page_title="License generator", page_icon="🚙🛣️", layout="centered")

st.title("🚗 GÉNÉRATEUR DE PERMIS DU QUÉBEC")
st.markdown("Tu as oublié ton numéro de permis ? Pas de souci, on va essayer de le deviner !")

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

            st.success(f"✅ Numéro de permis approximatif : **{licence_full}**")
            st.caption("⚠️ Ce code est une approximation basée sur les règles publiques connues. Le vrai algorithme utilisé par la SAAQ est confidentiel.")