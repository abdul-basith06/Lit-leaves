

$(document).ready(function (){
    $('.payWithrazorpay').click(function (e){
        e.preventDefault();


         // Fetch values from form elements using name attributes
        var selectedAddressId = $('input[name="selected_address"]:checked').val();
        var orderNotes = $('textarea[name="order_notes"]').val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        // Fetch values from data attributes
        var name = $(this).data('name');
        var email = $(this).data('email');
        var contact = $(this).data('contact');

        
        
        $.ajax({
            method: "GET",
            url: "/shop/proceed_to_pay/",
            success: function (response){
              console.log(response)
              console.log("Ajax response:", response);


              var options = {
            "key": "rzp_test_NxtHpgxEKbJK1k", // Enter the Key ID generated from the Dashboard
            "amount": 1 * 100,  // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "Lit Leaves", //your business name
            "description": "Thank you for shopping from us",
            "image": "https://example.com/your_logo",
       
            "handler": function (responseb){
                alert(responseb.razorpay_payment_id);
               data = {
                'selectedAddressId':selectedAddressId,
                'orderNotes':orderNotes,
                'pay_mod':'RAZ',
                'transaction_id': responseb.razorpay_payment_id,
                // 'razorpay_order_id': responseb.razorpay_order_id,
                // 'razorpay_payment_id': responseb.razorpay_payment_id,
                // 'razorpay_signature': responseb.razorpay_signature,
                csrfmiddlewaretoken:token,
               }
               $.ajax({
                    method : "POST",
                    url: "/shop/place_order_razorpay/",
                    data: data,
                    success: function(responsec) {
                        console.log("Response Object:", responsec);
                        Swal.fire("Congrats!!!", responsec.message, "success").then((value) => {
                            window.location.href = '/shop/orderplaced/';
                        });
                    }
               });
            },
            "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                "name": name, //your customer's name
                "email": email,
                "contact": contact,  //Provide the customer's phone number for better conversion rates 
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        var rzp1 = new Razorpay(options);     
        rzp1.open();
            }
        })

        
    });
});

