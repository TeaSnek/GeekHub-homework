$(document).ready(function () {
    $(".add_form").submit(function (event) {
        let quantity = $(this).find("input[name='quantity']").val();
        let searsId = $(this).find("button[name='product']").val();
        let csrftoken = $("[name=csrfmiddlewaretoken]").val()
        let body = new Map();
        body.set("action", "update");
        body.set(searsId, quantity);
        
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

$(document).ready(function () {
    $(".remove_form").submit(function (event) {
        let quantity = -Number($(this).find("input[name='quantity']").val());
        let searsId = $(this).find("button[name='product']").val();
        let csrftoken = $("[name=csrfmiddlewaretoken]").val()
        let body = new Map();
        body.set("action", "update");
        body.set(searsId, quantity);
        
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