document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("board");
    const message = document.getElementById("message");

    let solution = ""; // Загаданное слово, получаемое с сервера
    let currentRow = [];
    let currentGuess = "";
    let rowCount = 0;
    let wordLen = 0;
    let countWrongAnswers = 0;
    let prize = 65;

    // Запрашиваем случайное слово с сервера
    fetch('/api/random-word/')
        .then(response => response.json())
        .then(data => {
            solution = data.word.toLowerCase();
            wordLen = Number(data.len);
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

        if(wordLen == 4)
            row.classList.add("row_for_4_letters");
        else if(wordLen == 5)
            row.classList.add("row_for_5_letters");
        else if(wordLen == 6)
            row.classList.add("row_for_6_letters");

        for (let i = 0; i < wordLen; i++) {
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

        if (/^[a-zA-Zа-яА-ЯёЁ]$/.test(event.key) && currentGuess.length < wordLen) {
            // Добавляем букву в текущее предположение
            currentGuess += event.key.toLowerCase();
            updateCurrentRow();
        } else if (event.key === "Backspace" && currentGuess.length > 0) {
            // Удаляем последнюю букву
            currentGuess = currentGuess.slice(0, -1);
            updateCurrentRow();
        } else if (event.key === "Enter" && currentGuess.length === wordLen) {
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

    function calculatingReward(count) {
        if(count == 0)
            return prize

        if(count == 6)
            return 0;

        return (prize - prize%count) / count;
    }

    function submitGuess() {
        if (currentGuess === solution) {
            markRow("correct");
            // alert("Поздравляем! Вы угадали слово!");
            showWinAlert();
            // message.textContent = "Поздравляем! Вы угадали слово!";
            const data = { 
                money: calculatingReward(countWrongAnswers)
            }

            fetch('/api/put-cash/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() // Для защиты от CSRF-атак
                },
                body: JSON.stringify(data)
            })
            // .then(response => response.json())
            // .then(data => {
            //     console.log('Success:', data); // Обработка ответа от сервера
            // })
            // .catch((error) => {
            //     console.error('Error:', error);
            // });

            document.removeEventListener("keydown", handleKeyPress);

        } else {
            checkGuess();
            if (++rowCount < 6) {
                createEmptyRow();
                currentGuess = "";
                countWrongAnswers++;
            } else {
                showLoseAlert()
                // message.textContent = `Игра окончена! Загаданное слово: "${solution}".`;
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


    function showWinAlert() {
        // Создаем контейнер алерта
        const alertContainer = document.createElement('div');
        alertContainer.className = 'alert-container';
        alertContainer.id = 'alert';
        alertContainer.innerHTML = `
            <div class="alert-content">
                <h2>Вы победили!</h2>
                <p>Ты просто unstoppable! Как настоящий clever boy, ты угадал слово и теперь можешь спокойно занять место у водителя!</p>
                <p>Ваша награда: &#128012; ${calculatingReward(countWrongAnswers)}</p>
                <button onclick="closeAlert()">Закрыть</button>

                <!-- Контейнер для кнопок "Домой" и "Магазин" -->
                <div class="button-container">
                    <button onclick="goHome()">Домой</button>
                    <button onclick="goToShop()">Магазин</button>
                </div>
            </div>
        `;

        // Добавляем контейнер в body
        document.body.appendChild(alertContainer);

        document.querySelector('.alert-content h2').style.color = "#2ecc71";
        document.querySelector('.alert-content button').style.backgroundColor = "#2ecc71";

        // Показываем алерт с помощью класса "show"
        setTimeout(() => {
            alertContainer.classList.add('show');
        }, 10);
    }

    

    function showLoseAlert() {
        const alertContainer = document.createElement('div');
        alertContainer.className = 'alert-container';
        alertContainer.id = 'alert';
        alertContainer.innerHTML = `
            <div class="alert-content">
                <h2>Вы проиграли!</h2>
                <p>Кажется, wicked пассажиры оказались быстрее… Но не сдавайся! Еще одна попытка, и ты точно окажешься у руля.</p>
                <p>Правильное слово: <strong>${solution}</storng></p>
                <p>Ваша награда: &#128012; 0</p>
                <button onclick="closeAlert()">Закрыть</button>

                <!-- Контейнер для кнопок "Домой" и "Магазин" -->
                <div class="button-container">
                    <button onclick="goHome()">Домой</button>
                    <button onclick="goToShop()">Магазин</button>
                </div>
            </div>
        `;

        // Добавляем контейнер в body
        document.body.appendChild(alertContainer);

        // Показываем алерт с помощью класса "show"
        setTimeout(() => {
            alertContainer.classList.add('show');
        }, 10);
    }

   
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


function goHome() {
    window.location.href = homeUrl;
}

function goToShop() {
    window.location.href = shopUrl;
}

function restartGame() {
    location.reload();
}