document.addEventListener("DOMContentLoaded", function () {

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


    const submit_comments = document.getElementById("submit_comments");

    if (submit_comments) {
        submit_comments.addEventListener("click", function () {
            window.location.href = "/blog/";
        });
    }

    const replyLinks = document.getElementsByClassName('reply');

    [...replyLinks].forEach(function (replyLink) {
        replyLink.addEventListener('click', function (event) {
            // event.preventDefault();
            const commentId = replyLink.getAttribute('href').replace('#reply_', '');
            const replyForm = document.getElementById('reply_form_' + commentId);
            if (replyForm.style.display === 'none') {
                replyForm.style.display = 'block';
            } else {
                replyForm.style.display = 'none';
            }
        });
    });

});
// document.querySelectorAll('reply').forEach(function(replyLink) {
//         replyLink.addEventListener('click', function(event) {
//             event.preventDefault();
//             const formId = this.getAttribute('href').substring(1);
//             const form = document.getElementById(formId);
//             form.style.display = (form.style.display === 'none') ? 'block' : 'none';
//         });
//     });