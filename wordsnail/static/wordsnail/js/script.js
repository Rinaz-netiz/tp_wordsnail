document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeAlert();
    }
});


// Функция для получения CSRF-токена из cookies
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmedCookie = cookie.trim();
        if (trimmedCookie.startsWith(`${name}=`)) {
            return trimmedCookie.substring(name.length + 1);
        }
    }
    return '';
}
