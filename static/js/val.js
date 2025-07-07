function checkPasswordMatch() {
    var mot_de_passe = document.getElementById("mot_de_passe").value;
    var mot_de_passe_confirmation = document.getElementById("mot_de_passe_confirmation").value;
  
    if (mot_de_passe !== mot_de_passe_confirmation) {
      document.getElementById("mot_de_passe_erreur").innerHTML = "Les mots de passe ne correspondent pas.";
    } else {
      document.getElementById("mot_de_passe_erreur").innerHTML = "";
    }
  }