console.log(' kingeeee')


$(document).ready(function (){
    $('.payWithrazorpay').click(function (e){
        e.preventDefault();


         // Fetch values from form elements using name attributes
        var selectedAddressId = $('input[name="selected_address"]:checked').val();
        var orderNotes = $('textarea[name="order_notes"]').val();
        
        $.ajax({
            method: "GET",
            url: "/shop/proceed_to_pay/",
            success: function (response){
              console.log(response)
              console.log("Ajax response:", response);

              var options = {
            "key": "rzp_test_DaGwLRf1QVh5kA", // Enter the Key ID generated from the Dashboard
            "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "Lit Leaves", //your business name
            "description": "Thank you for shopping from us",
            "image": "https://example.com/your_logo",
        //    "order_id": "order_9A33XWu170gUtm",
            "handler": function (response){
                alert(response.razorpay_payment_id);
               
            },
            "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                "name": "Gaurav Kumar", //your customer's name
                "email": "gaurav.kumar@example.com", 
                "contact": "9000090000"  //Provide the customer's phone number for better conversion rates 
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

// $(document).ready(function (){
//     $('.payWithrazorpay').click(function (e){
//         e.preventDefault();


//          // Fetch values from form elements using name attributes
//         var selectedAddressId = $('input[name="selected_address"]:checked').val();
//         var orderNotes = $('textarea[name="order_notes"]').val();
        
//         $.ajax({
//             method: "GET",
//             url: "/shop/proceed_to_pay/",
//             success: function (response){
//               console.log(response)
//               console.log("Ajax response:", response);

//               var options = {
//             "key": "rzp_test_DaGwLRf1QVh5kA", // Enter the Key ID generated from the Dashboard
//             "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//             "currency": "INR",
//             "name": "Lit Leaves", //your business name
//             "description": "Thank you for shopping from us",
//             // "image": "{% static 'assets/images/romance/litleaves2.png' %}",
//             // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//             "handler": function (response){
//                 alert(response.razorpay_payment_id);
//                 alert(response.razorpay_order_id);
//                 alert(response.razorpay_signature)
//             },
//             "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
//                 "name": "Gaurav Kumar", //your customer's name
//                 "email": "gaurav.kumar@example.com", 
//                 "contact": "9000090000"  //Provide the customer's phone number for better conversion rates 
//             },
//             "theme": {
//                 "color": "#3399cc"
//             }
//         };
//         var rzp1 = new Razorpay(options);     
//         rzp1.open();
//             }
//         })

        
//     });
// });


// rzp1.on('payment.failed', function (response){
//     alert(response.error.code);
//     alert(response.error.description);
//     alert(response.error.source);
//     alert(response.error.step);
//     alert(response.error.reason);
//     alert(response.error.metadata.order_id);
//     alert(response.error.metadata.payment_id);
// });