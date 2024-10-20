document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach((card, index) => {
        // Задаем задержку для каждой карточки
        card.style.animationDelay = `${index * 0.2}s`; // 0.2 секунды между появлениями

        // Находим кнопку внутри текущей карточки
        const shopButton = card.querySelector('.shopBt');
        if (shopButton) {
            shopButton.addEventListener('click', function() {
                const itemId = this.getAttribute('data-id');
                const itemPrice = this.getAttribute('data-price');
                const action = this.getAttribute('data-act');

                // Проверяем, авторизован ли пользователь
                if (!userAuthenticated) {
                    showAlert(); // Показываем алерт, если не авторизован
                } else {
                    handlePurchase(itemId, itemPrice, action); // Обрабатываем покупку
                }
            });
        }
    });
});

function handlePurchase(itemId, itemPrice, action) {
    // Пример AJAX-запроса
    fetch('api/buy-item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),  // Не забудьте добавить CSRF-токен
        },
        body: JSON.stringify({ id: itemId, price: itemPrice, act: action }),
    })
    .then(response => {
        if (response.ok) {
            console.log('Покупка успешно завершена');

            window.location.href = window.location.pathname;;
        } else {
            console.error('Ошибка при покупке');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}



function showAlert() {
    const alertContainer = document.getElementById('alert');
    if (alertContainer) {
        alertContainer.style.display = 'block';
        alertContainer.classList.add('show');
    }
}

function closeAlert() {
    const alertContainer = document.getElementById('alert');
    if (alertContainer) {
        alertContainer.classList.remove('show');
        // Скрываем алерт вместо его удаления
        setTimeout(() => {
            alertContainer.style.display = 'none';
        }, 300);
    }
}


function goLogin() {
    window.location.href = loginUrl;
}