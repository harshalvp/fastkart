$(document).ready(function () {

    $(".remove-btn").click(function (event) {
        event.preventDefault();
        
        var product_Id = $(this).data('id');
        var remove_url= "/wishlist/remove/" + product_Id + '/';
        $.ajax({
            type: "GET",
            url: remove_url,
            
            success: function (data) {
                // Display success message
                showAlert(data.message, "alert-success");
    
                // Update the wishlist count on the page
                $('#header_wishlist_count').html(data.wishlist_count);
    
                // Remove the row from the table
                $(event.target).closest('tr').remove();

                // Check if the wishlist is empty and display a message
                if ($('#wishlist_table tbody tr').length == 0) {
                    $('#wishlist_table').html('<p>Your wishlist is empty.</p>');
                }

            },
            error: function (data) {
                if (data.status == '401') {
                    window.location.href = '/accounts/login/';
                } else {
                    showAlert(data.responseJSON.message, "alert-danger");
                }
            }
        });
    });
    function showAlert(message, alertClass) {
          var alertContainer = $("#alert-container");
          var alertDiv = $("<div>").addClass("alert " + alertClass).text(message);
          alertContainer.append(alertDiv);
  
          // Automatically hide the alert after 5 seconds
          setTimeout(function () {
              alertDiv.remove();
          }, 800);
      }
    
  });