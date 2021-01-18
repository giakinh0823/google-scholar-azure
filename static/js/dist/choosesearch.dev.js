"use strict";

$(document).ready(function () {
  $('#radioArticle').click(function () {
    $('#headerhome').text("Article");
    $('#id_name').attr({
      "id": "id_title",
      'name': 'title'
    });

    if ($('#headerhome').text() == "Article") {
      $('#id_name').attr({
        "id": "id_title",
        'name': 'title'
      });
      $('#homeSearchForm').attr("action", $('#radioArticle').val());
      $('#searchsmall').css("right", "30%");
    }
  });
  $('#radioUser').click(function () {
    $('#id_title').attr({
      "id": "id_name",
      'name': 'name'
    });
    $('#headerhome').text("User");

    if ($('#headerhome').text() == "User") {
      $('#id_title').attr({
        "id": "id_name",
        'name': 'name'
      });
      $('#homeSearchForm').attr("action", $('#radioUser').val());
      $('#searchsmall').css("right", "35%");
    }
  });
});