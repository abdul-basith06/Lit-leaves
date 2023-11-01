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

