

$(document).ready(function () {
    $("#uploadButton").click(function () {
        var fd = new FormData();
        var files = $('#formFile')[0].files;
        if (files.length > 0) {
            var ext = $('#formFile').val().split('.').pop().toLowerCase();
            if($.inArray(ext, ['jpg']) == -1) {
                alert('invalid extension!');
            }
            else{
                fd.append('file', files[0]);
                $.ajax({
                    url: 'upload/',
                    type: 'post',
                    dataType: 'json',
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response != 0) {
                            $("#imageCanvas").attr("src", "/media/" + response["route"]);
                        }
                    },
                });
            }
        } else {
            alert("Please select a file.");
        }
    })
});