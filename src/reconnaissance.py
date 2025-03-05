import os
from deepface import DeepFace
import pandas as pd

# Définir les chemins
# img_path = "data/test_faces/test3.jpeg"
img_path = "data/test_faces/test11.jpg"
# img_path = "data/test_faces/test4.jpg"
# img_path = "data/test_faces/test2.jpeg"
# img_path = "data/test_faces/test1.jpg"
db_path = "data/known_faces"

# Assurer que le chemin existe
if not os.path.exists(img_path):
    raise FileNotFoundError(f"L'image {img_path} n'a pas été trouvée.")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Le dossier de base de données {db_path} n'a pas été trouvé.")

try:
    # Rechercher les visages similaires
    result = DeepFace.find(
        img_path=img_path,
        db_path=db_path,
        model_name="VGG-Face",  # Modèle à utiliser
        distance_metric="cosine"  # Type de métrique pour la similarité
    )

    # Vérifier si le résultat est une liste de DataFrames
    if isinstance(result, list):
        # Supposons que chaque élément de la liste est un DataFrame
        df = result[0]  # Si plusieurs DataFrames sont retournés, on peut ajuster cela

        # Si le DataFrame est vide, afficher un message clair
        if df.empty:
            print("Aucune similarité trouvée dans la base de données.")
        else:
            # Calcul du pourcentage de similarité en fonction de la distance
            df['similarity_percentage'] = (1 - df['distance']) * 100

            # Exemple de filtrage des résultats si nécessaire (par distance, par exemple)
            threshold = 0.4  # seuil de distance
            similar_faces = df[df['distance'] <= threshold]

            # Vérifier s'il y a des visages similaires
            if similar_faces.empty:
                print(f"Aucune similarité avec une distance <= {threshold} trouvée.")
            else:
                # Afficher les visages similaires avec la similarité en pourcentage
                print(f"Visages similaires avec une distance <= {threshold}:")
                print(similar_faces[['identity', 'similarity_percentage', 'distance']])
    else:
        print("Le résultat n'est pas une liste.")
        # Traiter d'autres types de résultats si nécessaire

except Exception as e:
    print(f"Une erreur s'est produite: {e}")


# import os
# from deepface import DeepFace
# import pandas as pd

# # Définir les chemins
# img_path = "data/test_faces/test3.jpeg"
# # img_path = "data/test_faces/test2.jpeg"
# # img_path = "data/test_faces/test1.jpg"
# db_path = "data/known_faces"
# # Assurer que le chemin existe
# if not os.path.exists(img_path):
#     raise FileNotFoundError(f"L'image {img_path} n'a pas été trouvée.")
# if not os.path.exists(db_path):
#     raise FileNotFoundError(f"Le dossier de base de données {db_path} n'a pas été trouvé.")

# try:
#     # Rechercher les visages similaires
#     result = DeepFace.find(
#         img_path=img_path,
#         db_path=db_path,
#         model_name="VGG-Face",  # Modèle à utiliser
#         distance_metric="cosine"  # Type de métrique pour la similarité
#     )

#     # Afficher le résultat brut pour voir sa structure
#     print("Résultat brut de DeepFace.find():")
#     print(result)

#     # Si le résultat est une liste de DataFrames ou un autre type de données, il faut adapter le traitement
#     if isinstance(result, list):
#         # Supposons que chaque élément de la liste est un DataFrame
#         df = result[0]  # Si plusieurs DataFrames sont retournés, on peut ajuster cela
#         print("DataFrame extrait de la liste:")
#         print(df)

#         # Exemple de filtrage des résultats si nécessaire (par distance, par exemple)
#         threshold = 0.4  # seuil de distance
#         similar_faces = df[df['distance'] <= threshold]
#         print(f"Visages similaires avec une distance <= {threshold}:")
#         print(similar_faces)
#     else:
#         print("Le résultat n'est pas une liste.")
#         # Traiter d'autres types de résultats si nécessaire

# except Exception as e:
#     print(f"Une erreur s'est produite: {e}")
