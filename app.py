import os
import pickle
import re
from flask import Flask, render_template, request, jsonify
from deepface import DeepFace

app = Flask(__name__, static_folder='static', template_folder='templates')

# Charger les encodages existants
ENCODINGS_FILE = "models/face_encodings.pkl"

def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            return pickle.load(f)
    return None

encodings_data = load_encodings()

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# # Route pour la reconnaissance faciale
# @app.route('/recognize', methods=['POST'])
# def recognize_face():
#     if 'image' not in request.files:
#         return jsonify({'error': 'Aucune image téléchargée'}), 400

#     # Obtenir l'image téléchargée
#     image_file = request.files['image']
    
#     # Sauvegarder temporairement l'image
#     temp_image_path = "temp_image.jpg"
#     image_file.save(temp_image_path)
    
#     # Comparer l'image avec les encodages existants
#     try:
#         # Utilisation du modèle VGG-Face pour la comparaison
#         result = DeepFace.find(img_path=temp_image_path, db_path="data/known_faces", model_name="VGG-Face", distance_metric="cosine")
        
#         # Si aucune correspondance n'est trouvée
#         if result and len(result) > 0:
#             best_match = result[0]
#             distance = best_match['distance'][0]
            
#             if distance <= 0.4:  # Si la distance est assez faible
#                 # name = best_match['identity'][0].split('/')[-1].split('.')[0]  # Extraire le nom
#                 file_name = best_match['identity'][0].split('/')[-1].split('.')[0] 
#                 name = re.split(r'[_\d]+$', file_name)[0]  

#                 return jsonify({'match': True, 'name': name})
#             else:
#                 return jsonify({'match': False, 'name': 'Inconnu'})
#         else:
#             return jsonify({'match': False, 'name': 'Inconnu'})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/recognize', methods=['POST'])
def recognize_face():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image téléchargée'}), 400

    # Obtenir l'image téléchargée
    image_file = request.files['image']
    
    # Sauvegarder temporairement l'image
    temp_image_path = "temp_image.jpg"
    image_file.save(temp_image_path)
    
    # Comparer l'image avec les encodages existants
    try:
        # Utilisation du modèle VGG-Face pour la comparaison
        result = DeepFace.find(img_path=temp_image_path, db_path="data/known_faces", model_name="VGG-Face", distance_metric="cosine")
        
        # Si une correspondance est trouvée
        if result and len(result) > 0:
            best_match = result[0]
            distance = best_match['distance'][0]

            # Calcul du pourcentage de confiance
            confidence = round((1 - distance) * 100, 2)  # Arrondi à 2 décimales
            
            if distance <= 0.4:  # Seuil de confiance
                file_name = best_match['identity'][0].split('/')[-1].split('.')[0] 
                name = re.split(r'[_\d]+$', file_name)[0]  

                return jsonify({'match': True, 'name': name, 'confidence': confidence})
            else:
                return jsonify({'match': False, 'name': 'Inconnu', 'confidence': confidence})

        else:
            return jsonify({'match': False, 'name': 'Inconnu', 'confidence': 0})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
