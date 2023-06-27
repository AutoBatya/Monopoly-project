const combinations = { 
1: [5], 
2: [3, 7], 
3: [3, 5, 7], 
4: [1, 3, 7, 9], 
5: [1, 3, 5, 7, 9], 
6: [1, 3, 4, 6, 7, 9], 
};

let menuItems = document.querySelectorAll('.menu__item');
const betBtn = document.querySelector(".bet");
const dice1 = document.getElementById('dice-1');
const dice2 = document.getElementById('dice-2');
const resultTxt = document.querySelector('.result');
const odd = document.querySelector('.odd');
const even = document.querySelector('.even');
const balance = document.querySelector('.balance');
let money;
let id;

/*let xhr = new XMLHttpRequest();
let url = "https://url.com";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
    console.log(this.responseText);
    }
};*/
const getID = async () => {
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/users/10');
    const data = await response.json();
    id = data.id;
    console.log(`received an ID ${id}...`)
  } catch(e) {
    resultTxt.style.display = 'flex';
    resultTxt.querySelector('p').textContent = 'Невозможно получить ID!';
    console.error(e);
  }
};

getID();

const getBalance = async (id) => {
  try {
    const response = await fetch(`https://jsonplaceholder.typicode.com/users/10`);
    const data = await response.json();
    balance.textContent = `$${data.id}`;
    money = data.id;
  } catch(e) {
    money = undefined;
    resultTxt.style.display = 'flex';
    resultTxt.querySelector('p').textContent = 'Невозможно получить баланс!';
    console.error(e);
  }
};

getBalance(); 

// Меню 
menuItems.forEach(menuItem => {
  menuItem.addEventListener('click', () => {
      menuItems.forEach(item => {
          item.classList.remove('checked');
      })
      menuItem.classList.add('checked');
      console.log('Transition to another page')
  })
});

// Кнопка "нечетные"
odd.addEventListener('click', evt => {
  evt.preventDefault();
  odd.classList.add('checked-btn');
  even.classList.remove('checked-btn');
});

// Кнопка "четные"
even.addEventListener('click', evt => {
  evt.preventDefault();
  even.classList.add('checked-btn');
  odd.classList.remove('checked-btn');
});

// Кнопка "ставка"
betBtn.addEventListener("click", function(evt)
{
  evt.preventDefault();
  if(!even.classList.contains('checked-btn') && !odd.classList.contains('checked-btn')) {
    resultTxt.style.display = 'flex';
    resultTxt.querySelector('p').textContent = 'Выберите ставку!';
    return;
  }
  if((money || money === 0) && id) {
    resultTxt.style.display = 'flex';
    let betValue = document.getElementById('stavka').value;
    if(isNaN(betValue)) {
      resultTxt.querySelector('p').textContent = 'Введено не число!';
      return;
    }
    betValue = Number(betValue);
    if(betValue > money) {
      resultTxt.querySelector('p').textContent = 'Недостаточно денег!';
      return;
    }
    if(betValue <= 0) {
      resultTxt.querySelector('p').textContent = 'Введите ставку больше 0!';
      return;
    }
    money -= betValue;
    resultTxt.querySelector('p').textContent = '';
    dice1.style.transform = `rotate(360deg) translateY(-10px)`;
    dice2.style.transform = `rotate(360deg) translateY(-10px)`;
    setTimeout(() => {
      dice1.style.transform = ``;
      dice2.style.transform = ``;
    }, 250);
    let diceNum1 = getRandomInt(1, 6);
    let diceNum2 = getRandomInt(1, 6);
    let sum = diceNum1 + diceNum2;
    resultTxt.style.display = 'flex';
    if(odd.classList.contains('checked-btn') && sum % 2 === 1) {
      resultTxt.querySelector('p').textContent = `Вы выиграли $${betValue}!`;
      money += betValue * 2;
    } else if (even.classList.contains('checked-btn') && sum % 2 === 0) {
      resultTxt.querySelector('p').textContent = `Вы выиграли $${betValue}!`;
      money += betValue * 2;
    } else {
      resultTxt.querySelector('p').textContent = `Вы проиграли $${betValue}!`;
    }
    /*
    Отправка на сервер
    const obj = {
      'id': id,
      'money': money
    };
    xhr.send(obj);
    */
    showDots(dice1, diceNum1);
    showDots(dice2, diceNum2);
    balance.textContent = `$${money}`;

  }
});

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

function showDots(dice, number) {
  dice.querySelectorAll('.dot').forEach(dot => dot.style.display = "none");
  combinations[number].forEach(d => dice.querySelector(`.dot-${d}`).style.display = "block");
}

