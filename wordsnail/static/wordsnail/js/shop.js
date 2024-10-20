document.addEventListener("DOMContentLoaded", function() {
    if (userAuthenticated == 2) {
        showAlert();
    }

    const cards = document.querySelectorAll('.card');

    cards.forEach((card, index) => {
        // Задаем задержку для каждой карточки
        card.style.animationDelay = `${index * 0.2}s`; // 0.2 секунды между появлениями
    });
});


function showAlert() {
    console.log("alert");
    const alertContainer = document.getElementById('alert');
    if (alertContainer) {
        alertContainer.classList.add('show');
    }
}

function closeAlert() {
    const alertContainer = document.getElementById('alert');
    if (alertContainer) {
        alertContainer.classList.remove('show');
        // Удаляем алерт из DOM через время, чтобы завершить анимацию
        setTimeout(() => {
            alertContainer.remove();
        }, 300);

        window.location.href = window.location.pathname;
    }
}


function goLogin() {
    window.location.href = loginUrl;
}