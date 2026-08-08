/* 
 *  Projecte desenvolupat per la Diputació de Girona
 *   
 *  Arxiu creat el: 13 de set. 2024
 *   
 *  Autor: mmas
 * 
 */

$(document).ready(function () {
    $("#form-contacte").submit(function (event) {

        var form = $("#form-contacte")[0];
        var formData = convertFormToJSON(form);
        console.log("form data", formData);

        $.ajax({
            url: "/registre-contacte",
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function () {
                alert("Missatge enviat: En breu ens posarem en contacte amb vosaltres.");
            },
            error: function () {
                alert("S'ha produit un error a l'hora de contactar amb nosaltres.");
            }
        });

        event.preventDefault();


    });
});

function convertFormToJSON(form) {
    const array = $(form).serializeArray(); // Encodes the set of form elements as an array of names and values.
    const json = {};
    $.each(array, function () {
        json[this.name] = this.value || "";
    });
    return json;
}