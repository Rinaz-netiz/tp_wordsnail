document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach((card, index) => {
        // Задаем задержку для каждой карточки
        card.style.animationDelay = `${index * 0.2}s`; // 0.2 секунды между появлениями
    });
});

function goLogin() {
    window.location.href = loginUrl;
}