import io
import pandas as pd
import base64

from flask import Flask, render_template, request, send_file, redirect, url_for
from inference.inference_script import annotate_a_message


app = Flask(__name__, template_folder="app/templates", static_folder='app/static')

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

##################### Dashboard #################################################################

@app.route("/")
def dashboard():
    return render_template('dashboard.html')

##################### JOUER AVEC L'IA : FORMULAIRE #################################################################
# Page choix du mode d'annotation
@app.route("/form/choose", methods=["GET"])
def choose_annotation_mode():
    return render_template("sandbox-choose.html")

# Page mode annotation manuelle
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
        title = request.args.get("title")
        message = request.args.get("message")
        prediction_motif = request.args.get("prediction_motif")
        prediction_sous_motif = request.args.get("prediction_sous_motif")
        
        # Affichez les résultats sur la page /results
        return render_template("sandbox-result.html", title=title, message=message, prediction_motif=prediction_motif, prediction_sous_motif=prediction_sous_motif)
    elif request.method == "POST":
        # Traitement pour la méthode POST
        title = request.form.get("title")
        message = request.form.get("message")
        prediction_motif, prediction_sous_motif = annotate_a_message(discussion_title=title, comment=message)

        # Redirigez vers la page /results avec les données du formulaire
        return redirect(url_for("sandbox_result", title=title, message=message, prediction_motif=prediction_motif, prediction_sous_motif=prediction_sous_motif))

# Page mode annotation automatique (Fichier)
@app.route("/form/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        # Affiche le formulaire de téléchargement
        return render_template("sandbox-upload.html", file_processed=False, download_file=None)
    elif request.method == "POST":
        uploaded_file = request.files.get("file")

        if not uploaded_file:
            return "Aucun fichier sélectionné", 400

        try:
            # Détermine le type de fichier et charge dans un DataFrame
            if uploaded_file.filename.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                file_type = "csv"
            elif uploaded_file.filename.endswith(".json"):
                df = pd.read_json(uploaded_file)
                file_type = "json"
            elif uploaded_file.filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
                file_type = "excel"
            else:
                return "Format de fichier non supporté. Veuillez utiliser un fichier CSV, JSON ou Excel.", 400

            # Vérifie que les colonnes nécessaires existent
            if not {"title", "message"}.issubset(df.columns):
                return "Le fichier doit contenir les colonnes 'title' et 'message'.", 400

            # Applique les prédictions pour chaque ligne
            df["prediction_motif"], df["prediction_sous_motif"] = zip(
                *df.apply(lambda row: annotate_a_message(row["title"], row["message"]), axis=1)
            )

            # Prépare le fichier annoté dans le même format que l'entrée
            output = io.BytesIO()
            if file_type == "csv":
                df.to_csv(output, index=False)
                output.seek(0)
                mimetype = "text/csv"
                download_name = "annotated_results.csv"
            elif file_type == "json":
                output.write(df.to_json(orient="records").encode())
                output.seek(0)
                mimetype = "application/json"
                download_name = "annotated_results.json"
            elif file_type == "excel":
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)
                mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                download_name = "annotated_results.xlsx"

            # Retourne le fichier annoté et indique que le fichier a été traité
            return render_template("sandbox-upload.html", 
                                   file_processed=True, 
                                   download_file=output.getvalue(), 
                                   download_name=download_name, 
                                   mimetype=mimetype)
        except Exception as e:
            return f"Erreur lors du traitement du fichier : {e}", 500

        
##################### Dataset : Visualiser et Télécharger #################################################################

@app.route('/dataset')
def dataset():
    # Charger le fichier JSON en tant que DataFrame
    df = pd.read_json("app/static/data/test.json")
    df = df.reset_index()

    # Obtenir les colonnes et les données
    columns = df.columns.tolist()
    data = df.values.tolist()

    # Extraire les valeurs uniques pour les filtres
    sources = df['source'].unique().tolist()
    publishers = df['dataset_publisher'].unique().tolist()
    motifs = df['prediction_motif'].unique().tolist()
    sous_motifs = df['prediction_sous_motif'].unique().tolist()

    return render_template('dataset.html', columns=columns, data=data, sources=sources, publishers=publishers, motifs=motifs, sous_motifs=sous_motifs)


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
    app.run(host='0.0.0.0', port=5000, debug=True)
