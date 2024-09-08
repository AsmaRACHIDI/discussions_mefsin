import io
import pandas as pd

from flask import Flask, render_template, request, send_file, redirect, url_for
from inference.inference_script import annotate_a_message


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
        
        prediction_motif, prediction_sous_motif = annotate_a_message(discussion_title=title, comment=message)

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
        prediction_motif, prediction_sous_motif = annotate_a_message(discussion_title=title, comment=message)

        # Redirigez vers la page /results avec les données du formulaire
        return redirect(url_for("sandbox_result", title=title, message=message, prediction_motif=prediction_motif, prediction_sous_motif=prediction_sous_motif))

##################### Dataset : Visualiser et Télécharger #################################################################

@app.route('/dataset')
def dataset():
    # Charger le fichier JSON en tant que DataFrame
    df = pd.read_json("app/static/data/test.json")
    df = df.reset_index()
    
    # Obtenir les colonnes et les données
    columns = df.columns.tolist()
    data = df.values.tolist()
    
    return render_template('dataset.html', columns=columns, data=data)


@app.route('/dataset/download/csv')
def download_csv():
    df = pd.read_json("app/static/data/test.json")
    output = io.StringIO()
    df.to_csv(output, index=False)
    return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name="dataset.csv")

@app.route('/dataset/download/excel')
def download_excel():
    df = pd.read_json("app/static/data/test.json")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="dataset.xlsx")

@app.route('/dataset/download/json')
def download_json():
    return send_file("app/static/data/test.json", as_attachment=True)


##################### Barre latérale : Menu #################################################################

# @app.route("/sidebar-page")
# def sidebar_page():
#     return render_template("sidebar-page.html")

if __name__ == '__main__':
    app.run(debug=True)
