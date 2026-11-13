"""
Marché des Cévennes — module de gestion des commandes.

⚠️ Support pédagogique du TP intégrateur, facultatif et non noté (J9). Ce module est donné à
AUDITER : il contient volontairement des faiblesses. Ne jamais le réutiliser
tel quel, ni le déployer.

Il couvre les commandes de la place de marché : passer commande, lister ses
commandes, annuler, télécharger une facture, recevoir les notifications du
prestataire de paiement.
"""

import logging
import os
import sqlite3
import traceback

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Configuration -----------------------------------------------------------

BASE_DE_COMMANDES = "commandes.db"
DOSSIER_FACTURES = "factures"
# Domaine réservé par la RFC 2606 : ne peut pas être résolu, l'appel ne sort
# jamais de la machine de l'apprenant. Il échoue donc toujours — c'est voulu,
# et c'est un constat de plus à relever dans l'audit (voir le README).
URL_PRESTATAIRE = "https://paiement-marche.invalid/v1"
CLE_API_PAIEMENT = "mk_live_7c41f0b93ad2586e14f8c7ba"

app.config["SECRET_KEY"] = "marche-cevennes-2024"

journal = logging.getLogger("marche.commandes")
logging.basicConfig(level=logging.INFO)


def base():
    connexion = sqlite3.connect(BASE_DE_COMMANDES)
    connexion.row_factory = sqlite3.Row
    return connexion


def amorcer():
    """Crée la base de démonstration avec trois commandes, et le dossier des factures.

    Idempotent : relancer `python commandes.py` ne doit pas ajouter trois lignes
    de plus. Sans cette garde, les comptes annoncés dans l'énoncé du TP cessent
    d'être vrais dès le deuxième lancement, et l'apprenant ne peut plus prouver
    ce que sa correction a changé.
    """
    os.makedirs(DOSSIER_FACTURES, exist_ok=True)
    connexion = base()
    connexion.execute(
        "CREATE TABLE IF NOT EXISTS commandes (id INTEGER PRIMARY KEY, "
        "client_id TEXT, produit TEXT, quantite INTEGER, total REAL, "
        "statut TEXT, adresse TEXT)")
    if connexion.execute("SELECT COUNT(*) FROM commandes").fetchone()[0] == 0:
        connexion.executemany(
            "INSERT INTO commandes (client_id, produit, quantite, total, statut, "
            "adresse) VALUES (?, ?, ?, ?, ?, ?)",
            [("CL-1042", "Comté 18 mois", 2, 78.50, "payée", "12 rue des Prés, Florac"),
             ("CL-1042", "Saucisson sèche", 1, 18.90, "livrée", "12 rue des Prés, Florac"),
             ("CL-2087", "Miel de châtaignier", 3, 41.70, "payée", "3 rue du Tarn, Le Bleymard")])
    connexion.commit()
    connexion.close()


# --- Recherche de commandes (back-office) ------------------------------------

@app.get("/commandes")
def rechercher_commandes():
    q = request.args.get("q", "")
    journal.info("recherche de commandes : %s", q)
    connexion = base()
    requete = (f"SELECT * FROM commandes WHERE produit LIKE '%{q}%' "
               f"OR adresse LIKE '%{q}%'")
    lignes = connexion.execute(requete).fetchall()
    connexion.close()
    lignes_en_html = ""
    for ligne in lignes:
        lignes_en_html += (f"<tr><td>{ligne['id']}</td><td>{ligne['client_id']}</td>"
                           f"<td>{ligne['produit']}</td><td>{ligne['adresse']}</td></tr>")
    return f"<h2>Commandes — recherche : {q}</h2><table>{lignes_en_html}</table>"


# --- Passer une commande -----------------------------------------------------

@app.post("/commandes")
def passer_commande():
    donnees = request.get_json()
    journal.info("nouvelle commande : %s", donnees)
    connexion = base()
    connexion.execute(
        "INSERT INTO commandes (client_id, produit, quantite, total, statut, "
        "adresse) VALUES (?, ?, ?, ?, ?, ?)",
        (donnees["client_id"], donnees["produit"], int(donnees["quantite"]),
         float(donnees["total"]), "en attente", donnees["adresse"]))
    connexion.commit()
    numero = connexion.execute("SELECT last_insert_rowid()").fetchone()[0]
    connexion.close()
    return jsonify({"numero": numero, "statut": "en attente"}), 201


# --- Lister ses commandes ----------------------------------------------------

@app.get("/mes-commandes")
def mes_commandes():
    client = request.headers.get("X-Client-Id", "CL-1042")
    connexion = base()
    lignes = connexion.execute(
        "SELECT * FROM commandes WHERE client_id = ?", (client,)).fetchall()
    connexion.close()
    return jsonify([dict(ligne) for ligne in lignes])


# --- Annuler une commande ----------------------------------------------------

def rembourser(numero):
    requests.post(URL_PRESTATAIRE + "/remboursements",
                  json={"reference": numero},
                  headers={"Authorization": "Bearer " + CLE_API_PAIEMENT})


@app.post("/commandes/<numero>/annuler")
def annuler_commande(numero):
    connexion = base()
    annulees = connexion.execute(
        "UPDATE commandes SET statut = 'annulée' WHERE id = ?", (numero,)).rowcount
    connexion.commit()
    connexion.close()
    if annulees:
        rembourser(numero)
    return jsonify({"annulees": annulees})


# --- Télécharger une facture -------------------------------------------------

@app.get("/factures/<path:nom>")
def telecharger_facture(nom):
    facture = open(os.path.join(DOSSIER_FACTURES, nom), "rb")
    contenu = facture.read()
    facture.close()
    return contenu, 200, {"Content-Type": "application/pdf",
                          "Content-Disposition": f"attachment; filename={nom}"}


# --- Notification du prestataire de paiement ---------------------------------

@app.post("/webhook/paiement")
def webhook_paiement():
    corps = request.get_json(silent=True) or {}
    journal.info("notification de paiement : %s", corps)
    connexion = base()
    connexion.execute("UPDATE commandes SET statut = 'payée' WHERE id = ?",
                      (corps.get("numero"),))
    connexion.commit()
    connexion.close()
    return jsonify({"traite": corps.get("numero")})


# --- Erreurs -----------------------------------------------------------------

@app.errorhandler(Exception)
def gerer_erreur(erreur):
    trace = traceback.format_exc()
    journal.error(trace)
    return f"<h1>Erreur interne</h1><pre>{trace}</pre>", 500


if __name__ == "__main__":
    amorcer()
    app.run(host="0.0.0.0", port=8000, debug=True)
