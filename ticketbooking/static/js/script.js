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
            let minReturnDate = new Date(this.value);
            minReturnDate.setDate(minReturnDate.getDate() + 1); // Set return date to the day after departure
            return_date.setAttribute('min', minReturnDate.toISOString().split('T')[0]);
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

    // Hàm xử lý disable button Tiếp theo khi chưa chọn vé
    function handle_disable_button(ticket_price_value, return_ticket_price_value) {
        let button_submit_choose_ticket = document.getElementById('button-submit-choose-ticket')

        if(type_ticket == 'one-way') {
            if(ticket_price_value > 0) {
                button_submit_choose_ticket.removeAttribute('disabled')
            }
        }
        else {
            if(ticket_price_value > 0 && return_ticket_price_value > 0) {
                button_submit_choose_ticket.removeAttribute('disabled')
            }
        }
    }

    // JS xử lý hiển thị tiền khi chọn vé
    let ticket_price_item = document.getElementsByClassName("ticket_price_item")
    let ticket_price_return_item = document.getElementsByClassName("ticket_price_return_item")

    let ticket_price = document.getElementById("ticket_price");
    let return_ticket_price = document.getElementById("return_ticket_price");

    let total_price_ticket = document.getElementById("total_price_ticket");

    let ticket_price_value = 0;
    let return_ticket_price_value = 0;

    let ticket_price_input = document.getElementById("ticket_price_input")
    let return_ticket_price_input = document.getElementById("return_ticket_price_input")
    let total_price_ticket_input = document.getElementById("total_price_ticket_input")

    let flight_id = document.getElementById("flight_id")
    let price_id = document.getElementById("price_id")
    let class_id = document.getElementById("class_id")

    let flightReturn_id = document.getElementById("flightReturn_id")
    let priceReturn_id = document.getElementById("priceReturn_id")
    let classReturn_id = document.getElementById("classReturn_id")

    for (let i = 0; i < ticket_price_item.length; i++) {
        ticket_price_item[i].onclick = function displayPrice()
        {
            ticket_price.innerHTML = parseInt(this.getAttribute("data-price")).toLocaleString('en-US');
            ticket_price_value = parseInt(this.getAttribute("data-price"));
            ticket_price_input.value = ticket_price_value
            total_price_ticket.innerHTML = (parseInt(this.getAttribute("data-price")) + return_ticket_price_value).toLocaleString('en-US') + ' VND';
            total_price_ticket_input.value = (parseInt(this.getAttribute("data-price")) + return_ticket_price_value);
            for (let j = 0; j < ticket_price_item.length; j++) {
                ticket_price_item[j].classList.remove('ticket-price-select-active')
            }
            ticket_price_item[i].classList.add('ticket-price-select-active')
            handle_disable_button(ticket_price_value, return_ticket_price_value)

//            JS xử lý lấy thông tin chuyến bay đi được chọn
            flightID = this.getAttribute("data-flightID")
            flight_id.value = flightID
            priceID = this.getAttribute("data-priceID")
            price_id.value = priceID
            classID = this.getAttribute("data-classID")
            class_id.value = classID
        };
    }

    for (let i = 0; i < ticket_price_return_item.length; i++) {
        ticket_price_return_item[i].onclick = function displayPrice()
        {
            return_ticket_price.innerHTML = parseInt(this.getAttribute("data-price")).toLocaleString('en-US');
            return_ticket_price_value = parseInt(this.getAttribute("data-price"))
            return_ticket_price_input.value = return_ticket_price_value
            total_price_ticket.innerHTML = (parseInt(this.getAttribute("data-price")) + ticket_price_value).toLocaleString('en-US') + ' VND';
            total_price_ticket_input.value = (parseInt(this.getAttribute("data-price")) + ticket_price_value);
            for (let j = 0; j < ticket_price_return_item.length; j++) {
                ticket_price_return_item[j].classList.remove('ticket-price-select-active')
            }
            ticket_price_return_item[i].classList.add('ticket-price-select-active')
            handle_disable_button(ticket_price_value, return_ticket_price_value)

//            JS xử lý lấy thông tin chuyến bay về được chọn
            flightReturnID = this.getAttribute("data-flightReturnID")
            flightReturn_id.value = flightReturnID
            priceReturnID = this.getAttribute("data-priceReturnID")
            priceReturn_id.value = priceReturnID
            classReturnID = this.getAttribute("data-classReturnID")
            classReturn_id.value = classReturnID
        };
    }
    // Hủy hóa đơn
    var paymentStatusElement = document.getElementById('paymentStatus');
    if(paymentStatusElement) {
        var paymentStatus = paymentStatusElement.dataset.paymentStatus;

        var confirmCancel = document.getElementById('confirmCancel');
        var cancelButton = document.getElementById('cancelButton');

        if (confirmCancel && paymentStatus === "Cancelled") {
            cancelButton.classList.add('disabled-button'); // Thêm lớp CSS để vô hiệu hóa nút
        }
    }

    // Nếu không phải trạng thái "cancelled", thì thực hiện các hành động khi nhấp vào nút hủy
    if (confirmCancel && paymentStatus !== "Cancelled") {
        confirmCancel.addEventListener('click', function() {
            var invoiceId = cancelButton.getAttribute('data-id');

            // Chuyển hướng đến trang /cancel-invoice/.. nếu hủy hóa đơn thành công
            window.location.href = `/cancel-invoice/${invoiceId}`;
        });
    }
    // Hủy hóa đơn nhân viên
var paymentStatusElement_nv = document.getElementById('paymentStatus_nv');
if(paymentStatusElement_nv) {
    var paymentStatus_nv = paymentStatusElement_nv.dataset.paymentStatus_nv;

    var confirmCancel_nv = document.getElementById('confirmCancel_nv');
    var cancelButton_nv = document.getElementById('cancelButton_nv');

    if (confirmCancel_nv && paymentStatus_nv === "Cancelled") {
        cancelButton_nv.classList.add('disabled-button'); // Thêm lớp CSS để vô hiệu hóa nút
    }
}

// Nếu không phải trạng thái "cancelled", thì thực hiện các hành động khi nhấp vào nút hủy
if (confirmCancel_nv && paymentStatus_nv !== "Cancelled") {
    confirmCancel_nv.addEventListener('click', function() {
        var invoiceId_nv = cancelButton_nv.getAttribute('data-id');

        // Chuyển hướng đến trang /employee/cancel-invoice/.. nếu hủy hóa đơn thành công
        window.location.href = `/employee/cancel-invoice/${invoiceId_nv}`;
    });
}

    // JS hiện form popup thông báo Thanh toán đang chờ duyệt
//    if(payment_status == 'success') {
//        var myModal = new bootstrap.Modal(document.getElementById('popupFormModal1'), {
//            keyboard: false
//        });
//        myModal.show();
//    }
    if(payment_status == 'success') {
        alert(payment_status)
    }
    else {
        alert(payment_status)
    }
};