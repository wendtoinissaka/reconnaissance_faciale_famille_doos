import os
import cv2

# Dossier contenant les images de la personne
KNOWN_FACES_DIR = "data/known_faces/wendtoin"

def verifier_et_renommer_images(directory):
    """ Vérifie si chaque image contient un visage et la renomme """
    if not os.path.exists(directory):
        print(f"Le dossier {directory} n'existe pas.")
        return
    
    files = os.listdir(directory)
    i = 1
    
    for filename in files:
        file_path = os.path.join(directory, filename)
        image = cv2.imread(file_path)
        
        if image is None:
            print(f"❌ Impossible de lire l'image {filename}.")
            continue
        
        # Détecter les visages
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) > 0:
            new_name = f"face_{i}.jpg"
            new_path = os.path.join(directory, new_name)
            os.rename(file_path, new_path)
            print(f"✅ {filename} → {new_name}")
            i += 1
        else:
            print(f"❌ Aucun visage détecté dans {filename}, image ignorée.")

# Exécution
verifier_et_renommer_images(KNOWN_FACES_DIR)
