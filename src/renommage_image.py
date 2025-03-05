import os

# Dossier principal contenant les sous-dossiers des personnes
BASE_KNOWN_FACES_DIR = "data/known_faces/"

# Vérifier si le dossier existe
if not os.path.exists(BASE_KNOWN_FACES_DIR):
    print(f"❌ Erreur : le dossier '{BASE_KNOWN_FACES_DIR}' n'existe pas.")
    exit()

# Récupérer la liste des sous-dossiers (chaque sous-dossier étant un dossier pour une personne)
person_dirs = [f for f in os.listdir(BASE_KNOWN_FACES_DIR) if os.path.isdir(os.path.join(BASE_KNOWN_FACES_DIR, f))]

if not person_dirs:
    print(f"❌ Aucun sous-dossier trouvé dans '{BASE_KNOWN_FACES_DIR}'.")
    exit()

print(f"🔍 {len(person_dirs)} personne(s) trouvée(s) dans '{BASE_KNOWN_FACES_DIR}'.")

# Parcourir tous les sous-dossiers des personnes
for person_dir in person_dirs:
    person_path = os.path.join(BASE_KNOWN_FACES_DIR, person_dir)

    # Récupérer les images de chaque personne dans son dossier
    image_files = [f for f in os.listdir(person_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print(f"⚠️ Aucune image trouvée dans '{person_path}'.")
        continue

    print(f"🔍 {len(image_files)} image(s) trouvée(s) pour '{person_dir}'.")

    # Parcourir toutes les images et les renommer
    for i, image_name in enumerate(image_files, 1):
        image_path = os.path.join(person_path, image_name)

        # Créer le nouveau nom du fichier
        new_name = f"{person_dir}_{i}{os.path.splitext(image_name)[1]}"
        new_path = os.path.join(person_path, new_name)

        # Renommer le fichier
        try:
            os.rename(image_path, new_path)
            print(f"✅ Image renommée : {image_name} -> {new_name}")
        except Exception as e:
            print(f"❌ Erreur lors du renommage de {image_name}: {e}")

print("✅ Renommage terminé.")
