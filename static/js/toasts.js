document.addEventListener('DOMContentLoaded', (event) => {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: false
        })
    })
    toastList.forEach(toast => toast.show())
});