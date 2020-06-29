let files;
let image = $('#own_image_detected');
let submit = $('#own_submit');
$('#own_image_uploader').change(function () {
    files = this.files;
});
submit.click(function (event) {
    event.stopPropagation(); // Остановка происходящего
    event.preventDefault();  // Полная остановка происходящего
    submit.html(
        '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>  Loading...'
    );
    submit.prop('disabled', true);

    // Создадим данные формы и добавим в них данные файлов из files
    let data = new FormData();
    $.each(files, function (key, value) {
        data.append(key, value);
    });

    // Отправляем запрос
    $.ajax({
        url: detect_uploaded_url,
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false, // Не обрабатываем файлы (Don't process the files)
        contentType: false, // Так jQuery скажет серверу что это строковой запрос
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (data) {
            submit.html('Submit');
            submit.prop('disabled', false);
            image.css('display', 'block');
            image.attr('src', static_prefix + 'detection_demo/detected_images/' + data['img_name'] + '_detected.png')
        },
    });
});