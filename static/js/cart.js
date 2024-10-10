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
                    // Update cart display dynamically
                    alert(`Added ${data.quantity} of ${data.product} to cart!`);
                    // You can also add code here to update the cart total in the header dynamically
                } else {
                    alert('Error adding product. Please try again.');
                }
            })
            .catch(error => console.error('Error adding to cart:', error));
        });
    });
});
