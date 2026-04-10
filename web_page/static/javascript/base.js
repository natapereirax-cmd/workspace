const home = document.getElementById('home');
const about_us = document.getElementById('about_us');
const download = document.getElementById('download');
const sign_up = document.getElementById('sign_up');

if (home) {
    home.addEventListener('click', function() {
        window.location.href = "/home";
    });
}

if (about_us) {
    about_us.addEventListener('click', function() {
        window.location.href = "/about_us";
    });
}

if (download) {
    download.addEventListener('click', function() {
        window.location.href = "/download";
    });
}

if (sign_up) {
    sign_up.addEventListener('click', function() {
        window.location.href = "/sign_up";
    });
}