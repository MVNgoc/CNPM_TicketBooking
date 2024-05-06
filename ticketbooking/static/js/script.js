window.onload = function() {
    // JS animation của button Đăng nhập và Đăng ký
    let collapseButton = document.getElementById('collapseButton');
    let flightInfo = document.getElementById('flightInfo');
    let iconUp = document.getElementById('iconUp')
    let iconDown = document.getElementById('iconDown')
    if(collapseButton) {
        collapseButton.addEventListener('click', () => {
            if(flightInfo.classList.contains('animation_hidden')) {
                flightInfo.classList.remove('animation_hidden')
                flightInfo.classList.add('animation_show')
                if(iconDown.classList.contains('hidden')) {
                    iconDown.classList.remove('hidden')
                    iconUp.classList.add('hidden')
                }
            } else {
                flightInfo.classList.add('animation_hidden');
                flightInfo.classList.remove('animation_show');
                if(iconUp.classList.contains('hidden')) {
                    iconUp.classList.remove('hidden')
                    iconDown.classList.add('hidden')
                }
            }
        });
    }

    //    JS kiểm tra mật khẩu trùng khớp tại form đăng ký
    var passwordInput = document.getElementById('passwordInput');
    var confirmPasswordInput = document.getElementById('confirmPasswordInput');
    var passwordHelpBlock = document.getElementById('passwordHelpBlock');
    var submitButton = document.getElementById('submitButton');

    confirmPasswordInput.addEventListener('input', function() {
        if (passwordInput.value === confirmPasswordInput.value) {
            passwordHelpBlock.textContent = 'Mật khẩu trùng khớp';
            passwordHelpBlock.classList.remove('text-danger');
            passwordHelpBlock.classList.add('text-success');
            submitButton.removeAttribute('disabled');
        } else {
            passwordHelpBlock.textContent = 'Mật khẩu không trùng khớp';
            passwordHelpBlock.classList.remove('text-success');
            passwordHelpBlock.classList.add('text-danger');
                submitButton.setAttribute('disabled', 'disabled');
        }
    });

    let register_form = document.getElementById('registerForm')
    if(register_form) {
        // Lắng nghe sự kiện khi form được submit
        document.getElementById('registerForm').addEventListener('submit', function(event) {
        // Ngăn chặn hành vi mặc định của form (tải lại trang)
        event.preventDefault();
        alert('Đăng ký thành công!');
        });
    }

    // JS hiện form login khi đăng nhập thất bại
    if(errorCode == 'login_failed') {
        var myModal = new bootstrap.Modal(document.getElementById('popupFormModal1'), {
            keyboard: false
        });
        myModal.show();
    }
};