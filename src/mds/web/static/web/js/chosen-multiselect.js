// Assumes chosen and jQuery have already been imported

$(document).ready(function() {
    $("select[multiple]").chosen();
    $(".chosen-container").css({"min-width": 135});
});