$(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'))
        }
    });

    // 用户登陆操作
    $('#Sign-in').click(function () {

        var $username = $('#username');
        $username.css({border: '1px solid #ccc'}).next('p').text('');
        var $password = $('#password');
        $password.css({border: '1px solid #ccc'}).next('p').text('');
        var username = $username.val();
        var password = $password.val();
        var remember_me = $('#remember-me').prop('checked');


        if (!username) {
            $username.css({border: '1px solid red'}).next('p').text('用户名不能为空');
        }

        if (!password) {
            $password.css({border: '1px solid red'}).next('p').text('密码不能为空');
            return
        }

        $.ajax({
            url: '/login/',
            type: 'POST',
            data: {'username': username, 'password': password, 'remember_me': remember_me},
            success: function (data) {
                data = JSON.parse(data);
                if (data['user']) {
                    location.href = '/';
                } else {
                    $('.error-msg').text(data['error'])

                }

            }
        })

    });

    // 用户注册操作
    $('#sign-up').click(function () {


        var username = $('#id_username').val();
        var password = $('#id_password').val();
        var rePassword = $('#id_rePassword').val();
        var email = $('#id_email').val();
        var phone = $('#id_phone').val();
        var captcha = $('#id_captcha').val();

        var formdata = new FormData();
        formdata.append('username', username);
        formdata.append('password', password);
        formdata.append('rePassword', rePassword);
        formdata.append('email', email);
        formdata.append('phone', phone);
        formdata.append('captcha', captcha);


        $.ajax({
            url: '/register/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formdata,
            success: function (data) {
                // data = JSON.parse(data)
                console.log(data['status'], typeof data['status']);
                if (data['status']) {
                    location.href = '/login/'

                } else {
                    $('p').text('');

                    $.each(data['errors'], function (key, value) {
                        $('#id_' + key).nextAll('.error-msg').first().text(value);
                        if (key === '__all__') {
                            $('#id_rePassword').nextAll('.error-msg').first().text(value);
                        }
                    })

                }

            }

        })

    });

    // 更新验证码
    $('#captcha-img').click(function () {
        $('#captcha-img')[0].src += '?';
    });

    // 上传预览头像
    $('#avatar-choice').change(function () {
        var reader = new FileReader();
        var file_object = $('#avatar-choice')[0].files[0];
        reader.readAsDataURL(file_object);
        reader.onload=function (ev) {
            $('#avatar-img')[0].src = this.result;
        }

    });

    //保存个人信息到后端
    $('#save-info').click(function () {
        var file_object = $('#avatar-choice')[0].files[0];

        var username = $.cookie('username');
        console.log(username)
    })
});