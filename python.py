

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime


# Строка подключения
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# Базовый класс БД
Base = declarative_base()


class Athlete(Base):
    """
        Описывает структуру таблицы athletes для хранения записей данных атлетов
    """

    # Название таблицы
    __tablename__ = "athelete"

    # Индентификатор
    id = sa.Column(sa.INTEGER, primary_key = True)
    # Возраст
    age = sa.Column(sa.INTEGER)
    # Дата рождения
    birthdate = sa.Column(sa.TEXT)
    # Пол
    gender = sa.Column(sa.TEXT)
    # Рост
    height = sa.Column(sa.REAL)
    # ФИО
    name = sa.Column(sa.TEXT)
    # Вес
    weight = sa.Column(sa.INTEGER)
    # Золотые медали
    gold_medals = sa.Column(sa.INTEGER)
    # Серебрянные медали
    silver_medals = sa.Column(sa.INTEGER)
    # Бронзовые медали
    bronze_medals = sa.Column(sa.INTEGER)
    # Общее кол-во медалей
    total_medals = sa.Column(sa.INTEGER)
    # Вид спорта
    sport = sa.Column(sa.TEXT)
    # Страна
    country = sa.Column(sa.TEXT)


class User(Base):
    """
        Описывает структуру таблицы user для хранения записей данных пользователей
    """

    # Название таблицы
    __tablename__ = "user"

    # Идентификатор
    id = sa.Column(sa.INTEGER, primary_key = True)
    # Имя
    first_name = sa.Column(sa.TEXT)
    # Фамилия
    last_name = sa.Column(sa.TEXT)
    # Пол
    gender = sa.Column(sa.TEXT)
    # Адрес электронной почты
    email = sa.Column(sa.TEXT)
    # Дата рождения
    birthdate = sa.Column(sa.TEXT)
    # Рост
    height = sa.Column(sa.REAL)


def connect_db():
    """
        Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение с БД
    engine = sa.create_engine(DB_PATH)
    # создаем фабрику сессию
    session = sessionmaker(engine)

    # Возвращаем сессию
    return session()


def convert_time(birthdate):
    """
        Получаем из строки объект datetime.date
    """

    # Сплитим строку по "-"
    birthdate_list = birthdate.split("-")
    # Конвертируем строки в числа
    date_list = map(int, birthdate_list)

    # Возвращаем оьъект даты
    return datetime.date(*date_list)


def request_data():
    """
        Запрашивает уникальный идентификатор пользователя для поиска и возвращает его
    """

    print("Для теста введи 1 или 2")

    # Сбор данных
    id = input("Введи id пользователя для поиска: ")

    # Возвращает id
    return int(id)


def find_nearest_birthdate(user, session):
    """
        Поиск ближайшего атлета по дате рождения
    """

    # Получаем список всех атлетов
    athletes = session.query(Athlete).all()
    # Словарь для хранения id и даты рождения
    athletes_birthdates = {}

    # Заполняем словарь
    for athlete in athletes:
        # Получаем из строки объект даты
        birthdate = convert_time(athlete.birthdate)
        athletes_birthdates[athlete.id] = birthdate

    # Дата рождения пользователя
    user_birthdate = convert_time(user.birthdate)
    # Минимальная разница
    nearest_date = None
    # ID ближайшего атлета
    nearest_id = None

    for key, value in athletes_birthdates.items():
        # Считаем очередную разницу
        dist = abs(user_birthdate - value)
        if not nearest_date or dist < nearest_date:
            nearest_date = dist
            nearest_id = key

    # Возвращаем id нужного атлета
    return nearest_id

def find_nearest_height(user, session):
    """
        Поиск ближайшего атлета по дате рождения
    """

    # Получаем список всех атлетов у которых записан рост
    athletes = session.query(Athlete).filter(Athlete.height != None).all()
    # Заполняем словарь для хранения id и роста
    athletes_heights = {athlete.id:athlete.height for athlete in athletes}

    # Рост пользвоателя
    user_height = user.height

    # Минимальная разница
    nearest_height = None
    # ID ближайшего атлета
    nearest_id = None

    for key, value in athletes_heights.items():
        if value is None:
            continue

        # Считаем очередную разницу
        dist = abs(user_height - value)
        if not nearest_height or dist < nearest_height:
            nearest_height = dist
            nearest_id = key

    # Возвращаем id нужного атлета
    return nearest_id

def main():
    session = connect_db()
    user_id = request_data()

    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        print("Такого пользователя нет!")
    else:
        athlete_bd_id = find_nearest_birthdate(user, session)
        athlete_bd = session.query(Athlete).filter(Athlete.id == athlete_bd_id).first()

        athlete_height_id = find_nearest_height(user, session)
        athlete_height = session.query(Athlete).filter(Athlete.id == athlete_height_id).first()

        print("Ближайший к вам атлет по дате рождения:")
        print("Уникальный индентификатор: {}\nВозраст: {}\nДень рождения: {}\nФИО: {}\nСпорт: {}\nСтрана: {}".format(
                athlete_bd.id,
                athlete_bd.age,
                athlete_bd.birthdate,
                athlete_bd.name,
                athlete_bd.sport,
                athlete_bd.country)
             )
        print("Ближайший к вам атлет по росту:")
        print("Уникальный индентификатор: {}\nВозраст: {}\nДень рождения: {}\nФИО: {}\nРост: {}\nСпорт: {}\nСтрана: {}".format(
                athlete_height.id,
                athlete_height.age,
                athlete_height.birthdate,
                athlete_height.name,
                athlete_height.height,
                athlete_height.sport,
                athlete_height.country)
             )


if __name__ == "__main__":
        main()
