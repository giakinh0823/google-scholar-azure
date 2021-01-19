"use strict";

function getCookieSaveAddArticle(name) {
  var cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim(); // Does this cookie string begin with the name we want?

      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}

var csrftokenSaveAddArticle = getCookieSaveAddArticle('csrftoken');
$(document).on('click', "#addArticleProfile", function (e) {
  $('#FormAddArticle').submit();
});
$(document).on('submit', '#FormAddArticle', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: 'addArticle/',
    data: $(this).serialize(),
    dataType: 'json',
    success: function success(data, textStatus, jqXHR) {
      $("#FormAddArticle")[0].reset();
      alert("Add Article success");
    }
  });
});