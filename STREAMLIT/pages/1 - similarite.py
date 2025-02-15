import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import ast
from bs4 import BeautifulSoup
import pickle
import requests
import re
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from rapidfuzz import fuzz
from rapidfuzz import process
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns

# BASE

df = pd.read_csv('BD/dataset_a_jour.csv')
df = df.drop_duplicates(subset='ID', keep = 'first')
df = df[(df['name'].isna() == False) | (df['name'] == 'Pas encore fait')]
df['name'] = df['name'].astype(str)
df['name'] = df['name'].apply(lambda x : x.split(',') if ',' in x else x)
df['Team & Contract'] = df['Team & Contract'].apply(lambda x : int(x) if x != 'Unknown' else 0)
# df = df[(df['Team & Contract'] == 0) | (df['Team & Contract'] >= 2024)]
df['Nom_annee'] = df.apply(lambda x : x['name'][0] + ' (' + str(2025 - x['Age']) + ')' , axis = 1)

df = df[~(df['name'].isna() == True)]
df = df[~(df['name'] == '')]

colonnes = list(df.columns)[16:-9]

colonnes.remove('Total skill')
colonnes.remove('Total movement')
colonnes.remove('Total power')
colonnes.remove('Total mentality')
colonnes.remove('Total defending')
colonnes.remove('Total goalkeeping')

df = df.drop(['Total skill', 'Total movement', 'Total power', 'Total mentality', 'Total defending', 'Total goalkeeping'], axis = 1)

for element in colonnes:
    df[element] = df[element].fillna(0)
    df[element] = df[element].astype(float)

attacking = colonnes[0:5]
skill = colonnes[5:10]
movement = colonnes[10:15]
power = colonnes[15:20]
mentality = colonnes[20:26]
defending = colonnes[26:29]
goalkeeping = colonnes[29:34]

# FONCTIONS

navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
url_base = 'https://sofifa.com/player/'
from bs4 import BeautifulSoup
import requests

def calcul(value):

    if value == []:
        value = value
    else:
        if type(value) == list:
            value = ''.join(value)
        
        if ' ' in value:
            value = value.replace(' ', '')
            
        if '+' in value:
            a, b = value.split('+')
            return int(a) + int(b)
        elif '-' in value:
            a, b = value.split('-')
            return int(a) - int(b)
        
        value = int(value)
    
    return value

def montant(salary):
    salary = str(salary)
    if len(salary) > 3:
        if len(salary) > 6:
            if len(salary) > 9:
                if len(salary) > 12:
                    salary = salary[:-12] + ' ' + salary[-12:-9] + ' ' + salary[-9:-6] + ' ' + salary[-6:-3] + ' ' + salary[-3:]
                else:
                    salary = salary[:-9] + ' ' + salary[-9:-6] + ' ' + salary[-6:-3] + ' ' + salary[-3:]
            else:
                salary = salary[:-6] + ' ' + salary[-6:-3] + ' ' + salary[-3:]
        else:
            salary = salary[:-3] + ' ' + salary[-3:]
    else:
        salary = salary

    salary = salary + ' €'

    return salary

# KNN

# Appliquer des poids 
colonnes_fixes = ['Age',  
                      'Overall rating',  
                      'Potential',  
                      'Heading accuracy', 
                      'Curve',  
                      'Acceleration', 
                      'Balance',
                      'Interceptions',
                      'Vision',  
                      'Base stats',
                      'International reputation',
                      'Pace / Diving',
                      'Shooting / Handling',
                      'Passing / Kicking',
                      'Dribbling / Reflexes',
                      'Defending / Pace',
                      'Height',
                      'Weight',
                      'Value',
                      'Wage',
                      'Release clause',
                      'Crossing',
                      'Short passing',
                      'Volleys',
                      'Dribbling',
                      'FK Accuracy',
                      'Long passing',
                      'Ball control',
                      'Sprint speed',
                      'Agility',
                      'Reactions', 
                      'Shot power',
                      'Jumping',
                      'Stamina',
                      'Strength',
                      'Long shots',
                      'Aggression',
                      'Att. Position',
                      'Penalties',
                      'Composure',
                      'Defensive awareness',
                      'Standing tackle',
                      'Sliding tackle',
                      'GK Diving',
                      'GK Handling',
                      'GK Kicking',
                      'GK Positioning',
                      'GK Reflexes',
                      'Best overall',
                      'Growth',
                      'Pied droit']




def poids_numerique(X, colonnes_fixes, poids_fixes_dict):
    # Appliquer les poids aux colonnes numériques existantes
    for col in colonnes_fixes:
        if col in X.columns:
            X[col] *= poids_fixes_dict[col]
    
    return X


# FONCTION 1
def encodage_X(X, type, colonnes_fixes, poids_fixes_dict):
    from sklearn.preprocessing import StandardScaler, MinMaxScaler

    index = X.index
    X_num = X.select_dtypes('number')
    X_str = X.select_dtypes('object')

    if type == 'standard':
        SN = StandardScaler()
    else:
        SN = MinMaxScaler()
   
    X_num_scaled = pd.DataFrame(SN.fit_transform(X_num), columns=X_num.columns, index=index)


    X_encoded = pd.concat([X_str[['name', 'ID']], poids_numerique(X_num_scaled, colonnes_fixes, poids_fixes_dict)], axis=1)
    X_encoded = X_encoded.dropna()

    return X_encoded, SN


# FONCTION 4

def joueurs_similaires(X_encoded, id_joueur, model, df_recherche):

  df_recherche['ID'] = df_recherche['ID'].astype(str)
  id_joueur = str(id_joueur)
  if id_joueur not in df_recherche['ID'].values:
      return f"Le Pokémon {id_joueur} n'est pas dans le dataset."
  
  joueur_a_predire = X_encoded[X_encoded['ID'] == id_joueur]

  i, indices = model.kneighbors(joueur_a_predire.select_dtypes(include=[np.number]))

  return df_recherche.iloc[indices[0]].reset_index(drop=True)



# STREAMLIT

df_recherche = df.copy()

if 'Unnamed: 0' in df_recherche.columns:
    df_recherche = df_recherche.drop(columns=['Unnamed: 0'], axis = 1)

# df_recherche = df_recherche.dropna()
df_recherche['ID'] = df_recherche['ID'].astype(str)

df_recherche['name'] = df_recherche['name'].apply(lambda x : ",".join(x) if type(x) == list else x)
df_recherche['name'] = df_recherche['name'].apply(lambda x : x.lower())

df_recherche4 = df_recherche.copy()

# Sélectionner un joueur similaire

st.header("👇 Trouvez un joueur similaire à ... :")

choix_joueur = st.text_input('Tapez le nom du joueur souhaité :')

resultat_nom = process.extract(choix_joueur, df_recherche['name'].to_list(), score_cutoff = 40, limit = 5)

recherche = choix_joueur.lower().split(" ")

for element in recherche:
    df_recherche2 = df_recherche[df_recherche['name'].str.contains(element)]
    df_recherche = df_recherche2

liste_df_recherche = []

for n in range(len(df_recherche)):
    liste_df_recherche.append(df_recherche['Nom_annee'].iloc[n])

if len(liste_df_recherche) == 0:

    liste_id_resultat_nom = []

    for n in range(len(resultat_nom)):
        id = df_recherche4[df_recherche4['name'] == resultat_nom[n][0]]['ID'].iloc[0]
        liste_id_resultat_nom.append(id)
    
    for m in range(len(liste_id_resultat_nom)):

        nom_annee = df_recherche4[df_recherche4['ID'] == liste_id_resultat_nom[m]]['Nom_annee'].iloc[0]
        liste_df_recherche.append(nom_annee)
    
    df_recherche = df_recherche4

if choix_joueur:    

    name = st.selectbox("Quel joueur parmi notre base précisément ?",(liste_df_recherche))

    poids_fixes_dict = {
                        'Age': 1,  
                        'Overall rating': 1,  
                        'Potential': 1,  
                        'Heading accuracy': 1, 
                        'Curve': 1,  
                        'Acceleration': 1, 
                        'Balance': 1,
                        'Interceptions': 1,
                        'Vision': 1,  
                        'Base stats': 1,
                        'International reputation': 1,
                        'Pace / Diving': 1,
                        'Shooting / Handling': 1,
                        'Passing / Kicking': 1,
                        'Dribbling / Reflexes': 1,
                        'Defending / Pace': 1,
                        'Height': 1,
                        'Weight': 1,
                        'Value': 1,
                        'Wage': 1,
                        'Release clause': 1,
                        'Crossing': 1,
                        'Short passing': 1,
                        'Volleys': 1,
                        'Dribbling': 1,
                        'FK Accuracy': 1,
                        'Long passing': 1,
                        'Ball control': 1,
                        'Sprint speed': 1,
                        'Agility': 1,
                        'Reactions': 1, 
                        'Shot power': 1,
                        'Jumping': 1,
                        'Stamina': 1,
                        'Strength': 1,
                        'Long shots': 1,
                        'Aggression': 1,
                        'Att. Position': 1,
                        'Penalties': 1,
                        'Composure': 1,
                        'Defensive awareness': 1,
                        'Standing tackle': 1,
                        'Sliding tackle': 1,
                        'GK Diving': 1,
                        'GK Handling': 1,
                        'GK Kicking': 1,
                        'GK Positioning': 1,
                        'GK Reflexes': 1,
                        'Best overall': 1,
                        'Growth': 1,
                        'Pied droit': 1
                        }

    liste_critere = list(poids_fixes_dict.keys())
    liste_critere.sort()

    critere = options = st.multiselect("Quels sont vos critères importants ?", liste_critere,)

    st.header("Parlons chiffres :")
        
    critere_budget = st.toggle("Avez-vous un critère de coût de transfert ?", value = False)

    if critere_budget:

        col1, col2 = st.columns(2)

        with col2:
            max_budget = st.text_input("Quel est le coût de transfert maximum ?", max(df['Value']), autocomplete= str(max(df['Value'])))
            
        with col1:
            min_budget = st.text_input("Quel est le coût de transfert minimum ?", min(df['Value']), autocomplete= str(max(df['Value'])))
        
        max_budget = int(max_budget) 
        min_budget = int(min_budget)

    critere_salaire = st.toggle("Avez-vous un critère de salaire ?", value = False)
    if critere_salaire:

        col1, col2 = st.columns(2)

        with col2:
            max_salaire = st.text_input("Quel est le salaire maximum ?", max(df['Wage']), autocomplete= str(max(df['Wage'])))

        with col1:
            min_salaire = st.text_input("Quel est le salaire minimum ?", min(df['Wage']), autocomplete= str(max(df['Wage'])))
            
        max_salaire = int(max_salaire)
        min_salaire = int(min_salaire)

    resultats = st.button("Voir les résultats", type = 'primary')

    if resultats:

        id_joueur = df_recherche['ID'].iloc[0]
        position = df_recherche['Best position'][df_recherche['ID'] == id_joueur].iloc[0]

        liste_def = ["CB", "RB", "LB"]
        liste_lat = ["RB", "RWB", "LB", "LWB"]
        liste_milieu_def = ["CDM", "CM"]
        liste_milieu_off = ["CAM", "LM", "RM"]
        liste_ailies = ["LM", "RM", "LW", "RW"]
        liste_att = ["RW", "LW", "ST", "CF"]
        gardien = ["GK"]
        liste_cara_gk = ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']

        if position in gardien :
            df_recherche = df[df['Best position'].isin(gardien)]
        else:
            if position in liste_def :
                df_recherche = df[df['Best position'].isin(liste_def)]
            elif position in liste_lat :
                df_recherche = df[df['Best position'].isin(liste_lat)]
            elif position in liste_milieu_def :
                df_recherche = df[df['Best position'].isin(liste_milieu_def)]
            elif position in liste_milieu_off :
                df_recherche = df[df['Best position'].isin(liste_milieu_off)]
            elif position in liste_ailies :
                df_recherche = df[df['Best position'].isin(liste_ailies)]
            elif position in liste_att :
                df_recherche = df[df['Best position'].isin(liste_att)]
            elif position in gardien :
                df_recherche = df[df['Best position'].isin(gardien)]

            for element in liste_cara_gk:
                for n in range(len(df_recherche)):
                    df_recherche[element].iloc[n] = 0

        if critere_budget:
            df_recherche = df_recherche[df_recherche['Value'] <= max_budget]
            df_recherche = df_recherche[df_recherche['Value'] >= min_budget]
        if critere_salaire:
            df_recherche = df_recherche[df_recherche['Wage'] <= max_salaire]
            df_recherche = df_recherche[df_recherche['Wage'] >= min_salaire]

        X = df_recherche.copy()
        
        X['ID'] = X['ID'].astype(str)
        X_encoded, SN = encodage_X(X, 'standard', colonnes_fixes, poids_fixes_dict)
        
        k=8
        model = NearestNeighbors(n_neighbors=k, metric='euclidean')
        model.fit(X_encoded.select_dtypes(include=['number']))
        resultat = joueurs_similaires(X_encoded, id_joueur, model, df_recherche)
  
        resultat = resultat.sort_values(by = 'Overall rating', ascending = False)

        df_final = resultat.copy()

        if resultats:

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown("<h6 style='text-align: center; color: white;'>Name</h6>", unsafe_allow_html=True)
            with col2:
                st.markdown("<h6 style='text-align: center; color: white;'>Overall rating</h6>", unsafe_allow_html=True)
            with col3:
                st.markdown("<h6 style='text-align: center; color: white;'>Salaire</h6>", unsafe_allow_html=True)
            with col4:
                st.markdown("<h6 style='text-align: center; color: white;'>Valeur</h6>", unsafe_allow_html=True)
            with col5:
                st.markdown("<h6 style='text-align: center; color: white;'>Fin de contrat</h6>", unsafe_allow_html=True)


            if len(critere) > 5:
                critere = critere[:5]
            p = len(critere)

            for n in range(len(df_final)):

                date_contrat = df_final['Team & Contract'].iloc[n]
                nom = df_final['Nom_annee'].iloc[n]
                score = df_final['Overall rating'].iloc[n]
                salary = df_final['Wage'].iloc[n]
                achat = df_final['Value'].iloc[n]

                col6, col7, col8, col9, col10 = st.columns(5)

                with col6:
                    st.markdown(f"<div style='text-align: center;'>{nom}</div>", unsafe_allow_html=True)
                with col7:
                    st.markdown(f"<div style='text-align: center;'>{score}</div>", unsafe_allow_html=True)
                with col8:
                    st.markdown(f"<div style='text-align: center;'>{montant(salary)}</div>", unsafe_allow_html=True)
                with col9:
                    st.markdown(f"<div style='text-align: center;'>{montant(achat)}</div>", unsafe_allow_html=True)
                with col10:
                    st.markdown(f"<div style='text-align: center;'>{date_contrat}</div>", unsafe_allow_html=True)


                if p == 1:
                    element = critere[p-1]
                    st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                elif p == 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        element = critere[p-2]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col2:
                        element = critere[p-1]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                elif p == 3:
                    col1, col2, col3, = st.columns(3)
                    with col1:
                        element = critere[p-3]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col2:
                        element = critere[p-2]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col3:
                        element = critere[p-1]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                elif p == 4:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        element = critere[p-4]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col2:
                        element = critere[p-3]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col3:
                        element = critere[p-2]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col4:
                        element = critere[p-1]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                elif p == 5:
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        element = critere[p-5]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col2:
                        element = critere[p-4]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col3:
                        element = critere[p-3]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col4:
                        element = critere[p-2]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)
                    with col5:
                        element = critere[p-1]
                        st.markdown(f"<div style='text-align: center;'>{element} : {df_final[element].iloc[n]}</div>", unsafe_allow_html=True)

                col11, col12 = st.columns(2)

                with col11:
                    dico_colonnes = {}
                    dico_colonnes = {'Attacking' : float(df_final[attacking].iloc[n].mean()),
                            'Skill' : float(df_final[skill].iloc[n].mean()),
                            'Movement' : float(df_final[movement].iloc[n].mean()),
                            'Power' : float(df_final[power].iloc[n].mean()),
                            'Mentality' : float(df_final[mentality].iloc[n].mean()),
                            'Defending': float(df_final[defending].iloc[n].mean()),
                            'Goalkeeping' : float(df_final[goalkeeping].iloc[n].mean())}

                    data = pd.DataFrame.from_dict(dico_colonnes, orient = 'index').reset_index()

                    data = data.rename({'index' : 'theta',
                                        0 : 'r'},
                                    axis = 1)

                    if int(data['r'].sum()) > 0:
                        st.markdown("""
                            <style>
                                .page-break { page-break-before: always; }
                            </style>
                        """, unsafe_allow_html=True)
                        st.markdown("""
                            <style>
                                .page-break { page-break-before: always; }
                            </style>
                        """, unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align: center;'>Statistiques Globale : {int(round(data['r'].mean(), 0))}</div>", unsafe_allow_html=True)
                        fig = px.line_polar(data, r = 'r', theta= 'theta', line_close=True)
                        fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])))

                        st.plotly_chart(fig)

                with col12:
                
                    attaque = ['RW', 'LW', 'CF']
                    milieu = ['RM', 'LM', 'CDM', 'CAM', 'CM']
                    defense = ['RB', 'LB', 'CB']
                    gardien = ['GK']

                    poste = df_final['Best position'].iloc[n]

                    if poste in attaque:
                        colonnes_spé = attacking
                    elif poste in defense:
                        colonnes_spé = defending
                    elif poste in milieu:
                        colonnes_spé = movement
                    elif poste in gardien:
                        colonnes_spé = goalkeeping

                    df_final_stats = df_final[colonnes_spé]
                    dico_colonnes2 = {}

                    for element in colonnes_spé:
                        dico_colonnes2.update({element : df_final_stats[element].iloc[n]})

                    data = pd.DataFrame.from_dict(dico_colonnes2, orient = 'index').reset_index()

                    data = data.rename({'index' : 'theta',
                                        0 : 'r'},
                                    axis = 1)
                    if int(data['r'].sum()) > 0:

                        st.markdown("""
                            <style>
                                .page-break { page-break-before: always; }
                            </style>
                        """, unsafe_allow_html=True)
                        st.markdown("""
                            <style>
                                .page-break { page-break-before: always; }
                            </style>
                        """, unsafe_allow_html=True)
                    
                        st.markdown(f"<div style='text-align: center;'>Statistiques Spécifiques : {int(round(data['r'].mean(), 0))}</div>", unsafe_allow_html=True)
                        
                        fig = px.line_polar(data, r = 'r', theta= 'theta', line_close=True)
                        fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])))

                        st.plotly_chart(fig)
                    
                st.markdown("""---""")

        


