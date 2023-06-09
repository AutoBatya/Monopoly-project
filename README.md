# Monopoli
Монополия онлайн

Участники и их роли:
| Имя - name  | Роль | Задачи |
| ------------- | ------------- | ------------- |
| Дамир  | Teamlead   | 2 + 3 |
| Оля  | Разработка интерфейса UX/UI  | 1 |
| Дима  | F | 20 |
| Саша  | F | 11 + 12 |
| Юлдаш  | F  | 16 |
| Генна  | F  | 7 + 8 |
| Валерия  | F  | 13 + 9 |
| Данил  | B  | 4 + 14 |
| Володя  | B  | 19 + 23 |
| Макар  | B  | 10 + 15 |
| Инна  | B  | 27 + 1 |
| Марат  | B  | 24 + 25 |
| Диана  | Database  | 3 + 5 |
| Олег  | F  |13 + 22 |
| Вадим  | F  | 18 |
| Даша  | B  | 6 + 17 |
| Алена  | F  | 26 |
| Ира  | F  | 28 |
| Даурен  | B  | 21 |
| Алексей  | B  | 29 |

## Дизайн сайта
https://www.figma.com/file/NJVOiHCoeSbqa17b0leegB/MONOPOLY?node-id=0%3A1&t=uHIAWs4VGFH0RVhg-1

## Схема взаимодействия экранов
https://www.figma.com/file/c5sMST73hOa9AGCMSJr1Wr/MONOPOLY?type=whiteboard&node-id=0-1&t=EXhf2PJx9VIxQJUk-0
## Docker

- [Установка](https://docs.docker.com/desktop/install/windows-install)
- [Документация по созданию Dockerfile](https://docs.docker.com/engine/reference/builder)
- [MySql Image](https://hub.docker.com/_/mysql)
- [Nginx Image](https://hub.docker.com/_/nginx)
- [Python Image](https://hub.docker.com/_/python)

Сборка:

_Перед запуском нужно установить свои значения в docker/.env/environments_

> docker-compose -f ./docker-compose.yaml --env-file ./.env/environments build

Запуск:

> docker-compose -f ./docker-compose.yaml --env-file ./.env/environments up

## OpenApi

- [Визуализация](https://editor.swagger.io)

# Задачи

## Основное:

1. Дизайнер: Дизайн. Исправить замечания и добавить нужные экраны
2. Тимлид: Решить все вопросы с распределением задачек, уведомлять об изменениях. Помогать другим при возникновении тупиковых проблем. 
3. Архитекор + Тимлид: Изучить мой репозиторий с примером, реализовать в репозитории с проектом запуск через докер, выделить общий стиль создания обработчиков API. Работа с базой. Миграции. Соглашения по проекту.

## Стартовый экран и подключение:

4. B1: Создание новой комнаты (API / Реализация)
5. B1: Присоединение к существующей комнате по id (API / Реализация)
6. B2: Присоединение к существующей комнате по QR коду, ссылке (API / Реализация)
7. F1: Стартовый экран, кнопки создать / присоединиться
8. F1: Экран ввода id для присоединения
9. F2: Экран с qr кодом (и его генерация)

## Старт игры и профиль:

10. B1: Создание профиля в контексте комнаты (API / Реализация)
11. F1: Экран создания профиля
12. F1: Экран профиля, кнопка выйти из игры
13. F1: Экран настройки и старта игры
14. B1: Старт игры с указанными настройками

## Игра:

15. B1: Запрос информации о текущем профиле и балансе по id комнаты и токену юзера
16. F2: Экран истории транзакций
17. B2: Запрос списка транзакций по id комнаты и токену юзера
18. F1: Экран списка игроков
19. B1: Запрос списка игроков по id комнаты
20. F1: Экран списка действий и событий игры (отправка сообщений, запросы денег, броски кубиков)
21. B1: Запрос списка действий по id комнаты и токену юзера. Возможность указать id последнего известного действия.
22. F1: Экран запроса / перевода денег игроку
23. B1: Перевод денег игроку
24. B1: Запрос денег у игрока
25. B1: Одобрение запроса денег
26. F2: Экран с кубиками
27. B2: Бросок кубиков с указанной ставкой (или без). (Убедиться что не используется псевдослучайный генератор чисел)
28. F2: Игровое поле
29. B2: На экране с игровым полем, сделать вывод количества игроков в сессии


Основные функции монополии:
Страница входа
1) Создать комнату (до 5 (опционально) игроков)
- Генерация номера комнаты – также для возможности входа
- Войти
2) Присоединиться к комнате
- Ввод комнаты
- Отсканировать QR-код
- Войти
3) Ввод имени/псевдонима (проверка на уникальность (?))
- Выбор аватара (из предложенных) (прокрутка аватаров)
Производится создание комнаты и игрока, начисляется фиксированные 100$ (?) каждому
авторизированному игроку
Комната (вкладки)
В левом верхнем углу статично пусть будет указан номер комнаты
1) Профиль (стартовая страница)
- Демонстрация имени
- Демонстрация аватара (нет возможности сменить)
- Демонстрация баланса счёта
   2) Список
- Имя/псевдоним
- Кнопка для запроса денег
- Кнопка для перевода денег
3) История транзакций
- Демонстрация входящих/исходящих отчислений 4) Активность/уведомления
Здесь будут высвечивать сообщения по типу игрок1 присоединился к комнате, игрок1 говорит «Всем привет!», игрок1 запрашивает 50$, игрок2 игнорирует итд.
- Демонстрация того, кто присоединяется к комнате
- Кнопка: возможность сформировать запрос на пополнение счета (с указанием
точной суммы в виде целого числа)
- Кнопка: возможность ответить на запрос и произвести перевод средств
запросившему (отправить деньги или игнорировать сообщение)
- Возможность отправить сообщение из предложенных фиксированных сообщение
(Всем привет / скиньте денег)
5) Вкладка с кубиками (?????)
- Кнопка бросить кубики (просто анимация)
- Сделать ставку (лимит баланс счета) четное или нечетное
- Если ставка сыграет, баланс увеличивается на сумму ставки, в противном случае
игроков
она уходит со счета
