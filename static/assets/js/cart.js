console.log("jhfbjksfb")
var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product; // Use lowercase here
        var action = this.dataset.action;
        console.log("ProductId:", productId, "action:", action);
        updateUserOrder(productId, action); // Pass productId and action as arguments
    });
}

function updateUserOrder(productId, action) {
    console.log('user is logged in... sending data...')

    var url = '/shop/updateitem/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ "productId": productId, "action": action }) // Fix the JSON payload
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}

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



    var animation = bodymovin.loadAnimation({
        container: document.getElementById('animContainer'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: 'https://lottie.host/87abf9d2-a834-4f06-b667-26985786b0ba/0vh9JAhgi8.json' // lottie file path
    })
