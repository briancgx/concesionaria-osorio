document.getElementById('loginForm').addEventListener('submit', function(event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Validación simple del formulario
    if (username.trim() === '' || password.trim() === '') {
        event.preventDefault();
        alert('Por favor, completa todos los campos.');
    }
});
