new DataTable('#example', {
      "lengthMenu": [5, 10, 25, 50, 100], // Choix de nombre d'entrées par page
      "pageLength": 5, // Nombre d'entrées par page par défaut
      "language": {
        "search": "Rechercher : ", // Modifier le texte du champ de recherche
        "decimal":        "",
        "emptyTable":     "Aucune donnée disponible dans le tableau",
        "info":           "Affichage de l'élément _START_ à _END_ sur _TOTAL_ éléments",
        "infoEmpty":      "Affichage de l'élément 0 à 0 sur 0 élément",
        "infoFiltered":   "(filtré à partir de _MAX_ éléments au total)",
        "infoPostFix":    "",
        "thousands":      ",",
        "lengthMenu":     "Afficher _MENU_ éléments",
        "loadingRecords": "Chargement...",
        "processing":     "Traitement...",
        "zeroRecords":    "Aucun enregistrement correspondant trouvé",
        "paginate": {
            "first":      "Premier",
            "last":       "Dernier",
            "next":       "Suivant",
            "previous":   "Précédent"
        },
        "aria": {
            "sortAscending":  ": activer pour trier la colonne par ordre croissant",
            "sortDescending": ": activer pour trier la colonne par ordre décroissant"
        }
      },
      "scrollX": true, // Activer le défilement horizontal
      "scrollY": 500, // Définir une hauteur fixe pour le défilement vertical
      scrollCollapse: true, // Permet de réduire si moins de données
      autoWidth: true,
  });


const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

// Vérifie l'état du mode sombre au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
  const darkMode = localStorage.getItem('darkMode') === 'true';

  if (darkMode) {
      body.classList.add('dark');
      modeText.innerText = "Light Mode";
  } else {
      modeText.innerText = "Dark Mode";
  }
});

// Fonctionnalités des boutons
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

// searchBtn.addEventListener("click", () => {
//   sidebar.classList.remove("close");
// });

modeSwitch.addEventListener("click", () => {
  body.classList.toggle("dark");
  const isDarkMode = body.classList.contains("dark");

  // Met à jour le texte du mode
  modeText.innerText = isDarkMode ? "Light Mode" : "Dark Mode";
  
  // Sauvegarde l'état du mode sombre dans localStorage
  localStorage.setItem('darkMode', isDarkMode);
});


// Script qui désactive le bouton après clic et affiche un indicateur de chargement pour le boutton "submit" de sandbox-form
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    // const submitButton = form.querySelector('input[type="submit"]');
    const submitButton = document.getElementById('submitButton');

    // Fonction pour réinitialiser le bouton
    function resetSubmitButton() {
      submitButton.disabled = false;
      submitButton.value = "Soumettre";
    }

    // Gestion de la soumission du formulaire
    form.addEventListener('submit', function() {
      submitButton.disabled = true;
      submitButton.value = "Traitement...";
    });

    // Réinitialisation du bouton lorsque la page devient visible
    // Il faut s'assurer ici que l'état du bouton est correctement réinitialisé lorsque la page est revisitée sans être rechargée. (page reste enn cache navigateur)
    document.addEventListener('visibilitychange', function() {
      if (document.visibilityState === 'visible') {
          resetSubmitButton();
      }
    });

    // Réinitialiser le bouton au chargement de la page
    resetSubmitButton();
});


// Script pour gérer le bouton "Annoter le fichier"
document.addEventListener("DOMContentLoaded", function() {
  const annotateForm = document.querySelector('form[action="/form/upload"]');
  const annotateButton = document.getElementById('annotateButton');

  // Fonction pour réinitialiser le bouton
  function resetAnnotateButton() {
      annotateButton.disabled = false;
      annotateButton.value = "Annoter le fichier";
  }

  // Gestion de la soumission du formulaire
  annotateForm?.addEventListener('submit', function() {
      annotateButton.disabled = true;
      annotateButton.value = "Traitement...";
  });

  // Réinitialisation du bouton lorsque la page devient visible
  document.addEventListener('visibilitychange', function() {
      if (document.visibilityState === 'visible') {
          resetAnnotateButton();
      }
  });

  // Réinitialiser le bouton au chargement de la page
  resetAnnotateButton();
});

