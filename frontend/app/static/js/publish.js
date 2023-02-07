var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/javascript");
lines = Math.floor((screen.height /2) / editor.renderer.lineHeight)
console.log(editor.renderer.lineHeight)
editor.setOptions({
    maxLines: lines
});

$('#publish').addClass('active')
$('.ui.dropdown').dropdown();

$(document).ready(function() {
    var editor = ace.edit("editor");
    lines = Math.floor((screen.height / 2) / editor.renderer.lineHeight)
    console.log(editor.renderer.lineHeight)
    editor.setOptions({
        minLines: lines,
        maxLines: lines
    });
})

$('.message .close')
.on('click', function() {
    $(this)
    .closest('.message')
    .transition('fade')
    ;
});

$(document).ready(function() {
    $("#publish_form").on('submit', (function(e) {
        e.preventDefault();
        $.ajax({
            url: "/publish",
            type: "post",
            data: {
                title: $('#title').val(),
                cve: $('#cve').val(),
                type: $('#type').val(),
                severity: $('#severity').val(),
                language: $('#language').val(),
                poc: editor.getValue()
            },
            success: function(response) {
                if (response.error) {
                    $("#modal_status").text("Publish failed")
                } else {
                    $("#modal_status").text("Publish successful")
                }
                $("#modal_message").text(response.message)
                $('#publish_modal').modal('show');
            },
        });
        return false;
    }));
});