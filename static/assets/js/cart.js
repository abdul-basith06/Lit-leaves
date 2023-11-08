
// var url = '/shop/updateitem/';



var removeButtons = document.getElementsByClassName('btn-remove');

for (var i = 0; i < removeButtons.length; i++) {
    removeButtons[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        clearCartItem(productId);
    });
}

function clearCartItem(productId) {
    var url = '/shop/clearitem/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ "productId": productId })
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('data:', data);
            location.reload(); // Reload the cart page to reflect the updated cart
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


