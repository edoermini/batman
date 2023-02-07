function mint(amount) {
    $.ajax({
        url: "/mint",
        type: "post",
        data: {
            amount: amount,
        },
        success: function(response) {
            if (response.error) {
                $("#balance_modal_status").text("Purchase failed")
            } else {
                $("#balance_modal_status").text("Purchase successful")
            }
            $("#balance_modal_message").text(response.message)
            $('#balance_message_modal').modal('show');
        },
    });
    return true;
}