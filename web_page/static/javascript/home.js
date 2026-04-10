const get_started = document.getElementById('get_started')
const get_workspace = document.getElementById('get_workspace')

if (download) {
    get_workspace.addEventListener('click', function() {
        window.location.href = "/download";
    });
}

if (sign_up) {
    get_started.addEventListener('click', function() {
        window.location.href = "/sign_up";
    });
}