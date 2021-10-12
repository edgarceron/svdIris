

$(document).ready(function () {
    $("#uploadButton").click(function () {
        var fd = new FormData();
        var files = $('#formFile')[0].files;
        if (files.length > 0) {
            var ext = $('#formFile').val().split('.').pop().toLowerCase();
            if($.inArray(ext, ['bmp']) == -1) {
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
                            min = response["min"]
                            if(min < 5){
                                person = response['person'],
                                eye = response['eye']
                                alert("Corresponde con el ojo " + eye + " de la persona: " + person)
                            }
                            else {
                                alert("Iris no corresponde a ningun usuario")
                            }
                        }
                    },
                });
            }
        } else {
            alert("Seleccione un archivo.");
        }
    })
});