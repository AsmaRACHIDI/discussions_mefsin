import io
import json
import pandas as pd
import plotly.express as px

from flask import Flask, render_template, request, send_file, redirect, url_for
from flask import jsonify
from inference.inference_script import annotate_a_message
from inference import categories


app = Flask(__name__, template_folder="app/templates", static_folder='app/static')

##################### Dashboard #################################################################

@app.route("/")
def dashboard():
    return render_template('dashboard.html')

##################### JOUER AVEC L'IA : FORMULAIRE #################################################################

# Route pour le formulaire de la sandbox
@app.route("/form", methods=["GET", "POST"])
def sandbox_route():
    if request.method == "GET":
        return render_template("sandbox-form.html")
    elif request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        
        prediction_motif, prediction_sous_motif = annotate_a_message(title=title, message=message)

        # Redirigez vers la page /results avec les données du formulaire
        return redirect(url_for("sandbox_result", title=title, message=message, prediction_motif=prediction_motif, prediction_sous_motif=prediction_sous_motif))

@app.route("/form/results", methods=["GET", "POST"])
def sandbox_result():
    if request.method == "GET":
        # Traitement pour la méthode GET
        # Récupérez les données passées depuis le formulaire
        title = request.args.get("title")
        message = request.args.get("message")
        prediction_motif = request.args.get("prediction_motif")
        prediction_sous_motif = request.args.get("prediction_sous_motif")
        
        # Affichez les résultats sur la page /results
        return render_template("sandbox-result.html", title=title, message=message, prediction_motif=prediction_motif, prediction_sous_motif=prediction_sous_motif)
    elif request.method == "POST":
        # Traitement pour la méthode POST
        # Effectuez le traitement du formulaire POST ici si nécessaire
        title = request.form.get("title")
        message = request.form.get("message")
        prediction_motif, prediction_sous_motif = annotate_a_message(title=title, message=message)

        # Redirigez vers la page /results avec les données du formulaire
        return redirect(url_for("sandbox_result", title=title, message=message, prediction_motif=prediction_motif, prediction_sous_motif=prediction_sous_motif))

##################### Dataset : Visualiser et Télécharger #################################################################

@app.route('/dataset')
def dataset():
    # Charger le fichier CSV en tant que DataFrame
    df = pd.read_csv("app/static/data/data_gouv_discussions.csv", delimiter=",")
    df = df.reset_index()
    # Convertir le DataFrame en un dictionnaire de listes
    data_dict = df.to_dict(orient='split')
    columns = data_dict['columns']
    data = data_dict['data']
    return render_template('dataset.html', columns=columns, data=data)

@app.route('/dataset/download/csv')
def download_csv():
    return send_file("app/static/data/data_gouv_discussions.csv", as_attachment=True)

@app.route('/dataset/download/excel')
def download_excel():
    # Télécharger le fichier Excel
    df = pd.read_csv("app/static/data/data_gouv_discussions.csv", delimiter=",")
    output = 'dataset.xlsx'
    df.to_excel(output, index=False)
    return send_file(output, as_attachment=True)

@app.route('/dataset/download/json')
def download_json():
    # Charger le fichier CSV en tant que DataFrame
    df = pd.read_csv("app/static/data/data_gouv_discussions.csv", delimiter=",")
    
    # Convertir le DataFrame en JSON
    output = df.to_json(orient='records')
    
    # Envoyer les données JSON en tant que fichier téléchargeable
    return send_file(io.BytesIO(output.encode()), 
                     mimetype="application/json", 
                     as_attachment=True, 
                     download_name="dataset.json")

##################### Barre latérale : Menu #################################################################

# @app.route("/sidebar-page")
# def sidebar_page():
#     return render_template("sidebar-page.html")

if __name__ == '__main__':
    app.run(debug=True)
