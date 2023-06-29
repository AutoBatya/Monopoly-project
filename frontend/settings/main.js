document.querySelector("#button").addEventListener("click", sendPlayerInfo);

function sendPlayerInfo() {
  // Получение значений количества игроков и бюджета
        var playersNumber = document.getElementById("number").value;
        var playersBudget = document.getElementById("budget").value;

  // Формирование объекта с информацией
  var playerInfo = {
    playersNumber: playersNumber,
    playersBudget: playersBudget
  };

  // Определение параметров запроса
  var requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(playerInfo)
  };

  // Отправка запроса на сервер
  fetch('https://jsonplaceholder.typicode.com/users', requestOptions)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Ошибка при отправке данных:', error));
}