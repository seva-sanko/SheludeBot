import sqlite3

def create_tables():
    try:
        # Подключение к SQLite (файл students.db будет создан, если его нет)
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        print("Successful connection!")
        print("#" * 20)

        # SQL-запросы для создания таблиц
        sql_queries = [
            """-- Таблица "institute" (Институты)
CREATE TABLE IF NOT EXISTS institute (
    id_institute INTEGER PRIMARY KEY AUTOINCREMENT,
    Institute TEXT NOT NULL
);""",
            """-- Таблица "fuclty" (Факультеты)
CREATE TABLE IF NOT EXISTS fuclty (
    id_fuclty INTEGER PRIMARY KEY AUTOINCREMENT,
    Fuclty TEXT NOT NULL,
    id_institute INTEGER,
    FOREIGN KEY (id_institute) REFERENCES institute(id_institute)
);""",
            """-- Таблица "education" (Формы обучения)
CREATE TABLE IF NOT EXISTS education (
    id_education INTEGER PRIMARY KEY AUTOINCREMENT,
    Education TEXT NOT NULL
);""",
            """-- Таблица "study_group" (Учебные группы)
CREATE TABLE IF NOT EXISTS study_group (
    id_study_group INTEGER PRIMARY KEY AUTOINCREMENT,
    Study_group TEXT NOT NULL,
    url TEXT
);""",
            """-- Таблица "student" (Студенты)
CREATE TABLE IF NOT EXISTS student (
    id_student INTEGER PRIMARY KEY AUTOINCREMENT,
    Student TEXT NOT NULL,
    id_study_group INTEGER,
    id_fuclty INTEGER,
    id_institute INTEGER,
    id_education INTEGER,
    course INTEGER,
    FOREIGN KEY (id_study_group) REFERENCES study_group(id_study_group),
    FOREIGN KEY (id_fuclty) REFERENCES fuclty(id_fuclty),
    FOREIGN KEY (id_institute) REFERENCES institute(id_institute),
    FOREIGN KEY (id_education) REFERENCES education(id_education)
);""",
            """-- Таблица "lesson" (Предметы)
CREATE TABLE IF NOT EXISTS lesson (
    id_lesson INTEGER PRIMARY KEY AUTOINCREMENT,
    Lesson TEXT NOT NULL UNIQUE
);""",
            """-- Таблица "schedule_list" (Расписание)
CREATE TABLE IF NOT EXISTS schedule_list (
    id_schedule_list INTEGER PRIMARY KEY AUTOINCREMENT,
    id_lesson INTEGER,
    id_study_group INTEGER,
    id_student INTEGER,
    lesson_date DATE,
    FOREIGN KEY (id_lesson) REFERENCES lesson(id_lesson),
    FOREIGN KEY (id_study_group) REFERENCES study_group(id_study_group),
    FOREIGN KEY (id_student) REFERENCES student(id_student)
);""",
            """-- Таблица "spot" (Места проведения занятий)
CREATE TABLE IF NOT EXISTS spot (
    id_spot INTEGER PRIMARY KEY AUTOINCREMENT,
    Spot TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);"""
        ]

        # Выполнение каждого SQL-запроса
        for query in sql_queries:
            cursor.execute(query)
            print(f"Executed: {query.split()[3]}")  # Вывод имени таблицы

        # Сохранение изменений
        connection.commit()
        print("All tables created successfully!")

    except Exception as ex:
        print("Connection failed...")
        print(ex)

    finally:
        # Закрытие соединения
        if connection:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    create_tables()