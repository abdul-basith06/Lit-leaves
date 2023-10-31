// add to cart functionality

$("#add-to-cart-btn").on("click", function(){
    let quantity = $("#product-quantity").val();
    let product_title = $("#product-title").text();  // Use .text() for non-input elements
    let product_id = $(".product-id").val();  // Use .text() for non-input elements
    let product_price = $("#product-price").text();  
    let this_val = $(this)

     console.log("Quantity:",quantity);
     console.log("Product:",product_title);
     console.log("ID:",product_id);
     console.log("Price:",product_price);
     console.log("This:",this_val);

     $.ajax({
        // type: "POST",
        url: "/add-to-cart",  // Replace with the correct URL for your Django view
        data: {
            'id': product_id,
            'qty': quantity,
            'title': product_title,
            'price': product_price
        },
        dataType: 'json',
        beforeSend: function(){
           console.log("Adding product to cart...")
        },
        success: function(response) {
            this_val.html ("Item added to cart")
            console.log("Added product to cart!!!")
        }
    });

})