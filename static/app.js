$('form input[type="file"]').change(event => {
    let fileTarget = event.target.files;
    if (fileTarget.length === 0) {
        console.log('No image to show')
    } else {
        if (fileTarget[0].type == 'image/jpeg') {
            $('img').remove();
            let image = $('<img class="img-fluid">')
            image.attr('src', window.URL.createObjectURL(fileTarget[0]))
            $('figure').prepend(image)
        } else {
            let msg = 'Not supported file type'
            console.log(msg)
            alert(msg)
        }
    }
});
