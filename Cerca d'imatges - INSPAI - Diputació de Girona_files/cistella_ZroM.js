/* 
 *  Projecte desenvolupat per la Diputació de Girona
 *   
 *  Arxiu creat el: 10 de gen. 2025
 *   
 *  Autor: mmas
 * 
 */

/**
 * Afegeix una imatge a la cistella
 * 
 * @param {number} idImatge - ID de la imatge a afegir
 */
function afegeixImatgeCistella(idImatge) {
    $.ajax({
        url: "/afegeix-imatge-cistella/" + idImatge,
        type: "POST",
        data: '{}',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (resposta) {
            if(resposta) {
                // Actualitzem el comptador d'imatges a la cistella
                $("#cistella_petita_contador").text(resposta.numeroImatgesCistella);
                
                // Comprovem si l'operació ha estat correcta
                if (resposta.correcte) {
                    alert("S'ha afegit la imatge a la cistella.");
                } else {
                    // Si hi ha un missatge d'error, el mostrem
                    if (resposta.missatgeError) {
                        alert(resposta.missatgeError);
                    } else {
                        alert("No s'ha pogut afegir la imatge a la cistella.");
                    }
                }
            }
        },
        error: function () {
            alert("S'ha produit un error a l'hora d'afegir la imatge a la cistella.");
        }
    });
}

function eliminaImatgeCistella(idImatge) {
    $.ajax({
        url: "/esborra-imatge-cistella/" + idImatge,
        type: "POST",
        data: '{}',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (resposta) {
            $("#imatge-" + idImatge).remove();
            if(resposta) {
                $("#cistella_petita_contador").text(resposta.numeroImatgesCistella);
            }
            alert("S'ha eliminat correctament la imatge de la cistella.");
        },
        error: function () {
            alert("S'ha produit un error a l'hora d'eliminar la imatge a la cistella.");
        }
    });
}

function descarregaImatgesCistella() {
    $.ajax({
        url: "/descarrega-imatges-cistella",
        type: "POST",
        data: '{}',
        xhrFields: {
            responseType: 'arraybuffer'
        },
        success: function (data) {
            var blob = new Blob([data], { type: 'application/zip' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'images.zip';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            location.reload();
        },
        error: function (e) {
            console.log(e.responseText);
            alert("S'ha produit un error a l'hora de descarregar les imatges.");
        }
    });
}
