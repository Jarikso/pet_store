# Django-diploma - Placemarket
## Содержание
- Описание приложения <br/>
- Запуск приложения <br/>
- Структура приложения <br/>
- Используемые библиотеки <br/>

## Описание клиента
Web-сервис, практическая работа реализации интернет магазина <br/>
Ссылка для работы с клиентом: [добавить ссылку](ссылка) <br/>

## Заупуск приложения

Создание вируального окружения:<br/>
- python -m venv <название виртуального окружения>

Установка библиотек:<br/>
- pip install -r requirements.txt

Запуск приложения на локальном сервере:<br/>
- python manage.py runserver

## Структура приложения

- [name='main_page'] или '/' - главная страница приложения
- /catalog - список, каталог товаров
- /catalog/<slug:slug> - детальная страница товаров
- /demo - демонстративная версия станицы /report
- /account/sign-up - страница регистрации
- /account/login_passim - страдица входа в аккаунт
- /account/logout - страница выхода из аккаунта
- /account/<int:pk> - страница профиля
- /account/<int:pk>/change - страница редактирования профиля
- /cart - страниуца корзины
- /order - страница оформления заказа
- /order/history/<int:pk> - история заказов клиента
- /order/only-order/<int:pk> - детальная страница заказа

## Используемые библиотеки сторонние библиотеки
<table align="center">
    <tr>
        <td align="center">Package</td>
        <td align="center">Version</td>
    </tr>
    <tr>
        <td align="center">asgiref</td>
        <td align="center">3.5.2</td>
    </tr>
    <tr>
        <td align="center">Django</td>
        <td align="center">4.1.2</td>
    </tr>
    <tr>
        <td align="center">django-filter</td>
        <td align="center">22.1</td>
    </tr>
    <tr>
        <td align="center">django-phonenumber-field</td>
        <td align="center">7.0.0</td>
    </tr>
    <tr>
        <td align="center">Pillow</td>
        <td align="center">9.2.0</td>
    </tr>
    <tr>
        <td align="center">pytz</td>
        <td align="center">2022.4</td>
    </tr>
    <tr>
        <td align="center">sqlparse</td>
        <td align="center">0.4.3</td>
    </tr>
</table>