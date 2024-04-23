$(document).ready(function () {
    $('.btn-action-wishlist').click(function (e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        var button = $(this);

        $.ajax({
            type: 'GET',
            url: '/shop/wishlist/add/?product_id=' + productId,
            dataType: 'json',

            success: function (data) {    
                // Update wishlist count
                $('#header_wishlist_count').text(data.wishlist_count);
            },
            error: function (data) {
                if (data.status == '401') {window.location.href = '/accounts/login/';
                }else{showAlert(data.responseJSON.message, "alert-danger");}
            }
        });
    });
});