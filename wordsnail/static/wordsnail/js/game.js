document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("board");
    const message = document.getElementById("message");

    let solution = ""; // Загаданное слово, получаемое с сервера
    let currentRow = [];
    let currentGuess = "";
    let rowCount = 0;
    let word_len = 0;

    // Запрашиваем случайное слово с сервера
    fetch('/api/random-word/')
        .then(response => response.json())
        .then(data => {
            solution = data.word.toLowerCase();
            word_len = Number(data.len);
            console.log("Загаданное слово:", solution); // Для проверки в консоли
            createEmptyRow(); // Создаем начальную строку пустых плиток после получения слова
        })
        .catch(error => {
            console.error('Ошибка при получении слова:', error);
            message.textContent = "Не удалось загрузить слово. Пожалуйста, попробуйте позже.";
        });

    document.addEventListener("keydown", handleKeyPress);

    function createEmptyRow() {
        const row = document.createElement("div");
        row.classList.add("row");

        if(word_len == 4) 
            row.classList.add("row_for_4_letters");
        else if(word_len == 5)
            row.classList.add("row_for_5_letters");
        else if(word_len == 6)
            row.classList.add("row_for_6_letters");

        for (let i = 0; i < word_len; i++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            row.appendChild(cell);
        }

        board.appendChild(row);
        currentRow = Array.from(row.children);
    }

    function handleKeyPress(event) {
        // Проверяем, находится ли фокус на элементе input
        if (document.activeElement.tagName === "INPUT") {
            return; // Если да, выходим из функции, чтобы не вводить буквы в плитки
        }

        if (message.textContent) message.textContent = "";

        if (/^[a-zA-Zа-яА-ЯёЁ]$/.test(event.key) && currentGuess.length < word_len) {
            // Добавляем букву в текущее предположение
            currentGuess += event.key.toLowerCase();
            updateCurrentRow();
        } else if (event.key === "Backspace" && currentGuess.length > 0) {
            // Удаляем последнюю букву
            currentGuess = currentGuess.slice(0, -1);
            updateCurrentRow();
        } else if (event.key === "Enter" && currentGuess.length === word_len) {
            submitGuess();
        }
    }

    function updateCurrentRow() {
        currentRow.forEach((cell, index) => {
            cell.textContent = currentGuess[index] || "";
            if (currentGuess[index]) {
                cell.classList.add("filled");
            } else {
                cell.classList.remove("filled");
            }
        });
    }

    function submitGuess() {
        if (currentGuess === solution) {
            markRow("correct");
            // alert("Поздравляем! Вы угадали слово!");
            showAlert()
            message.textContent = "Поздравляем! Вы угадали слово!";
            document.removeEventListener("keydown", handleKeyPress);
        } else {
            checkGuess();
            if (++rowCount < 6) {
                createEmptyRow();
                currentGuess = "";
            } else {
                alert(`Игра окончена! Загаданное слово: "${solution}".`);
                message.textContent = `Игра окончена! Загаданное слово: "${solution}".`;
                document.removeEventListener("keydown", handleKeyPress);
            }
        }
    }

    function checkGuess() {
        currentGuess.split("").forEach((letter, index) => {
            const cell = currentRow[index];

            if (letter === solution[index]) {
                cell.classList.add("correct");
            } else if (solution.includes(letter)) {
                cell.classList.add("present");
            } else {
                cell.classList.add("absent");
            }
        });
    }

    function markRow(status) {
        currentRow.forEach(cell => {
            cell.classList.add(status);
        });
    }

    function showAlert() {
        const alertBox = document.getElementById('winAlert');
        alertBox.style.display = 'block';
        alertBox.style.opacity = '1'; // Показать с анимацией
    }
   
});

function closeAlert() {
    const alertBox = document.getElementById('winAlert');
    alertBox.style.opacity = '0'; // Скрыть с анимацией
    setTimeout(() => {
        alertBox.style.display = 'none'; // Убрать из потока после анимации
    }, 300); // Время должно совпадать с длительностью transition
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeAlert();
    }
});
