import os
import sys
import zipfile
import pandas as pd
import torch
import categories
import nltk
import re

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Accédez aux dictionnaires définis dans categories.py
labels = categories.LABELS
id2label = categories.ID2LABEL
label2id = categories.LABEL2ID

sslabels = categories.SSLABELS
id2sslabel = categories.ID2SSLABEL
sslabel2id = categories.SSLABEL2ID

class Inference:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model_from_zip(self, model_zip):
        extract_dir = "extracted_model"

        with zipfile.ZipFile(model_zip, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        self.model = AutoModelForSequenceClassification.from_pretrained(extract_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(extract_dir)


    # Fonction de prétraitement pour encoder les exemples et ajouter les labels
    def preprocess(self, examples, is_second_preprocess=False):
        try:
            print(f"Prétraitement des données en cours... {'(2)' if is_second_preprocess else '(1)'}")
            
            if is_second_preprocess:
                combined_text = (
                    examples["prediction_motif"] + " " + examples["title"] + " " + examples["first_message"]
                )
            else:
                combined_text = examples["title"] + " " + examples["first_message"]

            # Nettoyage du texte
            # Convertir chaque texte en minuscules
            combined_text = [text.lower() for text in combined_text]
            # Supprimer les chiffres
            combined_text = [re.sub(r"\d+", "", text) for text in combined_text]
            # Supprimer les adresses mail
            combined_text = [re.sub(r"\S+@\S+", "", text) for text in combined_text]
            # Supprimer les caractères de ponctuation sauf les apostrophes et les accents
            combined_text = [re.sub(r"[^\w\s'-.]", "", text) for text in combined_text]
            # Supprimer certains mots vides
            words_to_remove = ["bonjour", "bonsoir", "bonne journée","cordialement","merci", "janvier", "février", "mars", "avril", "mai","juin","juillet","août","aout","septembre","octobre","novembre","décembre",
            ]
            combined_text = [[word for word in text.split() if word not in words_to_remove] for text in combined_text]
            combined_text = [" ".join(text) for text in combined_text]
            # Supprimer les espaces en trop et les sauts de lignes
            combined_text = [re.sub(r"\s+", " ", text) for text in combined_text]
            combined_text = [text.strip() for text in combined_text]
            #logging.info("Prétraitement des données terminé.")
            print("Prétraitement des données terminé !")

            return combined_text

        except Exception as e:
            print(f"Erreur lors du prétraitement des données {'(2)' if is_second_preprocess else '(1)'} : {str(e)}")
            return None

    def perform_inference(self, input_dataframe, is_second_preprocess=False):
        if self.model is None or self.tokenizer is None:
            raise ValueError("Le modèle et le tokenizer doivent être chargés avant d'effectuer l'inférence.")

        print(f"Inférence modèle {'2' if is_second_preprocess else '1'} :")
        preprocessed_data = self.preprocess(input_dataframe, is_second_preprocess)
        if preprocessed_data is None:
            raise ValueError("La fonction preprocess_data a renvoyé None. Veuillez vérifier la fonction.")

        predictions = []
        batch_size = 16
        num_batches = len(preprocessed_data) // batch_size + int(len(preprocessed_data) % batch_size > 0)
        self.model.eval()
        
        for i in range(num_batches):
            batch_texts = preprocessed_data[i * batch_size : (i + 1) * batch_size]
            with torch.no_grad():
                encoded_inputs = self.tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
                outputs = self.model(**encoded_inputs)
            predicted_labels = torch.argmax(outputs.logits, dim=1)
            predictions.extend(predicted_labels.tolist())

        print("Inférence terminée !")
        return predictions

if __name__ == "__main__":
    model1_zip_file = "../trained_models/bert-finetuned-my-data-final_archive.zip"
    model2_zip_file = "../trained_models/bert-finetuned-my-data-final2_archive2.zip"
    input_csv_df_mefsin = "../output.csv"
    output_csv_file_model = "models_predicted_data.csv"

    inference = Inference()

    # Chargez et préparez les modèles
    inference.load_model_from_zip(model1_zip_file)
    inference.load_model_from_zip(model2_zip_file)

    # Chargez le DataFrame d'entrée
    df = pd.read_csv(input_csv_df_mefsin, delimiter=',')

    # Effectuez l'inférence avec le modèle 1
    predictions_model1 = inference.perform_inference(df)
    df["prediction_motif"] = [id2label[prediction] for prediction in predictions_model1]

    # Effectuez l'inférence avec le modèle 2 en spécifiant is_second_preprocess=True
    predictions_model2 = inference.perform_inference(df, is_second_preprocess=True)
    df["prediction_sous_motif"] = [id2sslabel[prediction] for prediction in predictions_model2]

    # Enregistrez les DataFrames de sortie au format CSV
    df.to_csv(output_csv_file_model, index=False)

    print("Les données ont été annotées avec succès !")
