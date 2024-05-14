## Описание проекта:
Проект представляет собой REST-сервис просмотра текущей зарплаты сотрудника
и даты следующего повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности,
реализован метод, где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.

## Стек технологий:
- Frontend: HTML, CSS, JavaScript
- Backend: FastApi, FastApi-users, PostgreSQL,
Alembic, SQLAlchemy, Uvicorn
- Тестирование: Pytest
- Управление зависимостями: Poetry
- CI/CD: Docker

## Установка зависимостей - Poetry:
В качестве инструмента управления зависимостями используется Poetry.
Все зависимости проекта отражены в файле **pyproject.toml.**  

Для установки Poetry выполните команду:  
`pip install poetry` 

Для добавления poetry в виртуальное окружение необходимо выполнить команду:  
`poetry init` 

Для установки всех зависимостей проекта необходимо выполнить команду:  
`poetry install` 

Все зависимости проекта будут установлены в ваше виртуальное окружение.

## Запуск проекта:
После установки всех зависимостей можно развернуть проект на локальной машине
или развернуть Docker Image.

### Развертывание на локальной машине:
После установки всех зависимостей проекта, необходимо запустить
программный сервер `uvicorn`.  
Для запуска сервера необходимо перейти в рабочую директорию проекта `src`.  
Для этого необходимо выполнить в терминале команду `cd src`.  
После этого запустить **uvicorn** `uvicorn main:app --reload`.  

Проект развернется на [локалхосте](http://127.0.0.1:8000/docs) и 
можно переходить к работе с эндпоинтами.

В проекте доступен графический интерфейс. Его подробное описание
ниже в пункте **"Frontend"**.  
Для запуска интерфейса пользователя можно открыть проект в 
**IDE VS Code**, установить плагин **Live Server**, 
перейти в директорию `Pages` и запустить файл `registration.html` 
через **Live Server**.

### Использование Docker:
Описание подробного запуска готового `docker-compose.yml` файла
вы найдете в пункте **"Работа с Docker"**.  
Содержимое `Dockerfile` представлено ниже.

```dockerfile
FROM python:3.12

RUN mkdir /fastapi_app  

WORKDIR /fastapi_app 
 
COPY pyproject.toml . 
 
RUN pip install poetry  

RUN poetry config virtualenvs.create false
  
RUN poetry install 

COPY . . 

RUN chmod a+x docker/*.sh  
```
Этот код позволяет нам взять за основу Docker Image python 3.12,
создать директорию `fastapi_app` и указать ее как рабочую.  
Далее копируем файл `pyproject.toml` в текущую директорию и 
устанавливаем зависимости с помощью `poetry`.  
Далее копируем файлы проекта в текущую рабочую директорию и 
даем разрешение на запуск всех файлов в директории `docker` с 
расширением **.sh** 

Файл `docker-compose.yml` необходим для описания запуска в контейнере
всех сервисов, использующихся в проекте. Содержимое файла `docker-compose.yml`:  

```dockerfile
version: "3.12"
services:
  db:
    image: postgres:15
    container_name: db_app
    command: -p 1221
    expose:
      - 1221
    env_file:
      - .env-non-dev

  app:
    build:
      context: .
    env_file:
      - .env-non-dev
    container_name: fastapi_app
    command: ["/fastapi_app/docker/app.sh"]
    ports:
      - 9999:8000
    depends_on:
      - db
```

В данном файле мы описываем два сервиса: сервис базы данных и сервис
нашего приложения.

При описании сервиса базы данных мы указываем название базового 
образа, название контейнера, номер порта и название файла 
переменных окружения.  

При описании сервиса нашего приложения мы указываем аналогичные 
параметры, а также зависимость текущего сервиса от сервиса 
базы данных `depends_on` и файл **bash-скрипта** для корректной 
работы зависимостей в контейнере `command: ["/fastapi_app/docker/app.sh"]`

## Frontend:
Для реализации frontend-части приложения используется
стек HTML, CSS, JS. Каждый компонент содержится в
соответствующей директории.  

- Pages  

Содержит HTML-страницы регистрации `registration.html`, 
авторизации `login.html` и личного кабинета `profile.html`
- Styles  

Содержит описание css-стилей страниц авторизации `login.css`, 
личного кабинета `profile.css`,
общие стили повторяющихся элементов `style.css`,
а также базовые стили приложения `base.css`, 
такие как сбросы отступов стандартных элементов и стили фона страниц.
- Scripts  

Содержит файлы `.js` для реализации логики взаимодействия 
пользователя с интерфейсом, а также запросов на Backend.  

Содержимое каждого `.js` файла `registration.js`,
`profile.js`, `login.js` можно свести к 3-м основным функциям:  
1. Получение данных с формы
2. Отправка данных формы на соответсвующий эндпоинт Backend
3. Рендеринг данных json-ответа от Backend
4. Реализации логики взаимодействия с кнопками

- Static 

Содержит статичный контент - фавиконку и 
картинку пользователя в личном кабинете.
## Backend:
Основными компонентами Backend являются база данных `PostgreSQL` и 
и приложение на фреймворке `FastApi`. Рассмотрим эти компоненты 
подробнее.  

### База данных и работа с миграциями - PostgreSQL, Alembic:

Для корректной работы с базой данных необходимо установить
PostgreSQL с официального **[сайта](https://www.postgresql.org/download/)**.  
Так как работа с базой данных у нас будет асинхронная, то в зависимостях
уже установлен модуль `asyncpg`.

За корректную работу с базой данных, создание БД, 
подключение к ней отвечают 3 файла конфигурации БД:  
- Файл `config.py` отвечает за импорт переменных из 
переменных окружения. Импортируем имя хоста, номер порта, 
имя БД, имя пользователя и пароль. Такой же импорт
произведен и для тестовой БД.
- Файл `env.py` в директории `migrations` отвечает за
конфигурацию Alembic, связке его с PostgreSQL, а также
получение метаданных. Alembic отвечает за контроль миграций, 
версии миграций хранятся в директории `migrations/versions`. При изменении конфигурации БД необходимо создать версию миграции. 
Для этого необходимо в терминале выполнить команду 
`alembic revision --autogenerate -m "your comment here"`.
Применить изменения последней миграции можно с помощью 
команды `alembic upgrade head`
- Файл `database.py` в директории `src` устанавливает 
соединение с созданной БД в PostgreSQL, создает переменную 
с метаданными и устанавливает асинхронную сессию с 
помощью `get_async_session`

### Работа с FastApi:
Основная работа с фреймворком `FastApi` происходит
в директории `src`. Файловая структура в этой директории
выглядит следующим образом:
```text
src                      # source root директория
│─── auth                # регистрации, авторизации пользователя
│     | base_config.py   # базовые настройки FastApi
│     | manager.py       # работа с UserManager
│     | models.py        # описание структуры БД, таблиц
│     | router.py        # описание роутинга и эндпоитов регистрации, авторизации
│     | schemas.py       # описание базовых классов валидации данных 
│     | utils.py         # функция получения пользователя из БД
│      
└─── user_profile        # личный кабинет пользователя
│     | router.py        # роутинг и эндпоит получения user по id
│     | utils.py         # получение user из БД по токену
│   
└───  __init__.py   
└───  config.py          # получение переменных окружения
└───  database.py        # подключение к БД, создание сессии
└───  main.py            # точка входа в приложение
```
Рассмотрим подробнее основные компоненты приложения `FastApi`.  

- `base_config.py`  
Для работы регистрации пользователя и работу с JWT- токеном 
была использована библиотека **fastapi-users**. Данная 
библиотека предполагает создание экземпляра класса **AuthenticationBackend**.
Именно для целей создания экземпляров класса **FastAPIUsers** и 
класса **AuthenticationBackend** предназначен данный файл.
- `models.py`
Файл предназначен для описания структуры таблиц базы данных. Так как мы 
используем **FastAPIUsers**, то наследуемся от базового класса **SQLAlchemyBaseUserTable**.
В связи с этим у пользователя появляются дополнительные поля 
**is_active**, **is_superuser**, **is_verified**. В файле описаны три основных
сущности: пользователи - **users**, токены - **tokens**, 
сотрудники - **employees**, так как показалось нецелесообразно хранить 
данные с логинами и паролями совместно с зарплатами и датой повышения в 
одной таблице.
- `auth/router.py`
Основная функция данного файла - описание эндпоинта авторизации
пользователя и создание соответствующего роутера. Рассмотрим подробнее
основную функцию **login_user**.
```python
async def login_user(user: UserLogin, session: AsyncSession = Depends(get_async_session)):

    query_user = (select(users).where(users.c.email == user.email)
                               .where(users.c.hashed_password != user.password))

    result = await session.execute(query_user)
    get_user = result.fetchone()
    if get_user:

        query_token = select(tokens).where(tokens.c.user_id == get_user[0])
        result = await session.execute(query_token)
        get_token = result.fetchone()

        if not get_token:
            token = str(uuid.uuid4())
            query_token = insert(tokens).values(user_id=get_user[0],
                                                access_token=token)
            await session.execute(query_token)
            await session.commit()

            return {
                "user_id": get_user[0],
                "token": token
                }

        else:
            return {
                "user_id": get_user[0],
                "token": get_token[1]
            }
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
```
В параметрах функции мы ожидаем пользователя, соответствующего схеме (классу)
UserLogin и сессию типа AsyncSession, которая зависит от функции get_async_session.
Находим пользователя в базе данных с введенными логином и паролем, если пользователь
найден, то проверяем наличие у него токена. В случае его отсутствия - формируем.
Если текущего пользователя нет с такими данными, то формируем исключение HTTP_401_UNAUTHORIZED.
- `schemas.py`
В текущем файле мы описываем основные типы данных пользователей, 
которые будем использовать при валидации данных.  

Чтение/получение пользователя по id.
```python
class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    surname: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
```
Создание пользователя.
```python
class UserCreate(schemas.BaseUserCreate):
    password: str
    name: str
    surname: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
```
Авторизация пользователя.
```python
class UserLogin(schemas.BaseUserCreate):
    email: str
    password: str
```
- `user_profile/router.py`
Основная функция данного файла - описание эндпоинта личного кабинета
сотрудника и создание соответствующего роутера. Рассмотрим подробнее
основную функцию **user_profile**.
```
async def user_profile(user_id: int, access_token: Annotated[str, Depends(apikey_scheme)],
                    session: AsyncSession = Depends(get_async_session)):
    return await get_user_by_token(user_id, access_token=access_token, session=session)
```
Функция принимает id сотрудника, сессию и токен. Вся логика
работы с этими данными вынесена в функцию **get_user_by_token**,
в которую прокидываем также id, сессию и токен. Подробнее о данной
функции ниже.
- `user_profile/utils.py`
В данном файле реализованы сценарии работы пользователя с личным
кабинетом. Пользователь может успешно войти в личный кабинет,
быть залогиненым, но попытаться войти не в свой личный кабинет и 
не быть залогиненым в приложение. Данную логику реализует функция
**get_user_by_token**. Функция **select_token_by_access_token_from_db**
является вспомогательной и реализует логику поиска токена сотрудника
в БД. Рассмотрим подробнее основную функцию:  
```python
async def get_user_by_token(user_id: int, access_token:  str,
                            session: AsyncSession = Depends(get_async_session)):
    selected_token = await select_token_by_access_token_from_db(access_token, session)

    query_employee = select(employees)
    result = await session.execute(query_employee)
    get_employee = result.fetchall()

    if selected_token:
        if not any([selected_token[-1] == employee[1] for employee in get_employee]):
            stmt = insert(employees).values(id=get_employee[-1][0] + 1 if get_employee else 1,
                                            id_user=selected_token[-1],
                                            salary=random.randint(50000, 150000),
                                            next_grade_in=datetime.now() + timedelta(weeks=8))
            await session.execute(stmt)
            await session.commit()

    if selected_token:
        if selected_token[-1] == user_id:

            query_employee = select(employees).where(employees.c.id_user == selected_token[-1])
            result = await session.execute(query_employee)
            get_employee = result.first()

            if get_employee:
                query_user = select(users).where(users.c.id == selected_token[-1])
                result = await session.execute(query_user)
                get_user = result.fetchone()

                return {
                    "Salary": get_employee[-2],
                    "Next_grade_data": get_employee[-1],
                    "name": get_user[-1],
                    "surname": get_user[-2],
                    "email": get_user[1]
                }

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="FORBIDDEN"
        )
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
```
В первую очередь, с помощью вспомогательной функции производим поиск токена в БД.
Далее получает сотрудников из БД. Производим поиск сотрудника 
с текущим токеном. Если такого сотрудника не находим, то это означает, 
что у нас есть пользователь, у него есть токен, в список сотрудников
этот пользователь пока не переведен и у него нет данных по зарплате
и повышению. Добавляем эти данные.  
Далее производим поиск сотрудника по id, для получения данных
о зарплате и повышению. Если такой сотрудник найден и его id 
соответствует его токену, то возвращаем JSON-объект с данными
о Зарплате - **Salary**, Даты повышения - **Next_grade_data**,
Имени - **name**, Фамилии - **surname**, Логина/почты - **email**
- `main.py`
Файл является точкой входа в приложение, где мы создаем экземпляр
нашего приложения на **FastApi**, инициализируем все роутеры через
include_router и инициализируем **Middleware** для работы с 
CORS и успешной связки нашего frontend и backend.

## Переменные окружения и файлы конфигурации:
Для корректной работы приложения в проекте присутствуют файлы
конфигурации и переменные окружения:  
- Файл `app.sh` в директории docker необходим корректной работы зависимостей
**Alembic** и **guvicorn** в docker-контейнере
- Файл `.env` для работы с переменными окружения при разработке
- Файл `.env-non-dev` для работы с переменными окружения при развертывании Docker-контейнера

## Тестирование проекта - Pytest:
Тестирование проекта происходит с использованием библиотеки
Pytest, а именно его асинхронного варианта pytest-asyncio.  
Тесты хранятся в директории test. Для тестирования базы данных и 
эндпоинтов была создана тестовая база данных.  

Файл **`conftest.py`** отвечает за следующее:  
- Подключение с тестовой БД
- Переписывание зависимостей `override_get_async_session`
- Создание таблиц и данных в БД и ее очистка по
завершению тестов `prepare_database`
- Создание асинхронного Тестового Клиента  

В файле **`test_db.py`** располагаются тесты БД и эндпоинтов:  
- Тест на добавление пользователя в БД `test_add_user`
- Тест на добавление токена в БД `test_add_token`
- Тест на успешный вход зарегистрированного пользователя `test_api_login_success`
- Тест на ошибку входа незарегистрированного пользователя `test_api_login_failed`
- Тест на корректный просмотр данных пользователем с
соответсвующий id `test_api_profile_success`
- Тест на запрет просмотра данных пользователем с
несоответствующим id `test_api_profile_failed`

## Работа с Docker:
Для корректной работы с Docker необходимо установить
Docker Desktop с официального **[сайта](https://www.docker.com/products/docker-desktop/)**.  

Файл `Dockerfile` описывает приложение на FastApi.  
Файл `Docker-compose.yml` описывает сборку необходимых
сервисов для корректной работы с приложением,
включая базу данных.  

Для развертывания образа необходимо:
1. Запустить Docker Desktop
2. В терминале выполнить команду `docker compose build`
3. В терминале выполнить команду `docker compose up`
4. Перейти в Docker Desktop для просмотра корректности работы контейнеров

