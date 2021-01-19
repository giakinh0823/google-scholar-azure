function getCookieCoauthor(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftokenCoauthor = getCookieCoauthor('csrftoken');


$(function() {
    $('.inputSearchForm').keyup(function() {
        $.ajax({
            type: "GET",
            url: "searchCoauthor/",
            data: {
                'search_text': $('.inputSearchForm').val(),
                'csrfmiddlewaretoken': csrftokenCoauthor
            },
            dataType: 'html',
            success: function(data, textStatus, jqXHR) {
                $('#searchCoauthor_results').html(data)
            },
        });
    });
});


$(function() {
    $('#buttonSearchCoAuthor').click(function() {
        $.ajax({
            type: "GET",
            url: "searchCoauthor/",
            data: {
                'search_text': $('.inputSearchForm').val(),
                'csrfmiddlewaretoken': csrftokenCoauthor
            },
            dataType: 'html',
            success: function(data, textStatus, jqXHR) {
                $('#searchCoauthor_results').html(data)
            },
        });
    });
});

$(function() {
    $('.inputSearchForm').bind('enterKey', function(e) {
        $.ajax({
            type: "GET",
            url: "searchCoauthor/",
            data: {
                'search_text': $('.inputSearchForm').val(),
                'csrfmiddlewaretoken': csrftokenCoauthor
            },
            dataType: 'html',
            success: function(data, textStatus, jqXHR) {
                $('#searchCoauthor_results').html(data)
            },
        });
    });
    $('.inputSearchForm').keyup(function(e) {
        if (e.keyCode == 13) {
            $(this).trigger("enterKey");
        }
    });
});