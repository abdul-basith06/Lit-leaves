

$(function() {
    $("#q").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/search_suggestions/',
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2,  // Minimum characters before triggering autocomplete
        select: function(event, ui) {
            if (ui.item.url) {
                // Redirect to the selected product's description page
                window.location.href = ui.item.url;
            }
        },
        // Custom rendering of each item in the dropdown
        renderItem: function(ul, item) {
            var listItem = $("<li>")
                .append("<div class='autocomplete-item'>" + item.label + "<span class='clickable-symbol'>&#9658;</span></div>")
                .appendTo(ul);

            // Add hover effect
            listItem.hover(
                function() {
                    $(this).addClass('autocomplete-item-hover');
                },
                function() {
                    $(this).removeClass('autocomplete-item-hover');
                }
            );

            return listItem;
        }
    });
});
