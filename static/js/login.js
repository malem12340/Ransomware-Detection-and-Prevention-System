// Login UI enhancement only.
// Authentication is handled by Flask.

const username = document.getElementById("username");
const password = document.getElementById("password");

username.addEventListener("focus", function () {
    this.style.border = "2px solid #4da6ff";
});

password.addEventListener("focus", function () {
    this.style.border = "2px solid #4da6ff";
});

username.addEventListener("blur", function () {
    this.style.border = "none";
});

password.addEventListener("blur", function () {
    this.style.border = "none";
});