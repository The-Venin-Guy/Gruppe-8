const toggleBtn = document.getElementById('toggle-visibility');
const amountDisplay = document.getElementById('networth-amount');
const eyeIcon = document.getElementById('eye-icon');

let isHidden = false;

toggleBtn.addEventListener('click', () => {
    isHidden = !isHidden;

    if (isHidden) {
        // Change text to stars
        amountDisplay.textContent = "****";
        // Change eye icon to "eye-slash" (Requires Bootstrap Icons or FontAwesome)
        eyeIcon.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        // Restore original value from the data-value attribute
        amountDisplay.textContent = amountDisplay.getAttribute('data-value');
        // Change icon back
        eyeIcon.classList.replace('bi-eye-slash', 'bi-eye');
    }
});