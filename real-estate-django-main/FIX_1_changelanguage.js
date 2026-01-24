// DIESE FUNKTION ERSETZT DIE ALTE changelanguage FUNKTION IN templates/include/base.html
// Suche nach "function changelanguage" und ersetze den gesamten Block

// Sprachumschalter - einfache Version die zuverlässig funktioniert
function changelanguage(value) {
    window.location.href = "/set-language/" + value + "/";
}
