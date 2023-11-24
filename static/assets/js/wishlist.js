$(document).ready(function() {
    $('.btn-wishlist').on('click', function(e) {
        e.preventDefault();
        console.log('Script loaded successfully');


        var productId = $(this).data('product-id');

        $.ajax({
            type: 'GET',
            url: '/user_profile/add_to_wishlist/' + productId + '/',
            success: function(response) {
                console.log('Product added to wishlist successfully');
            },
            error: function(xhr, status, error) {
                console.error('Error adding product to wishlist:', error);

                // Log more details about the error
                console.log('XHR:', xhr);
                console.log('Status:', status);
            }
        });
    });
});