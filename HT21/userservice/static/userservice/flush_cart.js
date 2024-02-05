$(document).ready(function () {
    $(".flush_form").submit(function (event) {
        let csrftoken = $("[name=csrfmiddlewaretoken]").val()
        let body = new Map();
        body.set("action", "flush");
        
        let dataToSend = Object.fromEntries(body);
        console.log(dataToSend)
        $.ajax({            
            url: '/user/api/cart/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: dataToSend,
            error: function(response) { 
                console.error('Error:', response)
            },
        }).done(function(){
            location.reload();
        });
        event.preventDefault();
    });
});