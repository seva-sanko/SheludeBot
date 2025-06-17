import sqlite3
import traceback
import os
from pathlib import Path

# --- НАЧАЛО БЛОКА ОПРЕДЕЛЕНИЯ ПУТИ И ОТЛАДКИ ---

# requests.py находится в /Users/Seva/Polytech/tgBot/SheduleBot/database/requests.py
# Нам нужно подняться на ОДИН УРОВЕНЬ ВВЕРХ от местоположения requests.py, чтобы попасть в корень проекта.
# Path(__file__).resolve() -> /Users/Seva/Polytech/tgBot/SheduleBot/database/requests.py
# Path(__file__).resolve().parent -> /Users/Seva/Polytech/tgBot/SheduleBot/database (папка, где лежит requests.py)
# Path(__file__).resolve().parent.parent -> /Users/Seva/Polytech/tgBot/SheduleBot (КОРЕНЬ ПРОЕКТА)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Строим путь к БД: корень_проекта / "database" / "DataBase.db"
# Папка "database" для БД находится в корне проекта, а не внутри другой папки "database".
dataBasePath_calculated = str(PROJECT_ROOT / "database" / "DataBase.db")

# Отладочный вывод (выполнится один раз при импорте этого модуля)
print(f"--- DEBUG: requests.py (initialization) ---")
print(f"Current working directory (CWD): {os.getcwd()}")
print(f"Absolute path of this file (requests.py): {Path(__file__).resolve()}")
print(f"Calculated PROJECT_ROOT: {PROJECT_ROOT}") # Должен быть /Users/Seva/Polytech/tgBot/SheduleBot
print(f"Calculated dataBasePath to be used: {dataBasePath_calculated}") # Должен быть /Users/Seva/Polytech/tgBot/SheduleBot/database/DataBase.db
print(f"Does DB file exist at calculated path? {Path(dataBasePath_calculated).exists()}")
print(f"--- END DEBUG ---")

# Используем вычисленный путь для всех операций с БД
dataBasePath = dataBasePath_calculated
# --- КОНЕЦ БЛОКА ОПРЕДЕЛЕНИЯ ПУТИ И ОТЛАДКИ ---


def _execute_query(query, params=None, fetch_one=False, fetch_all=False, is_insert_or_delete=False,
                   func_name="<unknown>"):
    """Вспомогательная функция для выполнения SQL-запросов с общей обработкой ошибок."""
    result = None
    connection = None
    cursor = None  # Объявим курсор здесь, чтобы иметь к нему доступ для закрытия, хотя это не обязательно для sqlite3
    try:
        print(f"--- DEBUG: Attempting to connect in function '{func_name}' with dataBasePath: {dataBasePath} ---")
        connection = sqlite3.connect(dataBasePath)
        connection.row_factory = sqlite3.Row
        print(f"Successful connection! (func: {func_name})")
        print("#" * 20)

        cursor = connection.cursor()  # Просто создаем курсор
        cursor.execute(query, params or ())

        if is_insert_or_delete:
            connection.commit()
            print(f"Committed changes. (func: {func_name})")
        elif fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()

        # Курсор sqlite3 не требует явного закрытия, он закроется вместе с соединением.
        # Но если бы требовал, можно было бы cursor.close() здесь.

    except sqlite3.Error as db_err:
        print(f"!!! SQLite error in {func_name} !!!")
        print(f"  Query: {query}")
        print(f"  Params: {params}")
        print(f"  Type: {type(db_err)}")
        print(f"  Args: {db_err.args}")
        print(f"  String: {str(db_err)}")
        print("  --- Traceback START ---")
        traceback.print_exc()  # Надеюсь, теперь сработает
        print("  --- Traceback END ---")
    except Exception as ex:
        print(f"!!! Generic error in {func_name} !!!")
        print(f"  Query: {query}")
        print(f"  Params: {params}")
        print(f"  Type: {type(ex)}")
        print(f"  Args: {ex.args}")
        print(f"  String: {str(ex)}")
        print("  --- Traceback START ---")
        traceback.print_exc()  # Надеюсь, теперь сработает
        print("  --- Traceback END ---")
    finally:
        if connection:  # Соединение закрываем всегда
            connection.close()
            print(f"Connection closed. (func: {func_name})")
    return result

def get_institute(education):
    print(f"get_institute called with education: {education}")
    sql = """
        SELECT DISTINCT institute.id_institute, institute.Institute
        FROM student
        JOIN education ON education.id_education = student.id_education 
        JOIN institute ON institute.id_institute = student.id_institute
        JOIN study_group ON student.id_study_group = study_group.id_study_group 
        WHERE education.Education = ?
        AND institute.Institute LIKE '%нститут%'
        --AND study_group.Study_group NOT LIKE '%з%' 
        --AND study_group.Study_group NOT LIKE '%в%'
        ORDER BY institute.Institute;
    """
    institutes = _execute_query(sql, (education,), fetch_all=True, func_name="get_institute")
    print(f"Результат запроса get_institute: {institutes}")
    return institutes if institutes else []


def get_groups(fuclty_id, course, education_name_param): # education - это НАЗВАНИЕ формы
    print(f"get_groups called with fuclty_id: {fuclty_id}, course: {course}, education_name_param: '{education_name_param}'") # Уже должно быть
    sql = """
        SELECT DISTINCT sg.Study_group, sg.id_study_group
        FROM student s
        JOIN study_group sg ON s.id_study_group = sg.id_study_group 
        JOIN education e ON s.id_education = e.id_education 
        WHERE s.course = ?          -- course (число)
        AND s.id_fuclty = ?       -- fuclty_id (число)
        AND e.Education = ?       -- education_name_param (строка, например "Бакалавриат")
        --AND sg.Study_group NOT LIKE '%з%' AND sg.Study_group NOT LIKE '%в%'
        ORDER BY sg.Study_group;
    """
    # _execute_query ожидает кортеж параметров
    groups = _execute_query(sql, (course, fuclty_id, education_name_param), fetch_all=True, func_name="get_groups")
    print(f"Результат запроса get_groups: {groups}") # Дополнительный print
    return groups if groups else []


def get_fuclty(institute_id, education):  # Изменил institute на institute_id
    print(f"get_fuclty called with institute_id: {institute_id}, education: {education}")
    sql = """
        SELECT DISTINCT f.Fuclty, f.id_fuclty
        FROM student s
        JOIN fuclty f ON s.id_fuclty = f.id_fuclty
        JOIN education e ON s.id_education = e.id_education 
        JOIN study_group sg ON s.id_study_group = sg.id_study_group 
        WHERE s.id_institute = ?
        AND e.Education = ?
        --AND sg.Study_group NOT LIKE '%з%' AND sg.Study_group NOT LIKE '%в%'
        ORDER BY f.Fuclty;
    """
    faculties = _execute_query(sql, (institute_id, education), fetch_all=True,
                               func_name="get_fuclty")  # Переименовал groups в faculties
    return faculties if faculties else []


def get_institute_from_id(id_institute):
    print(f"get_institute_from_id called with id_institute: {id_institute}")
    sql = "SELECT Institute FROM institute WHERE id_institute = ?;"  # DISTINCT не нужен при поиске по PK
    row = _execute_query(sql, (id_institute,), fetch_one=True, func_name="get_institute_from_id")
    return row["Institute"] if row else None


def get_fuclty_from_id(id_fuclty):
    print(f"get_fuclty_from_id called with id_fuclty: {id_fuclty}")
    sql = "SELECT Fuclty FROM fuclty WHERE id_fuclty = ?;"  # DISTINCT не нужен
    row = _execute_query(sql, (id_fuclty,), fetch_one=True, func_name="get_fuclty_from_id")
    return row["Fuclty"] if row else None


def get_study_group_from_id(id_study_group):
    print(f"get_study_group_from_id called with id_study_group: {id_study_group}")
    sql = "SELECT Study_group FROM study_group WHERE id_study_group = ?;"  # DISTINCT не нужен
    row = _execute_query(sql, (id_study_group,), fetch_one=True, func_name="get_study_group_from_id")
    return row["Study_group"] if row else None


def get_student_from_id(id_student):
    print(f"get_student_from_id called with id_student: {id_student}")
    sql = "SELECT Student FROM student WHERE id_student = ?;"  # DISTINCT не нужен
    row = _execute_query(sql, (id_student,), fetch_one=True, func_name="get_student_from_id")
    return row["Student"] if row else None


def get_student(id_study_group):  # Изменил group на id_study_group
    print(f"get_student called with id_study_group: {id_study_group}")
    sql = """
        SELECT DISTINCT s.Student, s.id_student
        FROM student s
        WHERE s.id_study_group = ?
        ORDER BY s.Student;
    """
    students = _execute_query(sql, (id_study_group,), fetch_all=True, func_name="get_student")
    return students if students else []


def get_schedule_url(group_id):
    print(f"get_schedule_url called with group_id: {group_id}")
    sql = "SELECT url FROM study_group WHERE id_study_group = ?;"
    row = _execute_query(sql, (group_id,), fetch_one=True, func_name="get_schedule_url")
    return row["url"] if row else None


def get_geo(spot_name):  # Изменил spot на spot_name
    print(f"get_geo called with spot_name: {spot_name}")
    sql = "SELECT latitude, longitude FROM spot WHERE Spot = ?;"
    row = _execute_query(sql, (spot_name,), fetch_one=True, func_name="get_geo")
    return [row["latitude"], row["longitude"]] if row else None


def insert_lesson(lesson_name, group_id, student_id, year, month, day):
    connection = None
    inserted_successfully = False  # Флаг для реальной вставки
    already_exists = False  # Флаг, если запись уже была

    try:
        # Увеличиваем таймаут для соединений, как обсуждали ранее
        connection = sqlite3.connect(dataBasePath, timeout=10.0)
        connection.execute("PRAGMA foreign_keys = ON;")  # Включаем проверку внешних ключей
        connection.execute("PRAGMA journal_mode = WAL;")  # Рекомендуется
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        # 1. Получить или создать id_lesson
        cursor.execute("INSERT OR IGNORE INTO lesson (Lesson) VALUES (?);", (lesson_name,))
        # Не нужен commit здесь, если все в одной транзакции

        cursor.execute("SELECT id_lesson FROM lesson WHERE Lesson = ?;", (lesson_name,))
        lesson_row = cursor.fetchone()
        if not lesson_row:
            print(f"!!! КРИТИЧЕСКАЯ ОШИБКА: Не удалось получить/создать id_lesson для '{lesson_name}'")
            return False  # Явный выход при критической ошибке
        id_lesson = lesson_row["id_lesson"]

        lesson_date = f"{year}-{month:02d}-{day:02d}"

        # 2. Сначала проверим, существует ли уже такая запись
        check_sql = """
            SELECT 1 FROM schedule_list 
            WHERE id_lesson = ? AND id_study_group = ? AND id_student = ? AND lesson_date = ?;
        """
        cursor.execute(check_sql, (id_lesson, group_id, student_id, lesson_date))
        existing_record = cursor.fetchone()

        if existing_record:
            already_exists = True
            print(
                f"Запись для студента {student_id} на предмет '{lesson_name}' ({id_lesson}) на {lesson_date} уже существует.")
        else:
            # 3. Если записи нет, пытаемся вставить
            schedule_insert_sql = """
                INSERT INTO schedule_list 
                (id_lesson, id_study_group, id_student, lesson_date) 
                VALUES (?, ?, ?, ?);
            """
            # Используем просто INSERT, так как уже проверили на существование.
            # Если есть UNIQUE constraint на (id_lesson, id_study_group, id_student, lesson_date),
            # то INSERT OR IGNORE все еще безопасен, но проверка выше дает больше контроля.
            cursor.execute(schedule_insert_sql, (id_lesson, group_id, student_id, lesson_date))

            if cursor.rowcount > 0:  # rowcount покажет, сколько строк было изменено (вставлено)
                inserted_successfully = True
                print(f"Успешно вставлена запись: Студент {student_id}, Предмет '{lesson_name}', Дата {lesson_date}")
            else:
                # Этого не должно произойти, если проверка на existing_record была, а INSERT не сработал без ошибки
                print(f"!!! ПРЕДУПРЕЖДЕНИЕ: INSERT в schedule_list не изменил строки, но и ошибки не было.")

        connection.commit()  # Коммитим изменения

    except sqlite3.Error as db_err:
        print(f"!!! SQLite ошибка в insert_lesson для '{lesson_name}', студент {student_id} !!!")
        print(f"  Тип: {type(db_err)}, Аргументы: {db_err.args}, Строка: {str(db_err)}")
        if connection:
            connection.rollback()  # Откатываем транзакцию при ошибке
        # inserted_successfully останется False
    except Exception as ex:
        print(f"!!! Общая ошибка в insert_lesson для '{lesson_name}', студент {student_id} !!!")
        print(f"  Тип: {type(ex)}, Аргументы: {ex.args}, Строка: {str(ex)}")
        if connection:
            connection.rollback()
        # inserted_successfully останется False
    finally:
        if connection:
            connection.close()
            print(f"Соединение закрыто (func: insert_lesson)")

    # Теперь функция возвращает True только если была успешная НОВАЯ вставка
    # Если вы хотите, чтобы бот сообщал "Вы уже отмечены", то нужно будет
    # либо возвращать специальное значение из insert_lesson (например, строку "already_exists"),
    # либо оставить как есть, и сообщение "Возможно, вы уже отмечены" будет корректным.
    return inserted_successfully


def get_lessons(group_id):
    print(f"--- DEBUG: bd.get_lessons (group_id: {group_id}) ---")
    lessons_list = []
    connection = None
    cursor = None  # Объявим здесь, хотя для sqlite3 это не так критично
    try:
        # print(f"--- DEBUG: Attempting to connect in function 'get_lessons' with dataBasePath: {dataBasePath} ---")
        connection = sqlite3.connect(dataBasePath)
        connection.row_factory = sqlite3.Row
        # print(f"Successful connection! (func: get_lessons)")
        # print("#" * 20)

        cursor = connection.cursor()  # Просто создаем курсор БЕЗ with

        cursor.execute("SELECT DISTINCT id_lesson FROM schedule_list WHERE id_study_group = ?;", (group_id,))
        id_lesson_rows = cursor.fetchall()
        print(f"  id_lesson_rows: {id_lesson_rows}")

        for id_row in id_lesson_rows:
            id_lesson_val = id_row["id_lesson"]  # Получаем значение из Row объекта
            cursor.execute("SELECT Lesson FROM lesson WHERE id_lesson = ?;", (id_lesson_val,))
            lesson_row = cursor.fetchone()
            print(f"  Для id_lesson {id_lesson_val}, найдено lesson_row: {lesson_row}")
            if lesson_row and lesson_row["Lesson"]:
                lessons_list.append(lesson_row["Lesson"])
            else:
                print(f"  ПРЕДУПРЕЖДЕНИЕ: Для id_lesson {id_lesson_val} не найдено название или оно пустое.")

        print(f"  Возвращаемый список уроков: {lessons_list}")

    except sqlite3.Error as db_err:
        print(f"!!! SQLite error in get_lessons !!!")
        print(f"  Type: {type(db_err)}")
        print(f"  Args: {db_err.args}")
        print(f"  String: {str(db_err)}")
        traceback.print_exc()
    except Exception as ex:
        print(f"!!! Generic error in get_lessons !!!")
        print(f"  Type: {type(ex)}")
        print(f"  Args: {ex.args}")
        print(f"  String: {str(ex)}")
        traceback.print_exc()
    finally:
        # Курсор sqlite3 не требует явного закрытия, он закроется вместе с соединением.
        if connection:
            connection.close()
            # print(f"Connection closed. (func: get_lessons)")
    return lessons_list


def get_lesson_dates(lesson_name, group_id, date_start_str):
    print(f"--- DEBUG: bd.get_lesson_dates (lesson_name: '{lesson_name}', group_id: {group_id}, date_start_str: '{date_start_str}') ---")
    dates_list = ["Студент"]
    connection = None
    try:
        connection = sqlite3.connect(dataBasePath)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT id_lesson FROM lesson WHERE Lesson = ?;", (lesson_name,))
        lesson_id_row = cursor.fetchone()
        print(f"  Для lesson_name '{lesson_name}', найдено lesson_id_row: {lesson_id_row}")

        if not lesson_id_row:
            print(f"  ПРЕДУПРЕЖДЕНИЕ: Предмет '{lesson_name}' не найден в таблице lesson.")
            return dates_list

        id_lesson = lesson_id_row["id_lesson"]
        sql = """
            SELECT DISTINCT lesson_date 
            FROM schedule_list 
            WHERE id_study_group = ? 
            AND id_lesson = ? 
            AND lesson_date >= ?  -- ИЗМЕНЕНО НА >= для включения начальной даты, если нужно
            ORDER BY lesson_date ASC; 
        """ # Можно вернуть > если не нужно включать начальную дату
        print(f"  Выполняется SQL для дат: params=({group_id}, {id_lesson}, '{date_start_str}')")
        cursor.execute(sql, (group_id, id_lesson, date_start_str))
        lesson_date_rows = cursor.fetchall()
        print(f"  Найденные lesson_date_rows: {lesson_date_rows}")

        for date_row in lesson_date_rows:
            parts = date_row['lesson_date'].split('-')
            if len(parts) == 3:
                date_normal = f"{parts[2]}.{parts[1]}.{parts[0]}"
                dates_list.append(date_normal)
            else:
                print(f"  ПРЕДУПРЕЖДЕНИЕ: Неверный формат даты '{date_row['lesson_date']}' из БД.")
        print(f"  Возвращаемый список дат (с заголовком): {dates_list}")

    except sqlite3.Error as db_err:  # ... (обработка ошибок как выше) ...
        print(f"!!! SQLite error in get_lesson_dates !!!")
        traceback.print_exc()
    except Exception as ex:  # ... (обработка ошибок как выше) ...
        print(f"!!! Generic error in get_lesson_dates !!!")
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            print(f"Connection closed. (func: get_lesson_dates)")
    return dates_list


def get_student_list(dates_dd_mm_yyyy, group_id, lesson_name):  # Изменил names
    print(f"get_student_list called with group_id: {group_id}, lesson_name: {lesson_name}")
    students_attendance = []
    connection = None
    try:
        print(f"--- DEBUG: Attempting to connect in function 'get_student_list' with dataBasePath: {dataBasePath} ---")
        connection = sqlite3.connect(dataBasePath)
        connection.row_factory = sqlite3.Row
        print(f"Successful connection! (func: get_student_list)")
        print("#" * 20)

        with connection.cursor() as cursor:
            cursor.execute("SELECT id_lesson FROM lesson WHERE Lesson = ?;", (lesson_name,))
            id_lesson_row = cursor.fetchone()
            if not id_lesson_row:
                print(f"Lesson '{lesson_name}' not found for student list.")
                return []
            id_lesson = id_lesson_row["id_lesson"]

            cursor.execute("SELECT Student, id_student FROM student WHERE id_study_group = ? ORDER BY Student ASC;",
                           (group_id,))
            students_in_group = cursor.fetchall()

            for student_row in students_in_group:
                student_record = [student_row["Student"]]  # [ИмяСтудента]
                id_student = student_row["id_student"]

                for date_str_dd_mm_yyyy in dates_dd_mm_yyyy:
                    if date_str_dd_mm_yyyy == "Студент":  # Пропускаем заголовок
                        continue
                    # Преобразование DD.MM.YYYY в YYYY-MM-DD для запроса
                    parts = date_str_dd_mm_yyyy.split('.')
                    if len(parts) != 3:
                        print(f"Warning: Invalid date format '{date_str_dd_mm_yyyy}' in input for student list.")
                        student_record.append("ERR_DATE_FMT")  # Ошибка формата даты
                        continue

                    date_str_yyyy_mm_dd = f"{parts[2]}-{parts[1]}-{parts[0]}"

                    cursor.execute(
                        "SELECT id_schedule_list FROM schedule_list WHERE id_lesson = ? AND id_student = ? AND lesson_date = ?;",
                        (id_lesson, id_student, date_str_yyyy_mm_dd)
                    )
                    attendance_row = cursor.fetchone()
                    student_record.append("+" if attendance_row else "-")
                students_attendance.append(student_record)

    except sqlite3.Error as db_err:  # ... (обработка ошибок как выше) ...
        print(f"!!! SQLite error in get_student_list !!!")
        traceback.print_exc()
    except Exception as ex:  # ... (обработка ошибок как выше) ...
        print(f"!!! Generic error in get_student_list !!!")
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            print(f"Connection closed. (func: get_student_list)")
    return students_attendance


def delete_visiting(lesson_name, group_id, student_id, year, month, day):  # Изменил lesson
    print(f"delete_visiting called for lesson_name: {lesson_name}, group_id: {group_id}, student_id: {student_id}")
    success = False
    connection = None
    try:
        print(f"--- DEBUG: Attempting to connect in function 'delete_visiting' with dataBasePath: {dataBasePath} ---")
        connection = sqlite3.connect(dataBasePath)
        # connection.row_factory = sqlite3.Row # Не обязательно для DELETE, если не читаем результат
        print(f"Successful connection! (func: delete_visiting)")
        print("#" * 20)

        with connection.cursor() as cursor:
            cursor.execute("SELECT id_lesson FROM lesson WHERE Lesson = ?;", (lesson_name,))
            id_lesson_row = cursor.fetchone()
            if not id_lesson_row:
                print(f"Lesson '{lesson_name}' not found for deletion.")
                return False  # Предмет не найден

            id_lesson = id_lesson_row["id_lesson"]
            lesson_date = f"{year}-{month:02d}-{day:02d}"

            delete_sql = """
                DELETE FROM schedule_list 
                WHERE id_lesson = ? AND id_study_group = ? AND id_student = ? AND lesson_date = ?;
            """
            print(f"Executing delete: {delete_sql} with params ({id_lesson}, {group_id}, {student_id}, {lesson_date})")
            cursor.execute(delete_sql, (id_lesson, group_id, student_id, lesson_date))
            connection.commit()
            print(f"Rows affected by delete: {cursor.rowcount}")
            success = cursor.rowcount > 0  # Успешно, если хотя бы одна строка удалена

    except sqlite3.Error as db_err:  # ... (обработка ошибок как выше) ...
        print(f"!!! SQLite error in delete_visiting !!!")
        traceback.print_exc()
    except Exception as ex:  # ... (обработка ошибок как выше) ...
        print(f"!!! Generic error in delete_visiting !!!")
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            print(f"Connection closed. (func: delete_visiting)")
    return success


def _execute_query(query, params=None, fetch_one=False, fetch_all=False, is_insert_or_delete=False,
                   fetch_last_id=False, func_name="<unknown>"):  # <--- ДОБАВЛЕН fetch_last_id
    result = None
    connection = None
    cursor_obj = None
    try:
        # print(f"--- DEBUG: Attempting to connect in function '{func_name}' with dataBasePath: {dataBasePath} ---")
        connection = sqlite3.connect(dataBasePath)
        connection.row_factory = sqlite3.Row  # Для удобного доступа к колонкам по именам
        # print(f"Successful connection! (func: {func_name})")

        cursor_obj = connection.cursor()
        cursor_obj.execute(query, params or ())

        if is_insert_or_delete:
            connection.commit()
            if fetch_last_id:
                result = cursor_obj.lastrowid  # Получаем ID последней вставленной строки
            else:
                # Для INSERT/UPDATE/DELETE можно возвращать True/False или количество измененных строк
                result = cursor_obj.rowcount > 0
                # print(f"Committed changes. (func: {func_name}) Last ID (if requested): {result if fetch_last_id else 'N/A'}")
        elif fetch_one:
            result = cursor_obj.fetchone()
        elif fetch_all:
            result = cursor_obj.fetchall()

    except sqlite3.Error as db_err:
        print(f"!!! SQLite error in {func_name} !!!")
        print(f"  Query: {query}")
        print(f"  Params: {params}")
        print(f"  String: {str(db_err)}")
        traceback.print_exc()
    except Exception as ex:
        print(f"!!! Generic error in {func_name} !!!")
        print(f"  String: {str(ex)}")
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            # print(f"Connection closed. (func: {func_name})")
    return result

def get_education_id_by_name(education_name_from_state: str):
    """Получает ID формы обучения по ее названию из state (например, 'бакалавр')."""
    db_education_name = None
    # Приводим значение из state к тому, как оно хранится в БД
    if "бакалавр" in education_name_from_state.lower():
        db_education_name = "бакалавр"
    elif "магистр" in education_name_from_state.lower():
        db_education_name = "Магистратура"
    # Добавьте другие формы обучения, если они у вас есть, например:
    # elif "специалист" in education_name_from_state.lower():
    #     db_education_name = "Специалитет"

    if not db_education_name:
        print(f"Неизвестное название формы обучения для поиска ID: {education_name_from_state}")
        return None  # Возвращаем None, если форма обучения не распознана

    sql = "SELECT id_education FROM education WHERE Education = ?;"
    row = _execute_query(sql, (db_education_name,), fetch_one=True, func_name="get_education_id_by_name")
    if row:
        return row['id_education']
    else:
        # Если формы обучения нет в БД, это проблема данных.
        # Можно либо вернуть None, либо попытаться добавить ее (но это усложнит логику)
        print(
            f"Критическая ошибка: Форма обучения '{db_education_name}' не найдена в таблице 'education'. Проверьте данные в БД.")
        return None


def add_new_student_to_db(student_fio, id_study_group, id_fuclty, id_institute, id_education, course):
    """
    Добавляет нового студента в базу данных.
    Возвращает ID нового студента в случае успеха, иначе None.
    Если студент с таким ФИО в этой группе уже существует, возвращает ID существующего студента.
    """
    # Проверка на существование такого же студента в этой же группе
    check_sql = """
        SELECT id_student FROM student 
        WHERE Student = ? AND id_study_group = ?;
    """
    existing_student = _execute_query(check_sql, (student_fio, id_study_group), fetch_one=True,
                                      func_name="check_existing_student_in_group")
    if existing_student:
        print(
            f"Студент '{student_fio}' уже существует в группе ID {id_study_group} с ID {existing_student['id_student']}.")
        return existing_student['id_student']  # Возвращаем ID существующего, чтобы не создавать дубликат

    # Если студента нет, добавляем нового
    sql = """
        INSERT INTO student (Student, id_study_group, id_fuclty, id_institute, id_education, course)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    params = (student_fio, id_study_group, id_fuclty, id_institute, id_education, course)

    # Предполагается, что id_student в таблице student является AUTOINCREMENT (INTEGER PRIMARY KEY)
    new_student_id = _execute_query(sql, params, is_insert_or_delete=True, fetch_last_id=True,
                                    func_name="add_new_student_to_db")

    if new_student_id:
        print(f"Студент '{student_fio}' успешно добавлен в БД с ID {new_student_id}.")
        return new_student_id
    else:
        print(
            f"Не удалось добавить студента '{student_fio}' в БД (возможно, ошибка при вставке или _execute_query вернул не ID).")
        return None


def add_new_group_to_db(group_name: str, group_url: str = None):
    """
    Добавляет новую учебную группу, если ее еще нет по названию.
    Возвращает ID новой или существующей группы, или None в случае ошибки.
    """
    check_sql = "SELECT id_study_group, url FROM study_group WHERE Study_group = ?;"  # Также получаем url для сравнения
    existing = _execute_query(check_sql, (group_name,), fetch_one=True, func_name="check_existing_group")

    if existing:
        print(f"Группа '{group_name}' уже существует с ID {existing['id_study_group']}.")
        # Опционально: обновить URL, если он предоставлен и отличается
        # Убедимся, что group_url не None перед сравнением с existing['url'], который тоже может быть None
        if group_url is not None and existing['url'] != group_url:
            update_url_sql = "UPDATE study_group SET url = ? WHERE id_study_group = ?;"
            updated = _execute_query(update_url_sql, (group_url, existing['id_study_group']), is_insert_or_delete=True,
                                     func_name="update_group_url")
            if updated:
                print(f"URL для группы '{group_name}' (ID: {existing['id_study_group']}) обновлен на '{group_url}'.")
        return existing['id_study_group']

    # Если группы нет, добавляем новую
    insert_sql = "INSERT INTO study_group (Study_group, url) VALUES (?, ?);"
    # Если group_url не предоставлен, вставляем NULL (SQLite это обработает, если поле допускает NULL)
    new_id = _execute_query(insert_sql, (group_name, group_url), is_insert_or_delete=True, fetch_last_id=True,
                            func_name="add_new_group_to_db")

    if new_id:
        print(f"Группа '{group_name}' успешно добавлена с ID {new_id}.")
        return new_id
    else:
        print(f"Не удалось добавить группу '{group_name}'.")
        return None

def add_new_institute_to_db(institute_name: str):
    """Добавляет новый институт, если его еще нет. Возвращает ID."""
    check_sql = "SELECT id_institute FROM institute WHERE Institute = ?;"
    existing = _execute_query(check_sql, (institute_name,), fetch_one=True, func_name="check_existing_institute")
    if existing:
        print(f"Институт '{institute_name}' уже существует с ID {existing['id_institute']}.")
        return existing['id_institute']

    insert_sql = "INSERT INTO institute (Institute) VALUES (?);"
    new_id = _execute_query(insert_sql, (institute_name,), is_insert_or_delete=True, fetch_last_id=True,
                            func_name="add_new_institute_to_db")
    if new_id:
        print(f"Институт '{institute_name}' успешно добавлен с ID {new_id}.")
        return new_id
    else:
        print(f"Не удалось добавить институт '{institute_name}'.")
        return None


def add_new_faculty_to_db(faculty_name: str, id_institute: int):
    """Добавляет новый факультет к институту, если его еще нет. Возвращает ID."""
    # Предполагается, что связка факультет-институт уникальна по названию факультета ВНУТРИ института.
    # Если название факультета должно быть уникальным глобально, запрос check_sql нужно изменить.
    check_sql = "SELECT id_fuclty FROM fuclty WHERE Fuclty = ? AND id_institute = ?;"
    existing = _execute_query(check_sql, (faculty_name, id_institute), fetch_one=True,
                              func_name="check_existing_faculty")
    if existing:
        print(f"Факультет '{faculty_name}' уже существует в институте ID {id_institute} с ID {existing['id_fuclty']}.")
        return existing['id_fuclty']

    insert_sql = "INSERT INTO fuclty (Fuclty, id_institute) VALUES (?, ?);"
    new_id = _execute_query(insert_sql, (faculty_name, id_institute), is_insert_or_delete=True, fetch_last_id=True,
                            func_name="add_new_faculty_to_db")
    if new_id:
        print(f"Факультет '{faculty_name}' успешно добавлен к институту ID {id_institute} с ID {new_id}.")
        return new_id
    else:
        print(f"Не удалось добавить факультет '{faculty_name}'.")
        return None


def add_new_group_to_db(group_name: str, group_url: str = None):
    """
    Добавляет новую учебную группу, если ее еще нет по названию. Возвращает ID.
    Связи с факультетом, курсом и т.д. устанавливаются через таблицу student.
    """
    check_sql = "SELECT id_study_group FROM study_group WHERE Study_group = ?;"
    existing = _execute_query(check_sql, (group_name,), fetch_one=True, func_name="check_existing_group")
    if existing:
        print(f"Группа '{group_name}' уже существует с ID {existing['id_study_group']}.")
        # Можно обновить URL, если он предоставлен и отличается
        if group_url and existing['url'] != group_url:
            update_url_sql = "UPDATE study_group SET url = ? WHERE id_study_group = ?;"
            _execute_query(update_url_sql, (group_url, existing['id_study_group']), is_insert_or_delete=True,
                           func_name="update_group_url")
            print(f"URL для группы '{group_name}' обновлен.")
        return existing['id_study_group']

    insert_sql = "INSERT INTO study_group (Study_group, url) VALUES (?, ?);"
    new_id = _execute_query(insert_sql, (group_name, group_url), is_insert_or_delete=True, fetch_last_id=True,
                            func_name="add_new_group_to_db")
    if new_id:
        print(f"Группа '{group_name}' успешно добавлена с ID {new_id}.")
        return new_id
    else:
        print(f"Не удалось добавить группу '{group_name}'.")
        return None