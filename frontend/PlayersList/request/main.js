document.addEventListener('DOMContentLoaded', () => {
    const url = new URL(window.location.href);
    let id = url.searchParams.get("id");
    document.getElementById('id').innerHTML = id;
});

document.addEventListener('DOMContentLoaded', () => {
  const url = new URL(window.location.href);
  let id = url.searchParams.get("id");
  document.getElementById('id').innerHTML = id;
});

function sendMoney() {
  const url = new URL(window.location.href);
  let id = url.searchParams.get("id");
  let amount = document.getElementById('num_count').value;
  
  // Отправить запрос на сервер с указанием id и суммы
  fetch(`https://jsonplaceholder.typicode.com/users/${id}/sendMoney`, {
    method: 'POST',
    body: JSON.stringify({ amount }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    // Обработать ответ от сервера
    // В этом примере мы просто выводим ответ в консоль
    console.log(data);
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
}

function decline() {
  // Выполнить действия при отклонении перевода

  // Показать сообщение об успешном отклонении
  alert('Вы отменили перевод денег');
}

function accept() {
  // Выполнить действия при принятии перевода

  // Получить ID игрока
  const id = document.getElementById('id').textContent;

  // Получить сумму перевода
  const moneyAmount = document.getElementById('num_count').value;

  // Проверить, что сумма перевода не пустая
  if (moneyAmount) {
    // Отправить запрос на перевод денег
    fetch(`https://example.com/api/transfer-money?id=${id}&amount=${moneyAmount}`)
      .then(response => {
        if (response.ok) {
          // Показать сообщение об успешном переводе
          alert('Деньги успешно переведены');
        } else {
          // Показать сообщение о неудачном переводе
          alert('Не удалось перевести деньги');
        }
      })
      .catch(error => {
        // Показать сообщение об ошибке
        alert('Произошла ошибка при выполнении запроса');
      });
  } else {
    // Показать сообщение о необходимости ввести сумму перевода
    alert('Введите сумму перевода');
  }
}

function redirectToPlayerList() {
  // Произвести переход на страницу PlayerList.html
  window.location.href = 'Список игроков/PlayerList.html';
}