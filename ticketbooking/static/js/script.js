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

    if(confirmPasswordInput) {
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
    }

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
    else if(errorCode == 'account_already_exists' || errorCode == 'create_account_false') {
        var myModal = new bootstrap.Modal(document.getElementById('popupFormModal2'), {
            keyboard: false
        });
        myModal.show();
    }

    // JS disabled những ngày trong quá khứ - datepicker
    var today = new Date();
    var todayStr = today.toISOString().split('T')[0];
    var datePicker = document.getElementById('Date_of_department');

    if(datePicker) {
        datePicker.setAttribute('min', todayStr);

        datePicker.addEventListener('input', function() {
          var selectedDate = new Date(datePicker.value);
          if (selectedDate < today) {
            datePicker.value = todayStr;
          }
        });
    }

    // JS disabled những ngày trong quá khứ & không được chọn ngày về không được nhỏ hơn ngày đi - datepicker
    let departure_date = document.getElementById("departureDate")
    let return_date = document.getElementById("returnDate")
    // Disable past dates in departureDate
    var today = new Date().toISOString().split('T')[0];

    if(departure_date) {
        departure_date.setAttribute('min', today);

        // Disable past dates in returnDate and set min date based on departureDate
        departure_date.addEventListener('change', function() {
            document.getElementById("returnDate").setAttribute('min', this.value);
        });
    }

    // Validate returnDate not before departureDate
    let button_submit = document.getElementById("submitBtn")
    if(button_submit) {
        document.getElementById("submitBtn").addEventListener('click', function() {
            var departureDate = new Date(document.getElementById("departureDate").value);
            var returnDate = new Date(document.getElementById("returnDate").value);
            if (returnDate < departureDate) {
                return false; // Prevent form submission
            }
        });
    }

    // JS xử lý hiển thị tiền khi chọn vé
    let ticket_price_item = document.getElementsByClassName("ticket_price_item")
    let ticket_price_return_item = document.getElementsByClassName("ticket_price_return_item")

    let ticket_price = document.getElementById("ticket_price");
    let return_ticket_price = document.getElementById("return_ticket_price");

    let total_price_ticket = document.getElementById("total_price_ticket");

    let ticket_price_value = 0;
    let return_ticket_price_value = 0;

    for (let i = 0; i < ticket_price_item.length; i++) {
        ticket_price_item[i].onclick = function displayPrice()
        {
            ticket_price.innerHTML = parseInt(this.getAttribute("data-price")).toLocaleString('en-US');
            ticket_price_value = parseInt(this.getAttribute("data-price"));
            total_price_ticket.innerHTML = (parseInt(this.getAttribute("data-price")) + return_ticket_price_value).toLocaleString('en-US') + ' VND';
        };
    }

    for (let i = 0; i < ticket_price_return_item.length; i++) {
        ticket_price_return_item[i].onclick = function displayPrice()
        {
            return_ticket_price.innerHTML = parseInt(this.getAttribute("data-price")).toLocaleString('en-US');
            return_ticket_price_value = parseInt(this.getAttribute("data-price"))
            total_price_ticket.innerHTML = (parseInt(this.getAttribute("data-price")) + ticket_price_value).toLocaleString('en-US') + ' VND';
        };
    }
};