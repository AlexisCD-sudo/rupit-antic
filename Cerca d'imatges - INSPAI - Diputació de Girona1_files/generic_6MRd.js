/* 
 *  Projecte desenvolupat per la Diputació de Girona
 *   
 *  Arxiu creat el: 12 de des. 2024
 *   
 *  Autor: mmas
 * 
 */

function compartirURL(event) {
    event.preventDefault(); // Impedeix l'enllaç de fer la seva acció per defecte

    var tempInput = document.createElement("input");
    tempInput.value = window.location.href; // Agafa la URL actual
    document.body.appendChild(tempInput);
    tempInput.select(); // Selecciona el text dins de l'input
    document.execCommand("copy"); // Copia el text al porta-retalls
    document.body.removeChild(tempInput);

    // Opcional: mostrar un missatge confirmant que la URL ha estat copiada
    alert("S'ha copiat l'enllaç correctament.");
} 