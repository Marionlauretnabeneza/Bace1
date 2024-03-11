# -*- coding: utf-8 -*-
"""Selection Icc BACE1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z_1FlVTJ2qE8AzWkXTEkrx32RjQR_fIw
"""

pip install scanpy

pip install we-get

pip install you-get

pip install plotly

pip install mdtraj

pip install biopython pandas

pip install mdtraj pandas

pip install pytest

pip install mdtraj pandas requests

pip install parmed

pip install gemmi

<<<<<<< Updated upstream
=======
pip install rcsbsearchapi

pip install nglview

pip install requests

>>>>>>> Stashed changes
#from google.colab import drive
#drive.mount('/content/drive')

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import statsmodels.sandbox.stats.multicomp as sm
from scipy.stats import spearmanr
import scanpy as sc
import anndata
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import seaborn as sns
import mdtraj as md
import pandas as pd
import gemmi
import requests
from io import StringIO
import tempfile
import os
from tkinter import Tk, filedialog
import os
import shutil
<<<<<<< Updated upstream

"""1/ Données CSV from RSCB
filtered on
  1) Résolution
  2) Poids moléculaires
  3) Binding Affinity
"""

df = pd.read_csv(r"/content/(1)rcsb_pdb_custom_report.csv")
df.drop(df.index[:0], inplace=True)
# Remplacer les noms de colonnes par la première ligne
df.columns = df.iloc[0]

# Supprimer la première ligne qui contenait les anciens noms de colonnes
df = df[1:]

# Réindexer le DataFrame après la suppression de la première ligne
df.reset_index(drop=True, inplace=True)
df.set_index(df.columns[0], inplace=True)
df = df.dropna(subset=['Resolution (Å)'])
df.head(2)

df6=df.T
df6['5MCQ']

#1) extraire les données en fonction de leur résolution Å <2, WM,

# Convertir la colonne 'Resolution (Å)' en nombres
df['Resolution (Å)'] = pd.to_numeric(df['Resolution (Å)'], errors='coerce')
df['Ligand MW'] = pd.to_numeric(df['Ligand MW'], errors='coerce')
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
df['Number of Water Molecules per Deposited Model'] = pd.to_numeric(df['Number of Water Molecules per Deposited Model'])


=======
import webbrowser
from rcsbsearchapi import rcsb_attributes as attrs, TextQuery
from rcsbsearchapi.search import TextQuery, AttributeQuery, Attr
from rcsbsearchapi.const import CHEMICAL_ATTRIBUTE_SEARCH_SERVICE, STRUCTURE_ATTRIBUTE_SEARCH_SERVICE
import nglview
import json
import requests
from matplotlib import cm
import re

"""##RCSB Query

#1) criteria´ pdb

if you need to consult directly the pdb file on RCSB you can have the url of the site that give te result of the query advanced research. Just input the :Input_Gene_name = input("Enter Gene name: ")
Input_structure_title1 = input("Enter Structure title 1: ")
Input_structure_title2 = input("Enter Structure title 2: ")
#2) rcsbsearchapi
Access the RCSB advanced search directly from python: rcsbsearchapi.readthedocs.io

##Operator syntax

    Uses python comparison operators for basic attributes (==, <, <=, etc)
    Combine using set operators (&, |, ~, etc)
    Execute queries as functions

### e.g

  ´|´ (pipe or vertical bar): Logical OR operator.

  ´&´ is used for logical AND.

  (q2 & q3 & q4) represents a group of conditions joined by AND within parentheses.

  q1 & (q2 & q3 & q4) combines the condition q1 with the group in parentheses using the logical AND operation.

  ~ correspond a  'negation': True
"""

# User input for replacing keywords
Input_Gene_name = input("Enter Gene name: ")
Input_structure_title1 = input("Enter Structure title 1: ")
Input_structure_title2 = input("Enter Structure title 2: ")

# Original URL template with placeholders for keywords
url_template = (
    "https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22full_text%22%2C%22parameters%22%3A%7B%22value%22%3A%22{gene_name}%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22full_text%22%7D%2C%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22struct.title%22%2C%22operator%22%3A%22contains_phrase%22%2C%22value%22%3A%22{title_1}%22%2C%22negation%22%3Afalse%7D%7D%2C%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22struct.title%22%2C%22operator%22%3A%22contains_phrase%22%2C%22negation%22%3Afalse%2C%22value%22%3A%22{title_2}%22%7D%7D%5D%2C%22logical_operator%22%3A%22or%22%7D%2C%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_entity_source_organism.taxonomy_lineage.name%22%2C%22operator%22%3A%22exact_match%22%2C%22negation%22%3Afalse%2C%22value%22%3A%22Homo%20sapiens%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%2C%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text_chem%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22chem_comp.type%22%2C%22operator%22%3A%22exact_match%22%2C%22negation%22%3Afalse%2C%22value%22%3A%22peptide%20linking%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text_chem%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%22bc9fa4a269b60d22e6cfbce75b176a2e%22%7D%7D"
)

# Replace placeholders with user input
url = url_template.format(
    gene_name=Input_Gene_name,
    title_1=Input_structure_title1,
    title_2=Input_structure_title2,
)
print( "\nThe url of the rcsb query is\n: ",url,"\n")

#OR
q1a = Attr("struct.title").contains_phrase(Input_structure_title1 )
q1b = Attr("struct.title").contains_phrase(Input_structure_title2)
q2 = Attr("rcsb_entity_source_organism.rcsb_gene_name.value").exact_match(Input_Gene_name )
#AND
q3 = Attr("rcsb_entity_source_organism.taxonomy_lineage.name").exact_match("Homo sapiens")
#q4 = Attr("rcsb_polymer_entity.rcsb_ec_lineage.name").exact_match("Oxidoreductases")
q4 = AttributeQuery("chem_comp.type", "exact_match", "peptide linking",
    CHEMICAL_ATTRIBUTE_SEARCH_SERVICE) # this constant specifies "text_chem" service

query = (q1a | q1b |q2) & q3  & q4

print("The count of the PDBS IDs of with the title",Input_structure_title1  ,"is\n",q1a.count())
print("The count of the PDBS IDs of with the title",Input_structure_title2  ,"is\n",q1b.count())
print("The count of the PDBS IDs of with the gene name",Input_Gene_name ,"is\n",q2.count())
print("The count of the PDBS IDs of with that is an rcsb_entity_source_organism.taxonomy_lineage.name Homo Sapiens \n",q3.count())
print("The count of the PDBS IDs that the chemical structure is a peptide likeing is \n",q4.count())
print("The count of the selectionned PDBS IDs is \n",query.count())

nouveaux_entry_ids = list(query())

# Creating the query string for the IDs
query_string = '%2C'.join(['%22' + entry_id + '%22' for entry_id in nouveaux_entry_ids])

# Construction of the URL with the new list of IDs
url2 = f'https://data.rcsb.org/graphql/index.html?query=%7B%0A%20%20entries(entry_ids%3A%20%5B{query_string}%5D)%0A%20%20%7B%0A%20%20%20%20rcsb_id%0A%20%20%20%20exptl_crystal_grow%20%7B%0A%20%20%20%20%20%20pH%0A%20%20%20%20%7D%0A%20%20%20%20pubmed%20%7B%0A%20%20%20%20%20%20rcsb_pubmed_doi%0A%20%20%20%20%7D%0A%20%20%20%20rcsb_binding_affinity%20%7B%0A%20%20%20%20%20%20value%0A%20%20%20%20%7D%0A%20%20%20%20rcsb_entry_container_identifiers%20%7B%0A%20%20%20%20%20%20entry_id%0A%20%20%20%20%7D%0A%20%20%20%20rcsb_entry_info%20%7B%0A%20%20%20%20%20%20deposited_solvent_atom_count%0A%20%20%20%20%20%20resolution_combined%0A%20%20%20%20%7D%0A%20%20%20%20refine%20%7B%0A%20%20%20%20%20%20B_iso_mean%0A%20%20%20%20%7D%0A%20%20%20%20nonpolymer_entities%20%7B%0A%20%20%20%20%20%20nonpolymer_comp%20%7B%0A%20%20%20%20%20%20%20%20chem_comp%20%7B%0A%20%20%20%20%20%20%20%20%20%20formula_weight%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D"%20%20%7D%0A%20%20%7D%0A%7D'

print( "\nThe url of the rcsb query_ result_ json_file is\n: ",url2,"\n")

# Demander à l'utilisateur de saisir le contenu JSON
rcsb_query_result_json_script = input("Please enter the JSON content for script: ")
rcsb_query_result_json_file = input("Please enter the JSON content for file: ")

# Charger le JSON
rcsb_query_result_json_file = json.loads(rcsb_query_result_json_file)

# Extraire les entrées du fichier JSON
entries = rcsb_query_result_json_file['data']['entries']

# Créer un DataFrame pandas
rcsb_query_result_pd_file   = pd.json_normalize(entries).set_index('rcsb_id')

column_mapping = {
    "exptl_crystal_grow": "pH",
    "rcsb_binding_affinity":"Binding Affinity",
    "pubmed.rcsb_pubmed_doi":"pubmed.doi",
    "nonpolymer_entities":'Ligand MW',
    "refine": "B_Factor mean",
    "rcsb_entry_container_identifiers.entry_id": "PDB ID",
    "rcsb_entry_info.deposited_solvent_atom_count": "Number of Water Molecules per Deposited Model",
    "rcsb_entry_info.resolution_combined": "Resolution (Å)"
    # Ajoutez d'autres mappings ici pour les autres colonnes
}
rcsb_query_result_pd_file = rcsb_query_result_pd_file.rename(columns=column_mapping)

# Extraire le pH
rcsb_query_result_pd_file["pH"] = rcsb_query_result_pd_file["pH"].apply(lambda x: x[0]["pH"] if isinstance(x, list) and x else None)
# Extraire la valeur de B_iso_mean de la colonne "refine"
rcsb_query_result_pd_file["B_Factor mean"] = rcsb_query_result_pd_file["B_Factor mean"].apply(lambda x: x[0]["B_iso_mean"] if isinstance(x, list) and x else None)
# Extraire la valeur de l'affinité de liaison
rcsb_query_result_pd_file["Binding Affinity"] = rcsb_query_result_pd_file["Binding Affinity"].apply(lambda x: x[0]["value"] if isinstance(x, list) and x else None)
# Extraire la valeur de B_iso_mean de la colonne "refine"
rcsb_query_result_pd_file["Resolution (Å)"] = rcsb_query_result_pd_file["Resolution (Å)"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
# Extraire la valeur de "formula_weight" de la colonne "nonpolymer_entities"
rcsb_query_result_pd_file['Ligand MW'] = rcsb_query_result_pd_file['Ligand MW'].apply(lambda x: x[0]["nonpolymer_comp"]["chem_comp"]["formula_weight"] if isinstance(x, list) and len(x) > 0 else None)

ID =  input("Please enter GENE ID: ")

# Enregistrez le DataFrame dans un fichier CSV
rcsb_query_result_pd_file.to_csv(f'rcsb_pdb_{ID}_query_result.csv', index=True)

"""#Données CSV from RSCB to parse the optimal ligand
filtered on

  1) Résolution

  2) Poids moléculaires
  
  3) Binding Affinity
"""

df = rcsb_query_result_pd_file

df = df.dropna(subset=['Resolution (Å)','Binding Affinity','Ligand MW'])
len(df)

type(rcsb_query_result_pd_file )

"""##1) Parsing pdb file parameters

Parse
  - df = total
  - Resolution : df1 = df[df['Resolution (Å)'] <= 2]
  - Molecular Wight MW : df2 = df1[df1['Ligand MW'] >= 400]
  - Bindind Affinity valeur df3 = df2[(df2['Binding Affinity'] >= 0) & (df2['Binding Affinity'] <= 10)]

Using this list, we will parse and select the 10 optimal samples. In a second time, we´ll extract the prm files obtain from CHARMM-GUI of the complexes and obtain a list of these samples classified according to the lowest penalty frequency. Finally we will select 5 of the first elements which we will reorganize according to their highest molecular weight.

In conclusion, an analysis of the residue composition of the ligand will be done to select the complex that will have the best stability.

"""

# Convert the column 'Resolution (Å)' to numeric
df['Resolution (Å)'] = pd.to_numeric(df['Resolution (Å)'], errors='coerce')
df['Ligand MW'] = pd.to_numeric(df['Ligand MW'], errors='coerce')
df['Binding Affinity'] = pd.to_numeric(df['Binding Affinity'], errors='coerce')
df['Number of Water Molecules per Deposited Model'] = pd.to_numeric(df['Number of Water Molecules per Deposited Model'])

>>>>>>> Stashed changes
dfseuil= df[['Resolution (Å)','Number of Water Molecules per Deposited Model']]
dfseuil.head()
dfseuil = dfseuil.dropna()

<<<<<<< Updated upstream
dfseuil= df[['Resolution (Å)','Number of Water Molecules per Deposited Model']]
dfseuil.head()
dfseuil = dfseuil.dropna()
# Détermination du Seuil de résolution optimale par rapport au nombre de molécules d'eau
X = dfseuil[['Resolution (Å)']].values
y = dfseuil['Number of Water Molecules per Deposited Model'].values

# Initialiser le modèle de régression linéaire
model = LinearRegression()

# Ajuster le modèle aux données
model.fit(X, y)

# Prédire la quantité d'eau en fonction de la variable A
predictions = model.predict(X)

# Tracer le graphique de la régression linéaire
=======
# Determination of the optimal resolution threshold in relation to the number of water molecules

X = dfseuil[['Resolution (Å)']].values
y = dfseuil['Number of Water Molecules per Deposited Model'].values

# Initialize the linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(X, y)

# Predict the amount of water based on variable A
predictions = model.predict(X)

# Plot the linear regression graph to establish the threshold between water and resolution
>>>>>>> Stashed changes
plt.scatter(X, y, color='lightblue', label='Données')
plt.plot(X, predictions, color='red', label='Régression linéaire')
plt.xlabel('Variable A')
plt.ylabel('Quantité d\'eau')
plt.title('Régression Linéaire entre Variable A et Quantité d\'eau')
plt.legend()
<<<<<<< Updated upstream
plt.show()

len(df)

"""2) Sélectionné en fonction du pénalty

Parser en fonction des paramètres
  - df = total
  - Résolution : df1 = df[df['Resolution (Å)'] <= 2]
  - Poids moléculaires : df2 = df1[df1['Ligand MW'] >= 400]
  - Bindind valeur df3 = df2[(df2['Value'] >= 0) & (df2['Value'] <= 10)]

Grâce à cette liste, on va parser on va sélectionner les 10 échantillons, extraire les fichiers prm des complexes et obtenir une liste de ces échantillons classés selon la fréquence de pénalité la plus faible. Enfin on sélectionnera 5 des premiers éléments que l'on réorganisera selon leur poids moléuclaire le plus élevé. Pour finaliser la sélection, une analyse de la composition en résidus du ligand sera faite pour sélectionner le complexe qui aura la meilleure stabilité.
"""

# Filtrer les lignes où la colonne 'Resolution (Å)' est inférieure ou égale à 2
df1 = df[df['Resolution (Å)'] <= 2]
df2 = df1[df1['Ligand MW'] >= 400]
df3 = df2[(df2['Value'] >= 0) & (df2['Value'] <= 10)]
=======

plt.savefig(f'linear_regression_graph_of_{Input_Gene_name}_to_establish_the_threshold_between_water_and_resolution.png')


plt.show()

# Filter rows where the 'Resolution (Å)' column is less than or equal to 2
df1 = df[df['Resolution (Å)'] <= 2]
# Filter rows where the 'Molecular weight' column is more than or equal to 400kDa
df2 = df1[df1['Ligand MW'] >= 400]
# Filter rows where the 'Bindind affinity = Value' column is more than or equal to 0-10
df3 = df2[(df2['Binding Affinity'] >= 0) & (df2['Binding Affinity'] <= 10)]
# Sort the values in function of more elevated Molecular weight
df3 = df3.sort_values(by='Ligand MW', ascending=False)
>>>>>>> Stashed changes
print(" on a"  ,len(df)," initialement")
print(" on a"  ,len(df1)," qui ont une résolution inférieure à 2Å")
print(" on a ",len(df2)," qui ont le poids moléculaire est supérieure ou égale à 400kDa")
print(" on a " ,len(df3), " qui ont une valeur de binding comprise entre 0 et 10")

<<<<<<< Updated upstream
df3.sort_values(by='Ligand MW', ascending=False)

# Liste des codes PDB
pdb_codes = df3.index

element = "5MCQ"
if element in df2.index:
    print(f"L'élément {element} est présent dans la colonne d'index.")
else:
    print(f"L'élément {element} n'est pas présent dans la colonne d'index.")

"""LISTE des fichiers .prm en input"""
=======
# Liste des codes PDB

pdb_codes = df3.head(10)
pdb_codes.to_csv('Top_10_pdbid.csv', index=False)
print("\nThe list of the Top 10 PDBs" ,{}, "parsed is :\n",pdb_codes.index)

df3.head(10)

"""##2)Selected based on penalty

LISTE des fichiers .prm en input

pour BACE1

    '/content/2IQG.prm',
                  '/content/2VNM.prm',
                  '/content/2VNN.prm',
                  '/content/2XFK.prm',
                  '/content/3CIC.prm',
                  '/content/3CID.prm',
                  '/content/4DI2.prm',
                  '/content/4GID.prm',
                  '/content/2G94.prm'
"""
>>>>>>> Stashed changes

liste_fichiers = ['/content/2IQG.prm',
                  '/content/2VNM.prm',
                  '/content/2VNN.prm',
                  '/content/2XFK.prm',
                  '/content/3CIC.prm',
                  '/content/3CID.prm',
                  '/content/4DI2.prm',
                  '/content/4GID.prm',
                  '/content/2G94.prm']
<<<<<<< Updated upstream
df3['prm_penalty %']=None

"""TEST de calcul de la fréquence de pénalité

*   2IQG
=======

"""TEST de calcul de la fréquence de pénalité

*   e.g : 2IQG
>>>>>>> Stashed changes
*   Élément de liste


"""

<<<<<<< Updated upstream
# Chemin du fichier
chemin_fichier = '/content/2IQG.prm'

with open(chemin_fichier, 'r') as fichier:
      # Lire le contenu du fichier et stocker chaque ligne dans une liste
  lignes = fichier.readlines()

# Créer un DataFrame à partir de la liste de lignes
df5 = pd.DataFrame(lignes, columns=['Contenu'])

# Afficher le DataFrame
df5.head(4)

# Créer une colonne qui correspond au parsing du %penalty
df5['Nouvelle_Colonne'] = df5['Contenu'].str.extract(r' penalty= (.*)', expand=False)
df5['Nouvelle_Colonne'] = pd.to_numeric(df5['Nouvelle_Colonne'], errors='coerce')


# Calculer la fréquence de pénalty pour chaque complexe
=======
# File path
chemin_fichier = '/content/2IQG.prm'

with open(chemin_fichier, 'r') as fichier:
      # Read the contents of the file and store each line in a list
  lignes = fichier.readlines()

# Create a DataFrame from the Row List
df5 = pd.DataFrame(lignes, columns=['Contenu'])

# Show DataFrame
df5.head(4)

# Create a column that corresponds to the %penalty analysis
df5['Nouvelle_Colonne'] = df5['Contenu'].str.extract(r' penalty= (.*)', expand=False)
df5['Nouvelle_Colonne'] = pd.to_numeric(df5['Nouvelle_Colonne'], errors='coerce')

# Calculate the penalty frequency for each complex
>>>>>>> Stashed changes
Nb = 0
pen = 0

for i in df5['Nouvelle_Colonne']:
    if i >= 0:
        Nb = Nb + 1
    if i < 50:
        pen = pen + 1

<<<<<<< Updated upstream
# Éviter la division par zéro
=======
# Avoid division by zero
>>>>>>> Stashed changes
if Nb != 0:
    Freq_penalty = pen / Nb
    print("Freq_penalty = ",Freq_penalty,"%")
else:
    print("/content/2IQG.prm}Division par zéro évitée. Nb est égal à zéro.")

<<<<<<< Updated upstream
"""Calcule de la fréquence de pénalité pour chaque fichier.prm"""
=======
"""Calculate the penalty frequency for each .prm file"""
>>>>>>> Stashed changes

def calculer_freq_penalty(df_colonne):
    Nb = 0
    pen = 0

    for i in df_colonne:
        if i >= 0:
            Nb += 1

<<<<<<< Updated upstream
        # si somme des %pen >10 /Total %pen <20% on a un seuil de pénalité bas.
        if i > 10:
            pen += 1
    print(pen)
    # Éviter la division par zéro
=======
        # if sum of %pen >10 /Total %pen <20% we have a low penalty threshold.
        if i > 10:
            pen += 1
    print(pen)
    # Avoid division by zero
>>>>>>> Stashed changes
    if Nb != 0:
        Freq_penalty = pen / Nb
        return Freq_penalty
    else:
        print("Division par zéro évitée. Nb est égal à zéro.")
        return 0  # Return 0 instead of None

def trouver_index_par_chemin(df, chemin):
<<<<<<< Updated upstream
    # Extraire le nom du fichier du chemin
    ID = chemin.split('/')[-1].split('.')[0]
    print(ID)

    # Trouver l'index correspondant au nom du fichier dans la colonne 'Nom_Fichier'
=======
    # Extract file name from path
    ID = chemin.split('/')[-1].split('.')[0]
    print(ID)

    # Find the index corresponding to the file name in the 'File_Name' column
>>>>>>> Stashed changes
    index = df3.index[df3.index == ID].tolist()
    if index:
        return index[0]
    else:
        print(f"Le fichier {ID} n'a pas été trouvé dans la colonne 'Nom_Fichier' du DataFrame.")
        return None

<<<<<<< Updated upstream
# Chemin du fichier
chemin_fichier = liste_fichiers

# Initialiser une liste pour stocker les fréquences
freq_penalty_data = []

# Lire chaque fichier et calculer la fréquence de pénalité
for fichier in liste_fichiers:
    #Ouvrir le fichier.prm
    with open(fichier, 'r') as file:
        lignes = file.readlines()

    # Créer un DataFrame pour le fichier actuel : df_freq = fichier d'où l'on calcule la fréquence de pénalité du complexe
=======
# Path file
chemin_fichier = liste_fichiers

# Initialize a list to store frequencies
freq_penalty_data = []

# Read each file and calculate the penalty frequency
for fichier in liste_fichiers:
    # Open the .prm file
    with open(fichier, 'r') as file:
        lignes = file.readlines()

    # Create a DataFrame for the current file: df_freq = file from which we calculate the penalty frequency of the complex
>>>>>>> Stashed changes
    df_freq = pd.DataFrame(lignes, columns=['Contenu'])
    df_freq['Nouvelle_Colonne'] = df_freq['Contenu'].str.extract(r' penalty= (.*)', expand=False)
    df_freq['Nouvelle_Colonne'] = pd.to_numeric(df_freq['Nouvelle_Colonne'], errors='coerce')
    df_freq['Nouvelle_Colonne'] = df_freq['Nouvelle_Colonne'].astype(float)

<<<<<<< Updated upstream
    # Calcul de la fréquence de penalty
    freq_penalty_result = calculer_freq_penalty(df_freq['Nouvelle_Colonne'])

    # Trouver l'index correspondant dans le DataFrame principal df
=======
    # Calculation of penalty frequency
    freq_penalty_result = calculer_freq_penalty(df_freq['Nouvelle_Colonne'])

    # Find the corresponding index in the main DataFrame df
>>>>>>> Stashed changes
    index = trouver_index_par_chemin(df, fichier)

    if index is not None:
        if freq_penalty_result is not None:
            print(freq_penalty_result)
<<<<<<< Updated upstream
            # Ajouter les données de freq_penalty à la liste
            freq_penalty_data.append({'Nom_Fichier': index, 'Freq_Penalty': freq_penalty_result * 100})

            print(f"Fréquence Penalty pour {index} : {freq_penalty_result * 100}%")
        else:
            print("La fréquence de pénalité est None, ne pas ajouter à la liste.")

import matplotlib.pyplot as plt
from matplotlib import cm

# Filtrer les lignes où la colonne 'Resolution (Å)' est inférieure ou égale à 2
df1 = df[df['Resolution (Å)'] <= 2]
df2 = df1[df1['Ligand MW'] >= 400]
df3 = df2[(df2['Value'] >= 0) & (df2['Value'] <= 10)]
# Parseuer en fonction de la fréquence de pénalty
=======
            # Add freq_penalty data to list
            freq_penalty_data.append({'Nom_Fichier': index, 'Freq_Penalty': freq_penalty_result * 100})

            print(f"Penalty frequency for {index}: {freq_penalty_result * 100}%")
        else:
            print("Penalty frequency is None, not adding to the list.")

# Parse based on penalty frequency
>>>>>>> Stashed changes
penalty = pd.DataFrame(freq_penalty_data)
penalty.set_index('Nom_Fichier', inplace=True)

for i in df3.index:
    if i in penalty.index:
        df3.loc[i, 'Freq_penalty'] = penalty.loc[i, 'Freq_Penalty']
    else:
        df3.loc[i, 'Freq_penalty'] = None

df4 = df3[(df3['Freq_penalty'] >= 0) & (df3['Freq_penalty'] <= 20)]

<<<<<<< Updated upstream
# Transformer la colonne 'Freq_penalty' en données numériques
df4['Freq_penalty'] = pd.to_numeric(df4['Freq_penalty'], errors='coerce')

# Assurez-vous que la colonne est de type numérique
df4['Freq_penalty'] = df4['Freq_penalty'].astype(float)

# Tri par ordre décroissant en fonction de 'Freq_penalty' et qui ont un poids moléculaire >500
df5 = df4.sort_values(by='Ligand MW', ascending=True)

# Créer un graphique à barres pour visualiser les variations de la longueur des DataFrames
noms_des_groupes = ['Total', 'Résolution <= 2Å',' MW >=400 ', 'Affinity [5-10]nM', 'penalty <20%']
=======
# Transform 'Freq_penalty' column into numeric data
df4['Freq_penalty'] = pd.to_numeric(df4['Freq_penalty'], errors='coerce')

# Make sure the column is of numeric type
df4['Freq_penalty'] = df4['Freq_penalty'].astype(float)

# Sort in descending order based on 'Freq_penalty' and have a molecular weight >500
df5 = df4.sort_values(by='Ligand MW', ascending=True)

"""# 4) Results of the Selection

Show the results of the analysis steps until the final selection based on the number of missing elements

  Filter rows where the 'Resolution (Å)' column is less than or equal to 2

    df1 = df[df['Resolution (Å)'] <= 2]
  Filter rows where the 'Molecular weight' column is more than or equal to 400kDa

    df2 = df1[df1['Ligand MW'] >= 400]
  Filter rows where the 'Bindind affinity = Value' column is more than or equal to [0-10]
    
    df3 = df2[(df2['Value'] >= 0) & (df2['Value'] <= 10)]

  Parse based on penalty frequency  [0-20] %

    df4 = df3[(df3['Freq_penalty'] >= 0) & (df3['Freq_penalty'] <= 20)]
"""

# Create a bar chart to visualize variations in the number of parsed IDs
noms_des_groupes = ['Total', 'Resolution <= 2Å',' MW >=400 ', 'Affinity [5-10]nM', 'penalty <20%']
>>>>>>> Stashed changes
valeurs_des_groupes = [len(df), len(df1),len(df2),len(df3),len(df4)]

fig, ax = plt.subplots()

<<<<<<< Updated upstream
# Utiliser une colormap de bleu
couleurs = cm.Blues([0.2, 0.4, 0.6, 0.8, 1.0,1,2])

# Ajouter les barres au graphique avec le dégradé de couleur bleu
bars = ax.bar(noms_des_groupes, valeurs_des_groupes, color=couleurs)

# Ajouter des valeurs au-dessus de chaque barre
for bar, valeur in zip(bars, valeurs_des_groupes):
    height = bar.get_height()
    ax.annotate(f'{valeur}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points de décalage vers le haut
                textcoords="offset points",
                ha='center', va='bottom')

# Mettre en diagonale les éléments de la légende
plt.xticks(rotation=45)

# Ajouter des titres et des labels
plt.title('Selection du ligand optimal de BACE1 en fonction des paramètres')
plt.ylabel('Nombre de ligand ID')

# Récupérer le chemin complet du bureau
bureau_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Afficher le graphique
plt.show()

print('nombre Total=',len(df))
print('nombre filtré pour Résolution <= 2Å=',len(df1))
print('nombre filtré pour MW >= 400=',len(df2))
print('nombre filtré pour Affinité [5-10]nM=',len(df3))
print('nombre filtré pour Penalty < 20%=',len(df4))
print('nombre filtré pour Top high MW',len(df5))
print('la sélection Top high MW est ', df5.index)
=======
# Use a blue colormap
couleurs = cm.Blues([0.2, 0.4, 0.6, 0.8, 1.0,1,2])

# Add the bars to the chart with the blue color gradient
bars = ax.bar(noms_des_groupes, valeurs_des_groupes, color=couleurs)

# Add values ​​above each bar
for bar, valeur in zip(bars, valeurs_des_groupes):
    height = bar.get_height()
    ax.annotate(f'{valeur}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points of upward shift
                textcoords="offset points",
                ha='center', va='bottom')

# 3 points of upward shift
plt.xticks(rotation=45)

# Add titles and labels
plt.title(f"Selection of the optimal ligand for {Input_Gene_name}")
plt.ylabel('ligand ID')

# Get the full desktop path
bureau_path = os.path.join(os.path.expanduser("~"), "Desktop")

plt.savefig(f'Selection of the optimal ligand for {Input_Gene_name}.png')


# Show chart
plt.show()

print('Total number=', len(df))
print('Number filtered for Resolution <= 2Å=', len(df1))
print('Number filtered for MW >= 400=', len(df2))
print('Number filtered for Affinity [5-10]nM=', len(df3))
print('Number filtered for Penalty < 20%=', len(df4))
print('Number filtered for Top high MW', len(df5))
print('The selection for Top high MW is ', df5.index)
>>>>>>> Stashed changes

# Spécifiez le chemin du fichier CSV
chemin_csv = "Top_selection_BACE1.csv"

# Exportez le DataFrame en fichier CSV
df5.to_csv(chemin_csv, index=False)

# Spécifiez le chemin de destination pour le téléchargement
chemin_destination = "/Content"

# Copiez simplement le fichier vers le chemin de destination
shutil.copy(chemin_csv, chemin_destination)
# Affichez un message indiquant que le fichier CSV a été créé et téléchargé
print(f"Le DataFrame a été exporté dans {chemin_csv}")
<<<<<<< Updated upstream
print(f"Le fichier a été copié vers {chemin_destination}")
=======
print(f"Le fichier a été copié vers {chemin_destination}")
>>>>>>> Stashed changes
