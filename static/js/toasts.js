// Toast notification handler
class ToastHandler {
    constructor() {
        this.toastContainer = document.querySelector('.toast-container');
        if (!this.toastContainer) {
            this.createToastContainer();
        }
    }

    createToastContainer() {
        this.toastContainer = document.createElement('div');
        this.toastContainer.className = 'toast-container';
        document.body.appendChild(this.toastContainer);
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} show`;
        toast.innerHTML = `
            <div class="toast-header">
                <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        this.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, duration);

        toast.querySelector('.btn-close').addEventListener('click', () => {
            toast.remove();
        });
    }
}

// Initialize toast handler
const toast = new ToastHandler();

// Example usage:
// toast.show('Operation successful!', 'success');
// toast.show('An error occurred!', 'error');
// toast.show('Please wait...', 'info'); 