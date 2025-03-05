// Initialisation des éléments HTML
const fileInput = document.getElementById('file-input');
const testButton = document.getElementById('test-button');
const resultDiv = document.getElementById('result');
const imagePreview = document.getElementById('image-preview');
const imageStatus = document.getElementById('image-status');

// Fonction pour gérer le téléchargement de l'image
fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect(event) {
    const file = event.target.files[0];

    if (file) {
        // Afficher l'image choisie dans un élément pour l'aperçu
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;  // Afficher l'aperçu de l'image
            imagePreview.style.display = 'block'; // Afficher l'aperçu

            // Signaler que l'image a été correctement chargée
            imageStatus.textContent = 'Image chargée avec succès!';
            imageStatus.style.color = 'green';

            // Activer le bouton "Tester"
            testButton.disabled = false;
        };
        reader.readAsDataURL(file);
    } else {
        // Si aucune image n'est sélectionnée, afficher un message d'erreur
        imageStatus.textContent = 'Erreur lors du chargement de l\'image.';
        imageStatus.style.color = 'red';

        // Désactiver le bouton "Tester"
        testButton.disabled = true;
    }
}

// Fonction pour tester la reconnaissance faciale avec l'image sélectionnée
testButton.addEventListener('click', function () {
    // Afficher "Test en cours..." pendant le traitement
    resultDiv.textContent = 'Traitement en cours...';
    resultDiv.style.color = 'orange'; // Changer la couleur du texte pour indiquer l'attente

    const formData = new FormData();
    const imageFile = fileInput.files[0];  // Récupérer le fichier sélectionné

    // Si un fichier a été sélectionné
    if (imageFile) {
        formData.append('image', imageFile);  // Ajouter l'image à la requête

        // Envoyer l'image au backend Flask pour la reconnaissance
        fetch('/recognize', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            displayResult(data);
        })
        .catch(error => {
            console.error('Erreur:', error);
            resultDiv.textContent = 'Erreur lors de la reconnaissance.';
            resultDiv.style.color = 'red'; // Afficher l'erreur en rouge
        });
    } else {
        resultDiv.textContent = 'Veuillez sélectionner une image.';
        resultDiv.style.color = 'red'; // Afficher l'erreur en rouge
    }
});

// Fonction pour afficher le résultat de la reconnaissance
function displayResult(data) {
    if (data.match) {
        resultDiv.textContent = `Personne reconnue: ${data.name}`;
        resultDiv.style.color = 'green'; // Affichage du nom en vert pour une bonne reconnaissance
    } else {
        resultDiv.textContent = 'Personne inconnue';
        resultDiv.style.color = 'red'; // Affichage de l'échec en rouge
    }
}
