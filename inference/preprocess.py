import logging
import os
import re

import nltk
import pandas as pd

nltk.download("stopwords")


# Fonction de prétraitement pour encoder les exemples et ajouter les labels
def preprocess_data(examples, is_second_preprocess=False):
    try:
        #logging.info(f"Prétraitement des données en cours... {'(2)' if is_second_preprocess else '(1)'}")
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
        words_to_remove = ["bonjour", "bonsoir", "bonne journée","cordialement","merci", "janvier", "février", "mars", "avril", "mai","juin","juillet","août","aout","septembre","octobre","novembre","décembre"]
        combined_text = [[word for word in text.split() if word not in words_to_remove] for text in combined_text]
        combined_text = [" ".join(text) for text in combined_text]
        # Supprimer les espaces en trop et les sauts de lignes
        combined_text = [re.sub(r"\s+", " ", text) for text in combined_text]
        combined_text = [text.strip() for text in combined_text]
        #logging.info("Prétraitement des données terminé.")
        print("Prétraitement des données terminé !")

        return combined_text

    except Exception as e:
        #logging.error(f"Erreur lors du prétraitement des données {'(2)' if is_second_preprocess else '(1)'} : {str(e)}")
        print(f"Erreur lors du prétraitement des données {'(2)' if is_second_preprocess else '(1)'} : {str(e)}")
        return None