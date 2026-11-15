from django.shortcuts import render

def home(request):
    return render(request, 'detector/index.html')
# Cre your views here.
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .predictor import model, scaler

import pandas as pd
import numpy as np
import io
@csrf_exempt
def predict_attack(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if file is None:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            # 1. Lecture saine du fichier CSV
            file_text = io.StringIO(file.read().decode('utf-8-sig'))
            df = pd.read_csv(file_text, sep=None, engine='python', header=None)
            
            # 2. Conversion forcée en numérique
            df = df.apply(pd.to_numeric, errors='coerce')
            
            # Suppression des lignes contenant des valeurs manquantes (NaN) au cas où
            df = df.dropna()

            total_lignes = len(df)
            if total_lignes == 0:
                return JsonResponse({"error": "Le fichier CSV ne contient aucune ligne de données valide."}, status=400)

            # 3. Prédiction de TOUTES les lignes d'un coup
            features_matrix = df.values
            features_scaled = scaler.transform(features_matrix)
            
            predictions = model.predict(features_scaled)
            probabilites = model.predict_proba(features_scaled).max(axis=1)

            # 4. Calcul des statistiques
            # On suppose que 1 = Attaque et 0 = Normal
            nb_attaques = int(np.sum(predictions == 1))
            nb_normal = int(np.sum(predictions == 0))
            
            taux_attaque = round((nb_attaques / total_lignes) * 100, 2)
            probabilite_moyenne = round(float(np.mean(probabilites)) * 100, 2)

            # 5. Réponse JSON enrichie
            return JsonResponse({
                "total_rows": total_lignes,
                "attacks": nb_attaques,
                "normal": nb_normal,
                "attack_percentage": taux_attaque,
                "average_probability": probabilite_moyenne,
                # On détermine le statut global basé sur la présence d'au moins une attaque
                "global_threat": True if nb_attaques > 0 else False 
            })

        except Exception as e:
            print("⚠️ ERREUR MULTI-LIGNES :", str(e))
            return JsonResponse({"error": str(e)}, status=500)
