$(document).ready(function() {
    $('.add_to_cart_btn').click(function(e) {
        e.preventDefault()

        let searsId = $(this).data('searsid')
        let quantity = 1
        let csrftoken = $("[name=csrfmiddlewaretoken]").val()
        let body = new Map();
        body.set("action", "add");
        body.set(searsId, quantity);
        
        let dataToSend = Object.fromEntries(body);
        $.ajax({
            url: 'user/api/cart/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: dataToSend,
            error: function(response) { 
                console.error('Error:', response)
            }
        }).done(
            console.log('Yes')
        )
    })
})