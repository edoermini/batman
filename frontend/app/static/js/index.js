$('#home').addClass('active')
$('.ui.dropdown').dropdown();

function viewCode(poc_id) {
    $('#code-'+poc_id).transition('slide down')
    $("#code-arrow-"+poc_id).toggleClass('flip');
}

function verifyRequest(poc_id) {
    $.ajax({
        url: "/verify",
        type: "post",
        data: {
            pocid: poc_id,
        },
        success: function(response) {
            if (response.error) {
                $("#modal_status").text("Verify failed")
            } else {
                $("#modal_status").text("Verify successful")
                $("#verify_btn_"+poc_id).addClass('disabled')
            }
            $("#modal_message").text(response.message)
            $('#verify_modal').modal('show');
        },
    });
    return true;
}

function show_donate_modal(recipient) {
    $('#recipient').text(recipient)
    $('#donate_modal').modal('show')
}

function donate(amount) {
    $.ajax({
        url: "/donate",
        type: "post",
        data: {
            amount: amount,
            recipient: $("#recipient").text()
        },
        success: function(response) {
            if (response.error) {
                $("#donate_result_status").text("Donation failed")
            } else {
                $("#donate_result_status").text("Donation successful")
            }
            $("#donate_result_message").text(response.message)
            $('#donate_result_modal').modal('show');
        },
    });
    return true;
}