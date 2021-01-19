function getCookieSaveCoauthor(name) {
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
const csrftokenSaveCoauthor = getCookieSaveCoauthor('csrftoken');


// $(document).ready(function() {
//     $('#saveCoauthor').click(function() {
//         checkboxValues = $("input[name='coAuthor']:checked").map(function() {
//             return $(this).val();
//         }).get();
//         $.ajax({
//             type: "POST",
//             url: "",
//             data: {
//                 "coAuthorList": checkboxValues,
//                 "csrfmiddlewaretoken": csrftokenSaveCoauthor,
//             },
//             dataType: 'json',
//             success: function(data, textStatus, jqXHR) {
//                 alert("Save success")
//             },
//         });
//     })
// })


$(document).ready(function() {
    $('.chekboxCoAuthor').click(function() {
        id = $(this).data('id')
        $.ajax({
            type: "POST",
            url: "",
            data: {
                "id": id,
                "csrfmiddlewaretoken": csrftokenSaveCoauthor,
            },
            dataType: 'html',
            success: function(data, textStatus, jqXHR) {
                $('#listCoAuthorProfile').html(data)
                alert("Add Co-Author Success")
            },
        });
    })
})