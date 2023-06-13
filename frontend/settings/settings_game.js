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
let myButton = document.getElementById('button');
    myButton.addEventListener('click',function (ev) {
        let count_gamers = document.forms['settings'].elements['count_gamers'].value;
        let budget_gamers = document.forms['settings'].elements['budget_gamers'].value;
        let obj = {};
        obj['count_gamers']=count_gamers;
        obj['budget_gamers']=budget_gamers;
        obj = JSON.stringify(obj);
        //xhr.send(obj);
    })


