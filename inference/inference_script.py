import os
import sys
import zipfile

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

sys.path.append("/home/oem/Documents/open-data-discussions")

from inference.preprocess import preprocess_data
from inference import categories
from core.config import Config

# Accédez aux dictionnaires définis dans categories.py
labels = categories.LABELS
id2label = categories.ID2LABEL
label2id = categories.LABEL2ID

sslabels = categories.SSLABELS
id2sslabel = categories.ID2SSLABEL
sslabel2id = categories.SSLABEL2ID


model1_zip_file = "../trained_models/bert-finetuned-my-data-final_archive.zip"
model2_zip_file = "../trained_models/bert-finetuned-my-data-final2_archive2.zip"


def load_model_from_zip(model_zip, extraction_number):
    extract_dir = f"/home/oem/Documents/open-data-discussions/trained_models/extracted_model{extraction_number}"

    with zipfile.ZipFile(model_zip, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    model = AutoModelForSequenceClassification.from_pretrained(extract_dir)
    tokenizer = AutoTokenizer.from_pretrained(extract_dir)

    return model, tokenizer


def perform_inference(model, tokenizer, input_data, is_second_preprocess=False):
    print(f"Inférence modèle {'2' if is_second_preprocess else '1'} :")

    # Vérifie si l'entrée est déjà un DataFrame ou s'il s'agit d'un dict comme pour les fichiers json
    if isinstance(input_data, pd.DataFrame):
        df = input_data
    else:
        df = pd.DataFrame([input_data])  # df = pd.DataFrame([{'title': title, 'comment': comment}])

    # Préprocesser les données
    preprocessed_data = preprocess_data(df, is_second_preprocess)
    if preprocessed_data is None:
        raise ValueError("La fonction preprocess_data a renvoyé None. Veuillez vérifier la fonction.")

    predictions = []
    batch_size = 16
    num_batches = len(preprocessed_data) // batch_size + int(len(preprocessed_data) % batch_size > 0)
    model.eval()

    for i in range(num_batches):
        batch_texts = preprocessed_data[i * batch_size : (i + 1) * batch_size]
        with torch.no_grad():
            encoded_inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
            outputs = model(**encoded_inputs)
        predicted_labels = torch.argmax(outputs.logits, dim=1)
        predictions.extend(predicted_labels.tolist())

    print("Inférence terminée !")
    return predictions


def annotate_data_from_json(input_json):
    # Chargez et préparez les modèles
    model1_zip = Config.MODEL1_ZIP_FILE
    model2_zip = Config.MODEL2_ZIP_FILE
    model1, tokenizer1 = load_model_from_zip(model1_zip, 1)
    model2, tokenizer2 = load_model_from_zip(model2_zip, 2)

    # Effectuez l'inférence avec le modèle 1
    predictions_model1 = perform_inference(model1, tokenizer1, input_json)
    input_json["prediction_motif"] = id2label[predictions_model1[0]]

    # Effectuez l'inférence avec le modèle 2 en spécifiant is_second_preprocess=True
    predictions_model2 = perform_inference(model2, tokenizer2, input_json, is_second_preprocess=True)
    input_json["prediction_sous_motif"] = id2sslabel[predictions_model2[0]]

    print("Les données ont été annotées avec succès !")

    # Retourne le JSON annoté
    return input_json


def annotate_a_message(discussion_title, comment):
    # Extraire et charger les modèles
    model1_zip = Config.MODEL1_ZIP_FILE
    model2_zip = Config.MODEL2_ZIP_FILE
    model1, tokenizer1 = load_model_from_zip(model1_zip, 1)
    model2, tokenizer2 = load_model_from_zip(model2_zip, 2)

    # Créer un dictionnaire avec le titre et le message
    input_data = {"discussion_title": discussion_title, "comment": comment}

    # Inférence avec le modèle 1
    predictions_model1 = perform_inference(model1, tokenizer1, input_data)
    input_data["prediction_motif"] = id2label[predictions_model1[0]]
    prediction_motif = input_data["prediction_motif"]

    # Inférence avec le modèle 2
    predictions_model2 = perform_inference(model2, tokenizer2, input_data, is_second_preprocess=True)
    input_data["prediction_sous_motif"] = id2sslabel[predictions_model2[0]]
    prediction_sous_motif = input_data["prediction_sous_motif"]

    print("Les données ont été annotées avec succès !")

    return prediction_motif, prediction_sous_motif


# annotate_data_from_csv_file(input_csv_df_mefsin="/home/oem/Documents/open-data-discussions/app/static/data/data_gouv_discussions.csv")

# prediction_motif, prediction_sous_motif = annotate_a_message("Problème d'accès aux données", "Bonjour, j'essaye d'accéder aux données mais je n'y arrive pas. Merci de m'aider. Cordialement.")
# print("Catégorie prédite:", prediction_motif)
# print("Sous-catégorie prédite:", prediction_sous_motif)
