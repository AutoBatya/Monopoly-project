const transactions = [];

async function getUsername() {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const data = await response.json();
        const randomIndex = Math.floor(Math.random() * data.length);
        return data[randomIndex].name;
    } catch (error) {
        console.log("Error:", error);
        return "Unknown User"; // На случай ошибки
    }
}

async function addTransaction(type, amount) {
    const fromUser = await getUsername();
    const toUser = await getUsername();

    const transaction = {
        type: type,
        amount: amount,
        from: fromUser,
        to: toUser
    };

    transactions.push(transaction);
    updateUI(transaction); // Обновляем интерфейс сразу после добавления транзакции
}

function updateUI(transaction) {
    const transactionsDiv = document.querySelector('.transactions');
    const balanceSpan = document.getElementById('balance');

    if (!transactionsDiv || !balanceSpan) {
        console.error("Не удалось найти элемент для транзакций или баланса.");
        return;
    }

    // Инициализация баланса, если он не задан
    let balance = parseFloat(balanceSpan.textContent) || 0;
    let transactionMessage;

    // Создаем текст сообщения транзакции
    if (transaction.type === 'received') {
        transactionMessage = `${transaction.from} отправил ${transaction.amount} долларов ${transaction.to}.`;
        balance += transaction.amount; // Увеличиваем баланс при получении денег
    } else if (transaction.type === 'sent') {
        transactionMessage = `${transaction.from} отправил ${transaction.amount} долларов ${transaction.to}.`;
        balance -= transaction.amount; // Уменьшаем баланс при отправке денег
    }

    // Добавляем сообщение о транзакции на страницу
    const transactionElement = document.createElement('div');
    transactionElement.textContent = transactionMessage;
    transactionsDiv.appendChild(transactionElement);

    // Обновляем значение баланса на странице
    balanceSpan.textContent = balance.toFixed(2); // Округляем до 2 знаков
}

// Установим начальный баланс (чтобы был равен 0 изначально)
document.getElementById('balance').textContent = '0.00';

// Пример добавления новых транзакций
addTransaction('received', 100);
addTransaction('sent', 50);
addTransaction('received', 200);
