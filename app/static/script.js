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
      "scrollY": 600, // Définir une hauteur fixe pour le défilement vertical
      autoWidth: true,
  });


const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

      toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close")
      });
      searchBtn.addEventListener("click", () =>{
        sidebar.classList.remove("close")
      });

      modeSwitch.addEventListener("click", () =>{
        body.classList.toggle("dark");

        if(body.classList.contains("dark")){
            modeText.innerText = "Light Mode"
        }else{
            modeText.innerText = "Dark Mode"
        }
      });