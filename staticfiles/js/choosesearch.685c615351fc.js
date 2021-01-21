$(document).ready(function() {
    $('#radioArticle').click(function() {
        $('#headerhome').text("Article")
        $('#id_name').attr({ "id": "search", 'name': 'search', })
        if ($('#headerhome').text() == "Article") {
            $('#id_name').attr({ "id": "search", 'name': 'search', })
            $('#homeSearchForm').attr("action", $('#radioArticle').val())
            $('#searchsmall').css("right", "30%")
        }
    })
    $('#radioUser').click(function() {
        $('#search').attr({ "id": "id_name", 'name': 'name', })
        $('#headerhome').text("User")
        if ($('#headerhome').text() == "User") {
            $('#search').attr({ "id": "id_name", 'name': 'name', })
            $('#homeSearchForm').attr("action", $('#radioUser').val())
            $('#searchsmall').css("right", "35%")
        }
    })
})