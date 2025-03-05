import pickle

ENCODINGS_FILE = "models/face_encodings.pkl"

with open(ENCODINGS_FILE, "rb") as f:
    data = pickle.load(f)
    print(data)  # Affiche les données chargées
