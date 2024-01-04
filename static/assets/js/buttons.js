
document.addEventListener("DOMContentLoaded", function() {
    const login = document.getElementById("login_in");

    if (login) {
        login.addEventListener("click", function () {
            window.location.href = "/login/";
        });
    }

    const registration = document.getElementById("registration_in");

    if (registration) {
        registration.addEventListener("click", function () {
            window.location.href = "/registration/";
        });
    }
});
