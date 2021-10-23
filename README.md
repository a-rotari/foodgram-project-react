ДЕМО ПРОЕКТА РАБОТАЕТ (hopefully) ПО АДРЕСУ: http://larart.ru
Панель администратора: http://larart.ru/admin/

Проект Foodgram
Ваш так называемый «Продуктовый помощник». Представляет собой прототип онлайн-сервиса и API для него. На этой платформе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Ниже описаны базовые модели проекта:
(Более подробно с базовыми моделями можно ознакомиться в спецификации API, после деплоя проекта она доступна по адресу /foodgram/docs/)

Рецепт
Рецепт описывается такими полями:

- Автор публикации (пользователь).
- Название.
- Картинка.
- Текстовое описание.
- Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
- Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
- Время приготовления в минутах.

Тег
Тег описывается такими полями:

Название.
Цветовой HEX-код (например, #49B64E).

Slug.

Ингредиент
Ингредиент описывается такими полями:

- Название.
- Количество.
- Единицы измерения.

Ниже описаны сервисы и страницы проекта:

Главная страница
Содержимое главной страницы — список рецептов.

Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.
Сценарий поведения пользователя:
Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.
Сценарий поведения пользователя:
Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
При необходимости пользователь может удалить рецепт из избранного.

Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.
Сценарий поведения пользователя:
Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в виде текстового файла.
При скачивании списка покупок ингредиенты в результирующем списке не дублируются; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке один пункт: Сахар — 15 г.

Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.

Регистрация и авторизация
В проекте доступна система регистрации и авторизации пользователей.

Обязательные поля для пользователя:
Логин
Пароль
Email
Имя
Фамилия

Уровни доступа пользователей:
Гость (неавторизованный пользователь)
Авторизованный пользователь
Администратор

Что могут делать неавторизованные пользователи
Создать аккаунт.
Просматривать рецепты на главной.
Просматривать отдельные страницы рецептов.
Фильтровать рецепты по тегам.

Что могут делать авторизованные пользователи
Входить в систему под своим логином и паролем.
Выходить из системы (разлогиниваться).
Менять свой пароль.
Создавать/редактировать/удалять собственные рецепты
Просматривать рецепты на главной.
Просматривать страницы пользователей.
Просматривать отдельные страницы рецептов.
Фильтровать рецепты по тегам.
Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
изменять пароль любого пользователя,
создавать/блокировать/удалять аккаунты пользователей,
редактировать/удалять любые рецепты,
добавлять/удалять/редактировать ингредиенты.
добавлять/удалять/редактировать теги.
Все эти функции реализованы в стандартной админ-панели Django.

Инфраструктура проекта:
Проект использует базу данных PostgreSQL.

В Django-проекте есть файл requirements.txt со всеми зависимостями.
Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом пушится на Docker Hub.

Деплой проекта
Для развертывания проекта у вас на машине должен быть установлен docker-compose. Форкните репозиторий с гитхаба.

Подготовьте remote server к развертыванию проекта:
Для работы проекта на сервере должна работать операционная система Linux Ubuntu, выполнены базовые настройки безопасности, установлены docker и docker-compose.
Запустите терминал и клонируйте ваш форк проекта на сервер.
Войдите в директорию infra и создайте .env файл со следующими переменными (значения переменных ниже приведены в качестве примера):

DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=very_secret_key

Не покидая директорию infra выполните команду 'docker-compose up'

При развертывании контейнеров будут автоматически выполнены миграции, в базу данных будет загружена информация о ингредиентах, будут созданы три тега.
Также будет создана учетная запись администратора (юзернем -- admin, пароль -- админ) для работы в админке Django. Рекомендуется сменить пароль администратора сразу после начала работы с админкой.

Админка доступна по адресу '/admin/'

Работа с проектом
Подробная документация по работе с проектом доступна по адресу '/foodgram/docs/'
