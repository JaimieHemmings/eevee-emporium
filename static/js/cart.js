// Check if button is pressed to add an item to the cart
$(document).on('click', '#add-cart', function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "cart_add" %}',
        data: {
            'product_id': $('#add_cart').val(),
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            action: 'post',
        },

        success: function(json){
            console.log(json);
        },

        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert(`An error occurred while adding the item to the cart. ${errmsg} - ${err}`);
        }
    })
})