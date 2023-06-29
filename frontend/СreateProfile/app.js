document.addEventListener('DOMContentLoaded', function() {
    const icons = document.querySelectorAll('.selection_icons-js');
    const inputName = document.querySelector('.type_name');
    const startGameLink = document.querySelector('.start_game_link');
    const nameDisplay = document.querySelector('.name_display');
  
    icons.forEach(icon => {
    icon.addEventListener('click', function() {
        icons.forEach(icon => icon.classList.remove('active')); 
        // Добавляем класс active выбранной иконке
        this.classList.add('active');
    });
    });
    if (startGameLink) { // Проверяем, существует ли startGameLink
    startGameLink.addEventListener('click', function(e) {
        // Отменяем обычное поведение ссылки
        e.preventDefault();
        // Проверяем, есть ли выбранная иконка
        const selectedIcon = document.querySelector('.selection_icons-js.active');
        if (!selectedIcon) {
        alert('Выберите аватарку');
        return;
        }
        // Проверяем, введено ли имя
        if (inputName.value.trim() === '') {
        alert('Введите имя');
        return;
        }
        // Получаем данные выбранной иконки и имени
        const avatar = selectedIcon.getAttribute('data-name');
        const name = inputName.value.trim();
        // Формируем объект для отправки на сервер
        const data = {
        avatar: avatar,
        name: name
        };
        // Отправляем данные на сервер
        fetch('https://jsonplaceholder.typicode.com/users', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
        })
        .then(response => response.json())
        .then(data => {
          // Полученные данные от сервера
        console.log(data);
        
        
          // Перенаправление на другую страницу
        window.location.href = './profile.html';
        })
        .catch(error => {
        console.error('Error:', error);
        });
        const nameDisplay = document.querySelector('.name_display');
        // Отправить запрос на сервер для получения данных о имени пользователя
        fetch('https://jsonplaceholder.typicode.com/users/15')
        .then(response => response.json())
        .then(data => {
        // Обновить содержимое элемента "name_display" с данными о имени пользователя
        nameDisplay.textContent = data.userName;
        })
        .catch(error => {
    console.error('Ошибка при получении данных о пользователе:', error);
    
});
    });
    }
    
});

