# Questions
[![codecov](https://codecov.io/gh/MaksimBoltov/questions-for-quiz/branch/main/graph/badge.svg?token=UQJ0T5UYZI&style=plastic)](https://codecov.io/gh/MaksimBoltov/questions-for-quiz)

#### Краткое описание:
Проект предоставляет один простой интерфейс для добавления комментариев в базу данных.

#### Стэк технологий:
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy, Alembic
- Docker
____
#### Запуск и использование
Для работы проекта необходим Python версии 3.9 или выше (в случае отсутствия установить с [официального сайта](https://www.python.org/downloads)). \
База данных запускается в docker-контейнере, а веб-сервер отдельно для доступа к [внешнему ресурсу](https://jservice.io/api/random?count=). \
Для запуска проекта необходимо:
1. Установить виртуальное окружение в директории проекта. Для этого в терминале необходимо ввести:
    ```shell script
    python3 -m venv myenv
    ```
2. Активировать созданное виртуальное окружение:
    ```shell script
    source myenv/bin/activate
    ```
3. Установить дополнительные зависимости:
    ```shell script
    pip install -r requirements.txt
    ```
4. Добавить переменные окружения для базы данных в файл _.env_ (в переменной _VOLUMES_PATH_ указать путь для сохранения состояния базы данных).
5. Запустить контейнер с базой данных (флаг -d для запуска в фоновом режиме):
    ```shell script
    docker-compose up -d
    ```
6. Применить миграции к базе данных:
    ```shell script
    make migrate
    ```
7. Запустить сервер uvicorn:
    ```shell script
    make runserver
    ```
После этого сервер будет доступен по адресу http://127.0.0.1:8000 \
Для просмотра документации после запуска и ознакомления с функционалом:\
http://127.0.0.1:8000/docs \
Для запуска тестов:
```shell script
pytest tests/
```
___
#### Примеры запросов и ответов
POST http://127.0.0.1:8000/questions - для добавления вопросов в базу данных \
Тело запроса:
```json
{
    "questions_num": int
}
```
В качестве допустимых значений для _questions_num_ определены положительные целые числа и 0 (0 выбран для совместимости с [внешним сервисом](https://jservice.io/api/random?count=0)). \
Далее будут рассмотрены варианты запросов к сервису с различными значениями _questions_num_:
1. _questions_num_ целое положительное число (_questions_num_ > 0). Для чисел больше нуля сервер запрашивает у [внешнего сервиса](https://jservice.io/api/random?count=) вопросы для викторины в количестве _questions_num_ и в случае уникальности (если вопрос с указанным id уже существует в базе данных, будет выполнен запрос новых вопросов) добавляет их в базу данных, после чего возвращает в качестве ответа последний добавленный в базу данных вопрос (пример для num = 5): \
    Запрос:
    ```json
    {
        "questions_num": 5
    }
    ```
    Ответ: \
    ![Пример для q == 5](https://github.com/MaksimBoltov/questions-for-quiz/raw/main/docs/screenshots/q_5.png)
2. _questions_num_ равно нулю (_questions_num_ = 0). Если переданный _questions_num_ равен 0, то сервер отдаёт пустой json: \
    Запрос:
    ```json
    {
        "questions_num": 0
    }
    ```
    Ответ: \
    ![Пример для q == 0](https://github.com/MaksimBoltov/questions-for-quiz/raw/main/docs/screenshots/q_0.png)
3. _questions_num_ целое отрицательное число (_questions_num_ < 0). Данные значения не проходят валидацию и выдается сообщение об ошибке в формате: \
    Запрос:
    ```json
    {
        "questions_num": -1
    }
    ```
    Ответ: \
    ![Пример для q == -1](https://github.com/MaksimBoltov/questions-for-quiz/raw/main/docs/screenshots/q_-1.png)
4. _questions_num_ любое не целочисленное значение. Данные не пройдут валидацию и будет выдано сообщение об ошибке (при этом строка, содержащая целочисленное значение валидацию пройдет): \
    Запрос:
    ```json
    {
        "questions_num": "text"
    }
    ```
    Ответ: \
    ![Пример для q == "text"](https://github.com/MaksimBoltov/questions-for-quiz/raw/main/docs/screenshots/q_text.png)
5. В случае отсутствия _questions_num_ в теле запроса выдается ошибка: \
    ![question_num отсутствует](https://github.com/MaksimBoltov/questions-for-quiz/raw/main/docs/screenshots/field_required.png)

6. В случае, если внешний сервис не доступен или отсутствует подключение к Интернету у сервера, выдается следующий ответ: \
    ![Подключение отсутствует](https://github.com/MaksimBoltov/questions-for-quiz/raw/main/docs/screenshots/409.png)
