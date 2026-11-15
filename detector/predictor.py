import os
import joblib

from django.conf import settings

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "logistic_model.pkl"
)

SCALER_PATH = os.path.join(
    settings.BASE_DIR,
    "scaler.pkl"
)

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)