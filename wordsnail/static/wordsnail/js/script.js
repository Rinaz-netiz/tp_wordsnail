document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach((card, index) => {
        // Задаем задержку для каждой карточки
        card.style.animationDelay = `${index * 0.2}s`; // 0.2 секунды между появлениями
    });
});


function closeAlert() {
    const restartButton = document.getElementById('restart-container');
    restartButton.style.display = 'block';

    const alertContainer = document.getElementById('alert');
    if (alertContainer) {
        alertContainer.classList.remove('show');
        // Удаляем алерт из DOM через время, чтобы завершить анимацию
        setTimeout(() => {
            alertContainer.remove();
        }, 300);
    }

}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeAlert();
    }
});


function goLogin() {
    window.location.href = loginUrl;
}