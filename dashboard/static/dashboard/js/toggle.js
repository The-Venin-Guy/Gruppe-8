const toggleBtn = document.getElementById('toggle-visibility');
const eyeIcon = document.getElementById('eye-icon');

const sensitiveValues = document.querySelectorAll('.sensitive-value');

let isHidden = true;

toggleBtn.addEventListener('click', () => {

    isHidden = !isHidden;

    sensitiveValues.forEach((element) => {

        if (isHidden) {
            element.textContent = "****";
        } else {
            element.textContent = element.dataset.value;
        }

    });

    if (isHidden) {
        eyeIcon.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        eyeIcon.classList.replace('bi-eye-slash', 'bi-eye');
    }

});