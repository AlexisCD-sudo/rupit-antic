/* 
 *  Projecte desenvolupat per la Diputació de Girona
 *   
 *  Arxiu creat el: 9 d’oct. 2024
 *   
 *  Autor: mmas
 * 
 */

$(document).ready(function () {

    $('#select_autor').select2({
        allowClear: true
    });

    $('#select_municipi').select2({
        allowClear: true
    });
    $('#select_comarca').select2({
        allowClear: true
    });
    $('#select_fons').select2({
        allowClear: true
    });
    $('#select_drets').select2({
        allowClear: true
    });
    $('#select_pais').select2({
        allowClear: true
    });
    $('#select_provincia').select2({
        allowClear: true
    });
    
    
});

function resetFiltres() {
    console.log("reset filtres");
    $('#select_autor').val(null).trigger('change');
    $('#select_municipi').val(null).trigger('change');
    $('#select_comarca').val(null).trigger('change');
    $('#select_fons').val(null).trigger('change');
    $('#select_drets').val(null).trigger('change');
    $('#select_pais').val(null).trigger('change');
    $('#select_provincia').val(null).trigger('change');
    $('#text_filtre').val('');
    $('#cercaCodi').val('');
    $('#anyIniciCerca').val('');
    $('#anyFiCerca').val('');
}

