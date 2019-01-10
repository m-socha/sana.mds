// Assumes chosen and jQuery have already been imported

$(document).ready(function() {
    $("select[multiple]").each(function(index,el) {
      var $el = $(el);
      if ($el.children().length === 0) {
          $el.chosen({disable_search: true});
      } else {
          $el.chosen();
      }
    });
});