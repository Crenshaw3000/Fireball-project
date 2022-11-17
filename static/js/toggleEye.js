const togglePassword = document.querySelector('#togglePassword');

const password = document.querySelector('#password');
togglePassword.addEventListener('click', () => {

    // Toggle the type attribute using
    // getAttribute() method
    const type = password
        .getAttribute('type') === 'password' ?
        'text' : 'password';
        
    password.setAttribute('type', type);

    // Toggle the eye and bi-eye icon
    if (togglePassword.classList.contains('bi-eye-slash')) {
        togglePassword.classList.remove('bi-eye-slash');
        togglePassword.classList.add('bi-eye');
    }
    else {
        togglePassword.classList.remove('bi-eye');
        togglePassword.classList.add('bi-eye-slash');
    }


})