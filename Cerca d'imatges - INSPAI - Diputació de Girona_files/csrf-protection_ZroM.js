/* 
 *  Projecte desenvolupat per la Diputació de Girona
 *   
 *  Arxiu creat el: 25 de set. 2025
 *   
 *  Autor: mmas
 * 
 */

/**
 * Script per a la protecció contra atacs CSRF (Cross-Site Request Forgery)
 * 
 * Aquest script:
 * 1. Obté el token CSRF de la capçalera HTTP
 * 2. Afegeix el token CSRF a totes les peticions AJAX
 */
$(document).ready(function() {
    // Obtenim el token CSRF de la capçalera HTTP
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    
    // Si no existeix la meta tag, intentem obtenir-lo de la capçalera HTTP
    if (!csrfToken) {
        csrfToken = getCSRFTokenFromHeader();
    }
    
    // Configurem jQuery per afegir el token CSRF a totes les peticions AJAX
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // Només afegim el token CSRF a les peticions que ho requereixen
            if (requiresCSRFToken(settings.type)) {
                xhr.setRequestHeader('X-CSRF-TOKEN', csrfToken);
            }
        }
    });
    
    // Funció per obtenir el token CSRF de la capçalera HTTP
    function getCSRFTokenFromHeader() {
        // Intentem obtenir el token CSRF de la capçalera HTTP
        var csrfToken = '';
        
        // Creem una petició AJAX síncrona per obtenir el token CSRF
        $.ajax({
            url: window.location.href,
            type: 'HEAD',
            async: false,
            success: function(data, textStatus, jqXHR) {
                csrfToken = jqXHR.getResponseHeader('X-CSRF-TOKEN');
            }
        });
        
        return csrfToken;
    }
    
    // Funció per comprovar si una petició requereix token CSRF
    function requiresCSRFToken(method) {
        // Mètodes HTTP que requereixen token CSRF
        var protectedMethods = ['POST', 'PUT', 'DELETE', 'PATCH'];
        
        // Convertim el mètode a majúscules per fer la comparació
        method = method.toUpperCase();
        
        // Comprovem si el mètode requereix token CSRF
        return protectedMethods.indexOf(method) !== -1;
    }
});
