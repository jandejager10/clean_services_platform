document.addEventListener("DOMContentLoaded", function() {
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const url = this.action;
            const formData = new FormData(this);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartDisplay(data.grand_total, data.product_count);
                    showToast('Product added to cart successfully!');
                } else {
                    console.error('Error adding product to cart');
                    showToast('Error adding product to cart', 'error');
                }
            })
            .catch(error => {
                console.error('Error adding to cart:', error);
                showToast('Error adding product to cart', 'error');
            });
        });
    });
});

function updateCartDisplay(total, count) {
    const cartTotalElement = document.querySelector('#cart-total');
    const cartCountElement = document.querySelector('#cart-count');
    if (cartTotalElement) {
        cartTotalElement.textContent = parseFloat(total).toFixed(2);
    }
    if (cartCountElement) {
        cartCountElement.textContent = count;
    }
}

function showToast(message, type = 'success') {
    alert(message); // something still wrong with toasts
}
