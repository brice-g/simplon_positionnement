import csv
import urllib.request
import io

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv'

reponse = urllib.request.urlopen(url)
contenu = reponse.read().decode('utf-8')
fichier_virtuel = io.StringIO(contenu)

ventes_par_produit = {}

lecteur = csv.DictReader(fichier_virtuel)
for ligne in lecteur:
    nom_produit = ligne['produit']
    quantite = int(ligne['qte'])
    
    if nom_produit in ventes_par_produit:
        ventes_par_produit[nom_produit] += quantite
    else:
        ventes_par_produit[nom_produit] = quantite

produit_max = max(ventes_par_produit, key=ventes_par_produit.get)
produit_min = min(ventes_par_produit, key=ventes_par_produit.get)

print(f"Plus vendu : {produit_max} ({ventes_par_produit[produit_max]} unités)")
print(f"Moins vendu : {produit_min} ({ventes_par_produit[produit_min]} unités)")