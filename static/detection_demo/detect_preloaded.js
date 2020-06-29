$(".img-invoker").button().click(function sendJSON() {
    let this_button = $(this);
    this_button.prop('disabled', true);
    let old_value = this_button.html();
    this_button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');

    let active_img = $("div.active").children('img');
    let img_name = active_img.attr('id');
    let image = $("#" + img_name);

    $.ajax({
        url: detect_preloaded_url,
        type: 'POST',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            img_name: img_name
        }),
        success: function () {
            image.attr('src', static_prefix + 'detection_demo/detected_images/' + img_name + '_detected.png');
            this_button.html(old_value);
            this_button.prop('disabled', false);
        },
    });
});