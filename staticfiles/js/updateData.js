function getCookieSaveUpdateData(name) {
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
const csrftokenSaveUpdateData = getCookieSaveUpdateData('csrftoken');

$(document).on('click','#updateDataButton', function() {
    alert("Updating")
    $.ajax({
        type: 'GET',
        url: 'updateData/',
        data: '',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            alert("ok")
        },
    })
});

$(document).on('click','#updateArticleButton', function() {
    alert("Updating")
    $.ajax({
        type: 'GET',
        url: 'updateArticle/',
        data: '',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            alert("ok")
        },
    })
});