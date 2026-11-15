import os
import django

# 1. Configurer l'environnement Django (remplacez 'intrusion_project' par le nom exact de votre dossier de projet si différent)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intrusion_project.settings')
django.setup()

# 2. Importer maintenant vos modules en toute sécurité
from detector.predictor import scaler, model

print("\n--- 🔍 ANALYSE DE VOTRE MODÈLE ---")
if hasattr(scaler, 'n_features_in_'):
    print(f"Nombre total de colonnes (features) attendues par le scaler : {scaler.n_features_in_}")
else:
    print("Impossible de déterminer le nombre de colonnes via le scaler.")

if hasattr(scaler, 'feature_names_in_'):
    print("\nListe des colonnes attendues dans l'ordre strict :")
    print(list(scaler.feature_names_in_))
else:
    print("\nLe scaler ne contient pas le nom des colonnes (les données d'entraînement n'avaient probablement pas d'en-tête textuel).")
print("-----------------------------------\n")
