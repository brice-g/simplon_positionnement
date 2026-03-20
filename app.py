import plotly.express as px
import pandas as pd
import os
from flask import Flask, send_from_directory

données = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

figure = px.pie(données, values='qte', names='region', title='quantité vendue par région')

figure.write_html('ventes-par-region.html')

print('ventes-par-région.html généré avec succès !')

# Calcul du Chiffre d'Affaires (CA)
données['CA'] = données['prix'] * données['qte']

# A : Moyenne et Médiane (CA et Volume)
stats_a = données.groupby('produit').agg({
    'CA': ['mean', 'median'],
    'qte': ['mean', 'median']
}).reset_index()

stats_a.columns = ['produit', 'CA_Moyenne', 'CA_Mediane', 'Vol_Moyenne', 'Vol_Mediane']

fig_a = px.bar(stats_a, 
               x='produit', 
               y=['CA_Moyenne', 'CA_Mediane'],
               barmode='group',
               title='Analyse A : Moyenne vs Médiane du CA par Produit',
               labels={'value': 'Montant (€)', 'variable': 'Indicateur'})

fig_a.write_html('analyse_a_moyenne_mediane.html')


# B : Écart-type et Variance (Volume uniquement)
stats_b = données.groupby('produit')['qte'].agg(['std', 'var']).reset_index()

stats_b.columns = ['produit', 'Vol_Ecart_Type', 'Vol_Variance']

fig_b = px.bar(stats_b, 
               x='produit', 
               y='Vol_Variance',
               title='Analyse B : Variance du Volume des Ventes par Produit',
               color='produit',
               labels={'Vol_Variance': 'Variance'})

fig_b.write_html('analyse_b_dispersion.html')

print("Calculs terminés avec succès !")
print("- Fichier 'analyse_a_moyenne_mediane.html' généré.")
print("- Fichier 'analyse_b_dispersion.html' généré.")

# résumé par produit (Somme totale)
ventes_totales = données.groupby('produit').agg({
    'qte': 'sum',
    'CA': 'sum'
}).reset_index()

# --- GRAPHIQUE A : Ventes par produit (Volume) ---
fig_ventes = px.bar(ventes_totales, 
                    x='produit', 
                    y='qte',
                    title='Total des unités vendues par produit',
                    labels={'qte': 'Nombre d\'unités', 'produit': 'Produit'},
                    color='produit',
                    text_auto=True) # Affiche le chiffre au-dessus des barres

fig_ventes.write_html('ventes_par_produit.html')


# --- GRAPHIQUE B : Chiffre d'affaires par produit ---
fig_ca = px.bar(ventes_totales, 
                x='produit', 
                y='CA',
                title='Chiffre d\'affaires total par produit',
                labels={'CA': 'Chiffre d\'affaires (€)', 'produit': 'Produit'},
                color='produit',
                text_auto='.2f') # Affiche le CA avec 2 décimales

fig_ca.write_html('ca_par_produit.html')

print("Nouveaux graphiques générés :")
print("ventes_par_produit.html")
print("ca_par_produit.html")

# --- AJOUT DU SERVEUR WEB ---
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Résultats de l'analyse</h1>
    <ul>
        <li><a href="/graph1">Ventes par région</a></li>
        <li><a href="/graph2">Moyenne et Médiane</a></li>
        <li><a href="/graph3">Ecart-type et variance</a></li>
        <li><a href="/graph4">ventes par produit</a></li>
        <li><a href="/graph5">chiffre d'affaires par produit</a></li>
    </ul>
    """

@app.route('/graph1')
def show_graph1():
    return send_from_directory('.', 'ventes-par-region.html')

@app.route('/graph2')
def show_graph2():
    return send_from_directory('.', 'analyse_a_moyenne_mediane.html')

@app.route('/graph3')
def show_graph3():
    return send_from_directory('.', 'analyse_b_dispersion.html')

@app.route('/graph4')
def show_graph4():
    return send_from_directory('.', 'ventes_par_produit.html')

@app.route('/graph5')
def show_graph5():
    return send_from_directory('.', 'ca_par_produit.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)