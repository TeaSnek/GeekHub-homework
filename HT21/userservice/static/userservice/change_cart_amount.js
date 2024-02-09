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
        }).done(function(response){
            response['new_amounts'].forEach(element => {
                let product = element['product'];
                let new_amount = element['amount'];
                let product_quantity_field = $("td[class='"+product+"_quantity']");
                product_quantity_field.text(new_amount);
            });
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
        }).done(function(response){
            response['new_amounts'].forEach(element => {
                let product = element['product'];
                let new_amount = element['amount'];
                if (new_amount == 0){
                    $("tr[class='"+product+"_row']").remove()
                }
                let product_quantity_field = $("td[class='"+product+"_quantity']");
                product_quantity_field.text(new_amount);
                checkEmptyTable()
            })
        });
        event.preventDefault();
    });
});

function checkEmptyTable() {
    let table = $("table")[0];
    console.log(table.rows.length)
    if (table.rows.length - 2 == 0){
        emptyCartHeader = document.createElement("h3");
        emptyCartHeader.innerText = "Cart is Empty"
        table.replaceWith(emptyCartHeader);
    }
}