import os
import sys
import zipfile

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from inference.preprocess import preprocess_data

from inference import categories

# Accédez aux dictionnaires définis dans categories.py
labels = categories.LABELS
id2label = categories.ID2LABEL
label2id = categories.LABEL2ID

sslabels = categories.SSLABELS
id2sslabel = categories.ID2SSLABEL
sslabel2id = categories.SSLABEL2ID


def load_model_from_zip(model_zip, extraction_number):
    extract_dir = f"/home/asma/Documents/open-data-discussions/trained_models/extracted_model{extraction_number}"

    with zipfile.ZipFile(model_zip, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    model = AutoModelForSequenceClassification.from_pretrained(extract_dir)
    tokenizer = AutoTokenizer.from_pretrained(extract_dir)

    return model, tokenizer


def perform_inference(model, tokenizer, input_dataframe, is_second_preprocess=False):
    print(f"Inférence modèle {'2' if is_second_preprocess else '1'} :")
    preprocessed_data = preprocess_data(input_dataframe, is_second_preprocess)
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


def annotate_data_from_csv_file(input_csv_df_mefsin="/home/asma/Documents/open-data-discussions/app/static/data/dataset.csv", output_csv_file_model="app/static/data/models_predicted_data.csv"):
    model1_zip_file = "/home/asma/Documents/open-data-discussions/trained_models/bert-finetuned-my-data-final_archive.zip"
    model2_zip_file = "/home/asma/Documents/open-data-discussions/trained_models/bert-finetuned-my-data-final2_archive2.zip"

    # Chargez et préparez les modèles
    model1, tokenizer1 = load_model_from_zip(model1_zip_file, 1)
    model2, tokenizer2 = load_model_from_zip(model2_zip_file, 2)

    # Chargez le DataFrame d'entrée
    df = pd.read_csv(input_csv_df_mefsin, delimiter=';')

    # Effectuez l'inférence avec le modèle 1
    predictions_model1 = perform_inference(model1, tokenizer1, df)
    df["prediction_motif"] = [id2label[prediction] for prediction in predictions_model1]

    # Effectuez l'inférence avec le modèle 2 en spécifiant is_second_preprocess=True
    predictions_model2 = perform_inference(model2, tokenizer2, df, is_second_preprocess=True)
    df["prediction_sous_motif"] = [id2sslabel[prediction] for prediction in predictions_model2]

    # Enregistrez les DataFrames de sortie au format CSV
    df.to_csv(output_csv_file_model, index=False)

    print("Les données ont été annotées avec succès !")

    return df


def annotate_a_message(title, message):
    extract_dir1 = f"/home/asma/Documents/open-data-discussions/trained_models/extracted_model1"
    extract_dir2 = f"/home/asma/Documents/open-data-discussions/trained_models/extracted_model2"

    # Charger et préparer les modèles
    model1 = AutoModelForSequenceClassification.from_pretrained(extract_dir1)
    model2 = AutoModelForSequenceClassification.from_pretrained(extract_dir2)
    tokenizer1 = AutoTokenizer.from_pretrained(extract_dir1)
    tokenizer2 = AutoTokenizer.from_pretrained(extract_dir2)

    df = pd.DataFrame([{'title': title, 'first_message': message}])
    df.to_csv("data/res_inferance.csv", sep=';', index=False)

    # Inférence avec le modèle 1
    predictions_model1 = perform_inference(model1, tokenizer1, df)
    df["prediction_motif"] = [id2label[predictions_model1[0]]]
    prediction_motif = df["prediction_motif"][0]

    # Inférence avec le modèle 2
    predictions_model2 = perform_inference(model2, tokenizer2, df, is_second_preprocess=True)
    df["prediction_sous_motif"] = [id2sslabel[predictions_model2[0]]]
    prediction_sous_motif = df["prediction_sous_motif"][0]

    print("Les données ont été annotées avec succès !")

    return prediction_motif, prediction_sous_motif


#annotate_data_from_csv_file(input_csv_df_mefsin="/home/asma/Documents/open-data-discussions/dataset.csv", output_csv_file_model="test.csv")

#prediction_motif, prediction_sous_motif = annotate_a_message("Problème d'accès aux données", "Bonjour, j'essaye d'accéder aux données mais je n'y arrive pas. Merci de m'aider. Cordialement.")
#print("Catégorie prédite:", prediction_motif)
#print("Sous-catégorie prédite:", prediction_sous_motif)
