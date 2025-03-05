import os
import pickle
from deepface import DeepFace

# Dossier principal contenant les sous-dossiers de chaque personne
BASE_KNOWN_FACES_DIR = "data/known_faces/"
ENCODINGS_FILE = "models/face_encodings1.pkl"

# Vérifier si le dossier principal existe
if not os.path.exists(BASE_KNOWN_FACES_DIR):
    print(f"❌ Erreur : le dossier '{BASE_KNOWN_FACES_DIR}' n'existe pas.")
    exit()

# Récupérer la liste des sous-dossiers (chaque sous-dossier étant un dossier pour une personne)
person_dirs = [f for f in os.listdir(BASE_KNOWN_FACES_DIR) if os.path.isdir(os.path.join(BASE_KNOWN_FACES_DIR, f))]

if not person_dirs:
    print(f"❌ Aucun sous-dossier trouvé dans '{BASE_KNOWN_FACES_DIR}'.")
    exit()

print(f"🔍 {len(person_dirs)} personne(s) trouvée(s) dans '{BASE_KNOWN_FACES_DIR}'.")

known_encodings = []
known_names = []

# Parcourir tous les sous-dossiers des personnes
for person_dir in person_dirs:
    person_path = os.path.join(BASE_KNOWN_FACES_DIR, person_dir)

    # Récupérer les images de chaque personne dans son dossier
    image_files = [f for f in os.listdir(person_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print(f"⚠️ Aucune image trouvée dans '{person_path}'.")
        continue

    print(f"🔍 {len(image_files)} image(s) trouvée(s) pour '{person_dir}'.")

    # Parcourir toutes les images de la personne et extraire les encodages
    for image_name in image_files:
        image_path = os.path.join(person_path, image_name)

        try:
            # Extraire l'encodage facial
            embedding = DeepFace.represent(img_path=image_path, model_name="Facenet")

            if embedding:  # Vérifier si un encodage a été trouvé
                known_encodings.append(embedding[0]["embedding"])
                known_names.append(person_dir)  # Utiliser le nom du dossier comme nom de la personne

                print(f"✅ Encodage réussi pour : {image_name} ({person_dir})")
            else:
                print(f"⚠️ Aucun visage détecté dans {image_name}.")
        
        except Exception as e:
            print(f"❌ Erreur sur {image_name} de {person_dir}: {e}")

# Vérifier si des encodages ont été obtenus avant de sauvegarder
if known_encodings:
    # Sauvegarde des encodages
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)

    print("✅ Entraînement terminé. Encodages enregistrés !")
else:
    print("❌ Aucun encodage enregistré. Vérifie les images d'entrée.")


# import os
# import pickle
# from deepface import DeepFace

# # Dossier des images d'entraînement
# KNOWN_FACES_DIR = "data/known_faces/wendtoin/"
# ENCODINGS_FILE = "models/face_encodings.pkl"

# # Vérifier si le dossier existe
# if not os.path.exists(KNOWN_FACES_DIR):
#     print(f"❌ Erreur : le dossier '{KNOWN_FACES_DIR}' n'existe pas.")
#     exit()

# # Récupérer la liste des images
# image_files = [f for f in os.listdir(KNOWN_FACES_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]

# if not image_files:
#     print(f"❌ Aucune image trouvée dans '{KNOWN_FACES_DIR}'.")
#     exit()

# print(f"🔍 {len(image_files)} image(s) détectée(s) dans '{KNOWN_FACES_DIR}'.")

# known_encodings = []
# known_names = []

# # Parcourir toutes les images et extraire les encodages
# for image_name in image_files:
#     image_path = os.path.join(KNOWN_FACES_DIR, image_name)
    
#     try:
#         # Extraire l'encodage facial
#         embedding = DeepFace.represent(img_path=image_path, model_name="Facenet")

#         if embedding:  # Vérifier si un encodage a été trouvé
#             known_encodings.append(embedding[0]["embedding"])
#             known_names.append(image_name.split('.')[0])  # Utiliser le nom du fichier

#             print(f"✅ Encodage réussi pour : {image_name}")
#         else:
#             print(f"⚠️ Aucun visage détecté dans {image_name}.")
    
#     except Exception as e:
#         print(f"❌ Erreur sur {image_name}: {e}")

# # Vérifier si des encodages ont été obtenus avant de sauvegarder
# if known_encodings:
#     # Sauvegarde des encodages
#     with open(ENCODINGS_FILE, "wb") as f:
#         pickle.dump({"encodings": known_encodings, "names": known_names}, f)

#     print("✅ Entraînement terminé. Encodages enregistrés !")
# else:
#     print("❌ Aucun encodage enregistré. Vérifie les images d'entrée.")
