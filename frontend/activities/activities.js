let menuItems = document.querySelectorAll('.menu__item');
let activitiesList = document.querySelector('.activities__list');
let msg = document.querySelector('.activities__message__form__text');
let form = document.querySelector('.activities__message_form');
let activities = document.querySelector('.activities');
let errorMsg = document.querySelector('.activities__error');
let count = 0; // счетчик событий

/*let xhr = new XMLHttpRequest();
// адрес, куда мы отправим нашу JSON-строку
let url = "https://url.com";
// открываем соединение
xhr.open("POST", url, true);
// устанавливаем заголовок — выбираем тип контента, который отправится на сервер, в нашем случае мы явно пишем, 
//что это JSON
xhr.setRequestHeader("Content-Type", "application/json");
// когда придёт ответ на наше обращение к серверу, мы его обработаем здесь
xhr.onreadystatechange = function () {
    // если запрос принят и сервер ответил, что всё в порядке
    if (xhr.readyState === 4 && xhr.status === 200) {
    // выводим то, что ответил нам сервер — так мы убедимся, что данные он получил правильно
    console.log(this.responseText);
    }
};*/

// Создание события для передачи на сервер
const createAction = (id, type, details) => {
    let obj = {};
    obj['id'] = id;
    obj['type'] = type;
    obj['details'] = details;
    obj = JSON.stringify(obj);
    //xhr.send(obj);
}

// Обработчик для запроса
const createRequestHandler = (obj, fromID, toID, type, money) => {
    obj.addEventListener('click', (evt) => {
        evt.preventDefault();
        createAction(fromID, type, {'id': toID, 'money': money});

        if(type === 'accept') {
            createAction(toID, 'transaction', {'id': fromID, 'money': money})
        }
    })
}

// Добавление нового сообщения
form.addEventListener('submit', (evt) => {
    evt.preventDefault();
    if (!msg.value)
        return;
    let newMsg = createMessage(myId, msg.value);
    activitiesList.appendChild(newMsg); 

    createAction(myId, 'message', msg.value);

    msg.value = '';
    activities.scrollTop = activities.scrollHeight;
})

//Запрос к серверу на получение данных
/*let isFirst = true;
let previousData = 0;
function fetchData() {
    // Вызываем API для получения массива данных
    fetch("https://jsonplaceholder.typicode.com/todos")
    .then(response => response.json())
    .then(data => {
    console.log('Data received successfully');
    if(isFirst) {
        //initializeActions(data);
        console.log('Displaying data');
        isFirst = false;
        previousData = data.length;
        activities.scrollTop = activities.scrollHeight;
    }
    if(data.length > previousData && !isFirst) {
    location.reload();
    }
    })
    .catch(error => {
        console.log("Error:", error);
        errorMsg.style.display = 'flex';
    });
}
    
// Вызываем функцию fetchData() каждую секунду
setInterval(fetchData, 1000);*/


// Свой айди
let myId = 2;

/*fetch('https://jsonplaceholder.typicode.com/todos')
.then(response => response.json())
.then(json => {myId = json['id']})
.catch(error => {
    console.error(error)
})*/

// Список игроков, номер их аватара и имя
const players = [
    {
        'id': 1,
        'avatar': 3,
        'name': 'Пётр'
    },
    {
        'id': 2,
        'avatar': 3,
        'name': 'Иван'
    },
    {
        'id': 3,
        'avatar': 2,
        'name': 'Александра'
    }
];

// Список действий
const actions = [
    {
        'id': 1,
        'player': 1,
        'type': 'connection'
    },
    {
        'id': 2,
        'player': 2,
        'type': 'connection',
    },
    {
        'id': 3,
        'player': 2,
        'type': 'message',
        'details': 'Я присоединился!'
    },
    {
        'id': 4,
        'player': 1,
        'type': 'message',
        'details': 'играем?'
    },
    {
        'id': 5,
        'player': 3,
        'type': 'connection'
    },
    {
        'id': 6,
        'player': 2,
        'type': 'request',
        'details': {
            'id': 2,
            'money': 200
        }
    },
    {
        'id': 7,
        'player': 3,
        'type': 'dice',
        'details': 9
    },
    {
        'id': 8,
        'player': 2,
        'type': 'request',
        'details': {
            'id': 3,
            'money': 100
        }
    },
    {
        'id': 9,
        'player': 1,
        'type': 'message',
        'details': 'я банкрот!'
    },
    {
        'id': 10,
        'player': 3,
        'type': 'message',
        'details': 'ха'
    },
    {
        'id': 11,
        'player': 2,
        'type': 'dice',
        'details': 3
    },
    {
        'id': 12,
        'player': 1,
        'type': 'dice',
        'details': 7
    },
    {
        'id': 13,
        'player': 2,
        'type': 'message',
        'details': 'дайте денег'
    },
];

// Меню над игровым чатом
menuItems.forEach(menuItem => {
    menuItem.addEventListener('click', () => {
        menuItems.forEach(item => {
            item.classList.remove('checked');
        })
        menuItem.classList.add('checked');
    })
});

// Создать экземпляр типа "Соединение"
const createConnection = (name, id) => {
    let item = document.createElement('p');
    item.classList.add('activities__list__item');
    if(myId === id)
        item.textContent = 'Вы присоединились к игре';
    else
        item.textContent = name + ' присоединился к игре';
    return item;
}

// Создать экземпляр типа "Сообщение"
const createMessage = (id, message) => {
    let item = document.createElement('div');
    let img = document.createElement('div');
    let p = document.createElement('div');

    item.classList.add('activities__list__message');
    img.classList.add('activities__list__message__img');
    players.forEach(player => {
        if(player['id'] === id) {
            if(id === myId) {
                item.classList.add('my-message');
            } else
                img.style.backgroundImage = `url(img/avatar${player['avatar']}.svg)`;
        }
    })
    p.classList.add('activities__list__message__p');
    p.textContent = message;

    item.appendChild(img);
    item.appendChild(p);
    return item;
}

// Создать экземпляр типа "Бросок кубиков"
const createDice = (action) => {
    let item = document.createElement('div');
    let p = document.createElement('p');

    item.classList.add('activities__list__dice');
    players.forEach(player => {
        if(action['player'] === player['id'])
            p.textContent = `${player['name']} бросает кубики. Выпало число ${action['details']}!`;
    })
    item.appendChild(p);
    return item;
}

// Обработчик на экземпляр типа "Запрос"
const addRequestHandler = (item, name, sum) => {
    let actions = item.querySelector('.activities__list__money-request__actions'); 
    let p = item.querySelector('p');

    actions.querySelector('.activities__list__money-request__actions__accept')
    .addEventListener('click', () => {
        actions.style.display = 'none';
        p.textContent = 'Запрос на ' + sum + '$ от ' + name + ' принят';
    });
    actions.querySelector('.activities__list__money-request__actions__decline')
    .addEventListener('click', () => {
        actions.style.display = 'none';
        p.textContent = 'Запрос на ' + sum + '$ от ' + name + ' отклонен';
    });
}

// Создать экземпляр типа "Запрос"
const createRequest = (action) => {
    let item = document.createElement('div');
    let p = document.createElement('p');
    let actions = document.createElement('div');
    let decline = document.createElement('a');
    let accept = document.createElement('a');

    item.classList.add('activities__list__money-request');

    if(action['details']['id'] === myId) {
        actions.classList.add('activities__list__money-request__actions');
        decline.classList.add('activities__list__money-request__actions__decline');
        accept.classList.add('activities__list__money-request__actions__accept');
        accept.href = '#';
        decline.href = '#';

        createRequestHandler(accept, action['details']['id'], myId, 'accept', action['details']['money']);
        createRequestHandler(decline, action['details']['id'], myId, 'decline', action['details']['money']);

        actions.appendChild(decline);
        actions.appendChild(accept);
        players.forEach(player => {
        if(action['player'] == player['id']) {
            p.textContent = player['name'] + ' запрашивает ' 
            + action['details']['money'] + '$';
        }
        })
    } else {
        players.forEach(player => {
            if(action['player'] == player['id']) {
                p.textContent = player['name'] + ' запрашивает ' 
                + action['details']['money'] + '$ у ';
            }
        })
        players.forEach(player => {
            if(action['details']['id'] == player['id']) {
                p.textContent += player['name'];
            }
        })
    }

    item.appendChild(p);
    if(action['details']['id'] === myId) {
        item.appendChild(actions);
        players.forEach(player => {
            if(action['player'] === player['id']) {
                addRequestHandler(item, player['name'], action['details']['money']);
            }
        })
    }
    return item;
}

// Создать все действия
const initializeActions = (actions) => {
    actions.forEach(action => {
        if(action['type'] === 'connection') {
            let item;
            players.forEach(player => {
                if(action['player'] == player['id']) {
                    item = createConnection(player['name'], player['id']);
                }
            })
            activitiesList.appendChild(item);
        } 
        if (action['type'] === 'message') {
            let item;
            players.forEach(player => {
                if(action['player'] == player['id']) {
                    item = createMessage(player['id'], action['details']);
                }
            })
            activitiesList.appendChild(item);
        }
        if(action['type'] === 'request') {
            let item = createRequest(action);
            activitiesList.appendChild(item);
        }
        if(action['type'] === 'dice') {
            let item = createDice(action);
            activitiesList.appendChild(item);
        }
    })
}

// Отрисовать действия (actions - заглушка)
initializeActions(actions);
