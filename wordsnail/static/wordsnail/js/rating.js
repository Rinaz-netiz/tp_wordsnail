    document.addEventListener('DOMContentLoaded', function() {
        const tableContainer = document.querySelector('.table-container-unique');
        tableContainer.classList.add('visible'); // Добавляем класс для запуска анимации
    });

    // Функция фильтрации таблицы
    function filterTable() {
        const input = document.getElementById('searchInput');
        const filter = input.value.toLowerCase();
        const table = document.getElementById('leaderboardTable');
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) { // Пропускаем заголовок
            const cells = rows[i].getElementsByTagName('td');
            let match = false;

            // Проверяем каждую ячейку в строке
            for (let j = 1; j < cells.length; j++) { // Начинаем с 1, чтобы пропустить "Место"
                if (cells[j].innerText.toLowerCase().includes(filter)) {
                    match = true;
                    break;
                }
            }

            rows[i].style.display = match ? "" : "none"; // Показываем или скрываем строку
        }
    }