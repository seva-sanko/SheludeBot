import random
import sqlite3  # Добавлено для populate_database_directly
import traceback  # Добавлено для populate_database_directly
import os # Добавьте os
from pathlib import Path # Добавьте Path

# --- Определение пути к БД относительно текущего скрипта ---
SCRIPT_DIR = Path(__file__).resolve().parent # Это /Users/Seva/Polytech/tgBot/SheduleBot/database
DB_FILE_PATH = str(SCRIPT_DIR / "DataBase.db") # БД лежит рядом со скриптом

print(f"--- DEBUG: random_data.py (initialization) ---")
print(f"Current working directory (CWD): {os.getcwd()}")
print(f"Absolute path of this script: {Path(__file__).resolve()}")
print(f"SCRIPT_DIR: {SCRIPT_DIR}")
print(f"Calculated DB_FILE_PATH to be used: {DB_FILE_PATH}")
print(f"Does DB file exist at calculated path? {Path(DB_FILE_PATH).exists()}")
print(f"--- END DEBUG ---")

EDUCATION_FORMS = {
    "Бакалавриат": 1,
    "Магистратура": 2
}
INSTITUTES_DATA = {
    1: "Институт компьютерных наук и кибербезопасности", 2: "Гуманитарный институт",
    3: "Физико-математический институт", 4: "Институт промышленного менеджмента, экономики ...",
    5: "Институт биомедицинских систем и биотехнологий", 6: "Инженерно-строительный институт",
    7: "Институт энергетики и телекоммуникаций", 8: "Институт энергетики",
    9: "Институт ядерной энергетики", 10: "Институт машиностроения, материалов и транспорта"
}
FACULTIES_DATA = [
    {"id_fuclty": 1, "name": "Прикладная математика и информатика", "id_institute": 1},
    {"id_fuclty": 2, "name": "Механика и математическое моделирование", "id_institute": 3},
    {"id_fuclty": 3, "name": "Статистика", "id_institute": 4},
    {"id_fuclty": 4, "name": "Математика и компьютерные науки", "id_institute": 1},
    {"id_fuclty": 5, "name": "Математическое обеспечение и администрирование информационных систем", "id_institute": 1},
    {"id_fuclty": 6, "name": "Прикладная математика и физика", "id_institute": 3},
    {"id_fuclty": 7, "name": "Физика", "id_institute": 3},
    {"id_fuclty": 8, "name": "Экономика и бизнес-информатика", "id_institute": 8},
    {"id_fuclty": 9, "name": "Дизайн архитектурной среды", "id_institute": 6},
    {"id_fuclty": 10, "name": "Строительство", "id_institute": 6},
    {"id_fuclty": 11, "name": "Строительство уникальных зданий и сооружений", "id_institute": 6},
    {"id_fuclty": 12, "name": "Информатика и вычислительная техника", "id_institute": 1},
    {"id_fuclty": 13, "name": "Информационные системы и технологии", "id_institute": 1},
    {"id_fuclty": 14, "name": "Прикладная информатика", "id_institute": 1},
    {"id_fuclty": 15, "name": "Программная инженерия", "id_institute": 1},
    {"id_fuclty": 16, "name": "Программная инженерия (на базе высшего образования)", "id_institute": 1},
    {"id_fuclty": 17, "name": "Программная инженерия (на базе среднего профессионального образования)",
     "id_institute": 1},
    {"id_fuclty": 18, "name": "Информационная безопасность", "id_institute": 1},
    {"id_fuclty": 19, "name": "Компьютерная безопасность", "id_institute": 1},
    {"id_fuclty": 20, "name": "Информационная безопасность автоматизированных систем", "id_institute": 1},
    {"id_fuclty": 21, "name": "Информационно-аналитические системы безопасности", "id_institute": 1},
    {"id_fuclty": 22, "name": "Радиотехника", "id_institute": 7},
    {"id_fuclty": 23, "name": "Инфокоммуникационные технологии и системы связи", "id_institute": 7},
    {"id_fuclty": 24, "name": "Электроника и наноэлектроника", "id_institute": 7},
    {"id_fuclty": 25, "name": "Фотоника и оптоинформатика", "id_institute": 7},
    {"id_fuclty": 26, "name": "Теплоэнергетика и теплотехника", "id_institute": 8},
    {"id_fuclty": 27, "name": "Электроэнергетика и электротехника", "id_institute": 8},
    {"id_fuclty": 28, "name": "Энергетическое машиностроение", "id_institute": 8},
    {"id_fuclty": 29, "name": "Ядерные энергетика и теплофизика", "id_institute": 9},
    {"id_fuclty": 30, "name": "Атомные станции: проектирование, эксплуатация и инжиниринг", "id_institute": 9},
    {"id_fuclty": 31, "name": "Проектирование и эксплуатация атомных станций", "id_institute": 9},
    {"id_fuclty": 32, "name": "Машиностроение", "id_institute": 10},
    {"id_fuclty": 33, "name": "Прикладная механика", "id_institute": 3},
    {"id_fuclty": 34, "name": "Автоматизация технологических процессов и производств", "id_institute": 10},
    {"id_fuclty": 35, "name": "Конструкторско-технологическое обеспечение машиностроительных производств",
     "id_institute": 10},
    {"id_fuclty": 36, "name": "Мехатроника и робототехника", "id_institute": 10},
    {"id_fuclty": 37, "name": "Техническая физика", "id_institute": 7},
    {"id_fuclty": 38, "name": "Биотехнология", "id_institute": 5},
    {"id_fuclty": 39, "name": "Продукты питания животного происхождения", "id_institute": 5},
    {"id_fuclty": 40, "name": "Технология продукции и организация общественного питания", "id_institute": 5},
    {"id_fuclty": 41, "name": "Техносферная безопасность", "id_institute": 6},
    {"id_fuclty": 42, "name": "Материаловедение и технология материалов", "id_institute": 10},
    {"id_fuclty": 43, "name": "Металлургия", "id_institute": 10},
    {"id_fuclty": 44, "name": "Технология транспортных процессов", "id_institute": 10},
    {"id_fuclty": 45, "name": "Наземные транспортно-технологические средства", "id_institute": 10},
    {"id_fuclty": 46, "name": "Управление качеством", "id_institute": 10},
    {"id_fuclty": 47, "name": "Управление в технических системах", "id_institute": 1},
    {"id_fuclty": 48, "name": "Инноватика", "id_institute": 10},
    {"id_fuclty": 49, "name": "Нанотехнологии и микросистемная техника", "id_institute": 10},
    {"id_fuclty": 50, "name": "Технология художественной обработки материалов", "id_institute": 10},
    {"id_fuclty": 51, "name": "Экономика", "id_institute": 4},
    {"id_fuclty": 52, "name": "Менеджмент", "id_institute": 4},
    {"id_fuclty": 53, "name": "Государственное и муниципальное управление", "id_institute": 4},
    {"id_fuclty": 54, "name": "Бизнес-информатика", "id_institute": 4},
    {"id_fuclty": 55, "name": "Торговое дело", "id_institute": 4},
    {"id_fuclty": 56, "name": "Товароведение", "id_institute": 4},
    {"id_fuclty": 57, "name": "Экономическая безопасность", "id_institute": 4},
    {"id_fuclty": 58, "name": "Таможенное дело", "id_institute": 4},
    {"id_fuclty": 59, "name": "Юриспруденция", "id_institute": 2},
    {"id_fuclty": 60, "name": "Зарубежное регионоведение", "id_institute": 2},
    {"id_fuclty": 61, "name": "Реклама и связи с общественностью", "id_institute": 2},
    {"id_fuclty": 62, "name": "Издательское дело", "id_institute": 2},
    {"id_fuclty": 63, "name": "Сервис", "id_institute": 4},
    {"id_fuclty": 64, "name": "Туризм", "id_institute": 4},
    {"id_fuclty": 65, "name": "Гостиничное дело", "id_institute": 4},
    {"id_fuclty": 66, "name": "Психолого-педагогическое образование", "id_institute": 2},
    {"id_fuclty": 67, "name": "Лингвистика", "id_institute": 2},
    {"id_fuclty": 68, "name": "Интеллектуальные системы в гуманитарной сфере", "id_institute": 2},
    {"id_fuclty": 69, "name": "Дизайн", "id_institute": 6}
]

LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Васильев", "Зайцев", "Смирнов", "Попов", "Соколов",
              "Михайлов"]
FIRST_NAMES_MALE = ["Иван", "Алексей", "Дмитрий", "Сергей", "Андрей", "Максим", "Евгений", "Павел", "Роман", "Артем"]
FIRST_NAMES_FEMALE = ["Мария", "Ольга", "Елена", "Анна", "Екатерина", "Светлана", "Наталья", "Татьяна", "Ирина", "Юлия"]
PATRONYMICS_MALE = ["Иванович", "Сергеевич", "Викторович", "Андреевич", "Евгеньевич", "Дмитриевич", "Александрович",
                    "Максимович", "Павлович", "Романович"]
PATRONYMICS_FEMALE = ["Ивановна", "Сергеевна", "Викторовна", "Андреевна", "Евгеньевна", "Дмитриевна", "Александровна",
                      "Максимовна", "Павловна", "Романовна"]

current_study_group_id = 1


# current_student_id - не нужен, если id_student автоинкрементный в таблице student

def generate_fio():
    last_name = random.choice(LAST_NAMES)
    if random.random() < 0.5:
        first_name = random.choice(FIRST_NAMES_MALE)
        patronymic = random.choice(PATRONYMICS_MALE)
    else:
        first_name = random.choice(FIRST_NAMES_FEMALE)
        patronymic = random.choice(PATRONYMICS_FEMALE)
    return f"{last_name} {first_name} {patronymic}"


def generate_sql_for_students():
    global current_study_group_id  # Используем для генерации ID групп, если они не автоинкрементные в БД

    sql_inserts_groups = []
    sql_inserts_students = []
    generated_groups_ids_for_linking = {}  # (id_f, course_num, group_suffix_num, edu_id) -> сгенерированный_id_группы

    group_abbreviations = {
        fid_data["id_fuclty"]: "Б" + "".join([word[0] for word in fid_data["name"].split()[:2]]).upper()
        for fid_data in FACULTIES_DATA
    }
    mag_group_abbreviations = {
        fid: "М" + abbr[1:] if len(abbr) > 1 and abbr.startswith("Б") else "М" + abbr
        for fid, abbr in group_abbreviations.items()
    }
    # Добавляем запасные варианты, если аббревиатура не сгенерировалась (например, очень короткое имя факультета)
    for fid_data in FACULTIES_DATA:
        fid = fid_data["id_fuclty"]
        if fid not in group_abbreviations: group_abbreviations[fid] = "БГРП"
        if fid not in mag_group_abbreviations: mag_group_abbreviations[fid] = "МГРП"

    for edu_name, edu_id in EDUCATION_FORMS.items():
        courses = range(1, 5) if edu_name == "Бакалавриат" else range(1, 3)
        for course_num in courses:
            for inst_id, inst_name in INSTITUTES_DATA.items():
                faculties_in_institute = [f for f in FACULTIES_DATA if f["id_institute"] == inst_id]
                if not faculties_in_institute: continue

                num_faculties_to_use = min(len(faculties_in_institute),
                                           random.randint(1, 2) if len(faculties_in_institute) > 1 else 1)
                selected_faculties = random.sample(faculties_in_institute, num_faculties_to_use)

                for faculty_data in selected_faculties:
                    id_f = faculty_data["id_fuclty"]
                    for i in range(random.randint(1, 1)):  # По одной группе на факультет/курс для начала
                        group_suffix_num = i + 1
                        current_group_abbr_dict = mag_group_abbreviations if edu_name == "Магистратура" else group_abbreviations
                        group_abbr = current_group_abbr_dict.get(id_f, "ГРП" if edu_name == "Бакалавриат" else "МГРП")

                        current_year_short = "23"
                        try:
                            admission_year_short = int(current_year_short) - (course_num - 1)
                        except TypeError:  # На случай, если current_year_short не число
                            admission_year_short = 23 - (course_num - 1)

                        group_name = f"{group_abbr}{admission_year_short}-{group_suffix_num}"
                        group_url = f"http://example.com/{group_name.lower().replace(' ', '_')}"
                        group_key = (id_f, course_num, group_suffix_num, edu_id)

                        # В SQL генераторе мы явно указываем ID группы, так как не можем получить lastrowid
                        # Если id_study_group в БД автоинкрементный, то при выполнении SQL его не нужно указывать.
                        # Но для связывания студентов нам нужен этот ID.
                        # Поэтому для генерации SQL мы его продолжаем инкрементить.
                        # А для populate_database_directly - используем lastrowid.

                        # Генерируем INSERT для группы
                        # Если id_study_group автоинкрементный, то в БД нужно будет убрать current_study_group_id
                        sql_inserts_groups.append(
                            f"INSERT INTO study_group (id_study_group, Study_group, url) VALUES ({current_study_group_id}, '{group_name}', '{group_url}');"
                        )
                        generated_groups_ids_for_linking[group_key] = current_study_group_id  # Сохраняем для студентов

                        # Генерируем студентов для этой группы
                        num_students_in_group = random.randint(1, 2)  # По 1-2 студента на группу
                        for _ in range(num_students_in_group):
                            student_fio = generate_fio()
                            # Если id_student автоинкрементный, то в БД его не нужно указывать.
                            sql_inserts_students.append(
                                f"INSERT INTO student (Student, id_study_group, id_fuclty, id_institute, id_education, course) "
                                f"VALUES ('{student_fio}', {current_study_group_id}, {id_f}, {inst_id}, {edu_id}, {course_num});"
                            )
                        current_study_group_id += 1  # Инкрементируем ID для следующей группы
    return sql_inserts_groups, sql_inserts_students


def populate_database_directly():
    # --- Определение словарей аббревиатур ЗДЕСЬ, чтобы они были в области видимости функции ---
    group_abbreviations = {
        fid_data["id_fuclty"]: "Б" + "".join([word[0] for word in fid_data["name"].split()[:2]]).upper()
        for fid_data in FACULTIES_DATA
    }
    mag_group_abbreviations = {
        fid: "М" + abbr[1:] if len(abbr) > 1 and abbr.startswith("Б") else "М" + abbr
        for fid, abbr in group_abbreviations.items()
    }
    for fid_data in FACULTIES_DATA:  # Запасные варианты
        fid = fid_data["id_fuclty"]
        if fid not in group_abbreviations: group_abbreviations[fid] = "БГРП"
        if fid not in mag_group_abbreviations: mag_group_abbreviations[fid] = "МГРП"
    # --- Конец определения словарей аббревиатур ---

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        print(f"Подключено к БД для заполнения (populate_database_directly) по пути: {DB_FILE_PATH}")
        generated_groups_ids_map = {}

        for edu_name, edu_id in EDUCATION_FORMS.items():
            courses = range(1, 5) if edu_name == "Бакалавриат" else range(1, 3)
            for course_num in courses:
                for inst_id, inst_name in INSTITUTES_DATA.items():
                    faculties_in_institute = [f for f in FACULTIES_DATA if f["id_institute"] == inst_id]
                    if not faculties_in_institute: continue
                    num_faculties_to_use = min(len(faculties_in_institute),
                                               random.randint(1, 2) if len(faculties_in_institute) > 1 else 1)
                    selected_faculties = random.sample(faculties_in_institute, num_faculties_to_use)

                    for faculty_data in selected_faculties:
                        id_f = faculty_data["id_fuclty"]
                        for i in range(random.randint(1, 1)):  # По одной группе
                            group_suffix_num = i + 1
                            current_group_abbr_dict = mag_group_abbreviations if edu_name == "Магистратура" else group_abbreviations
                            group_abbr = current_group_abbr_dict.get(id_f,
                                                                     "ГРП" if edu_name == "Бакалавриат" else "МГРП")
                            current_year_short = "23"
                            try:
                                admission_year_short = int(current_year_short) - (course_num - 1)
                            except TypeError:
                                admission_year_short = 23 - (course_num - 1)
                            group_name = f"{group_abbr}{admission_year_short}-{group_suffix_num}"
                            group_url = f"http://example.com/{group_name.lower().replace(' ', '_')}"
                            group_key = (id_f, course_num, group_suffix_num, edu_id)
                            actual_group_id_to_use = -1

                            if group_key not in generated_groups_ids_map:
                                try:
                                    cursor.execute("INSERT INTO study_group (Study_group, url) VALUES (?, ?);",
                                                   (group_name, group_url))
                                    actual_group_id_to_use = cursor.lastrowid
                                    print(f"Добавлена группа: {group_name} (ID: {actual_group_id_to_use})")
                                    generated_groups_ids_map[group_key] = actual_group_id_to_use
                                except sqlite3.IntegrityError as e:
                                    print(
                                        f"Ошибка IntegrityError при добавлении группы {group_name}: {e}. Попытка найти существующую.")
                                    cursor.execute("SELECT id_study_group FROM study_group WHERE Study_group = ?",
                                                   (group_name,))
                                    existing_row = cursor.fetchone()
                                    if existing_row:
                                        actual_group_id_to_use = existing_row[0]
                                        generated_groups_ids_map[group_key] = actual_group_id_to_use
                                        print(
                                            f"Найдена существующая группа: {group_name} (ID: {actual_group_id_to_use})")
                                    else:
                                        print(f"Не удалось создать или найти группу {group_name}. Пропуск.")
                                        continue
                            else:
                                actual_group_id_to_use = generated_groups_ids_map[group_key]

                            if actual_group_id_to_use != -1:
                                num_students_in_group = random.randint(1, 2)
                                for _ in range(num_students_in_group):
                                    student_fio = generate_fio()
                                    try:
                                        cursor.execute(
                                            "INSERT INTO student (Student, id_study_group, id_fuclty, id_institute, id_education, course) VALUES (?, ?, ?, ?, ?, ?);",
                                            (student_fio, actual_group_id_to_use, id_f, inst_id, edu_id, course_num)
                                        )
                                    except sqlite3.Error as e_stud:
                                        print(
                                            f"Ошибка при добавлении студента {student_fio} в группу ID {actual_group_id_to_use}: {e_stud}")
        conn.commit()
        print("Данные успешно добавлены и сохранены (populate_database_directly).")
    except sqlite3.Error as e:
        print(f"Ошибка SQLite (populate_database_directly): {e}")
        if conn: conn.rollback()
    except Exception as e_gen:
        print(f"Общая ошибка (populate_database_directly): {e_gen}")
        traceback.print_exc()
        if conn: conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Соединение с БД закрыто (populate_database_directly).")


if __name__ == "__main__":
    print("--- Запуск скрипта генерации данных ---")
    print("Убедитесь, что FACULTIES_DATA содержит все ваши факультеты с корректными id_institute.")
    print("И что INSTITUTES_DATA также актуален.")

    # --- Вариант 1: Генерация SQL команд для ручного выполнения ---
    # Перед этим, если таблицы study_group и student не пусты и ID в них не автоинкрементные,
    # вам нужно будет установить current_study_group_id вручную на значение > максимального существующего.
    # Если ID автоинкрементные, то для SQL вам нужно будет убрать явное указание ID при INSERT.
    # Но для связывания студентов с группами, мы все равно генерируем SQL с ID для study_group.

    # print("Генерация SQL команд...")
    # generated_group_inserts, generated_student_inserts = generate_sql_for_students()
    # print("\n-- SQL для добавления учебных групп (study_group) --")
    # print("-- Если id_study_group в БД автоинкрементный, УДАЛИТЕ явное указание ID из этих INSERT'ов --")
    # for sql in generated_group_inserts:
    #     print(sql)
    # print("\n-- SQL для добавления студентов (student) --")
    # print("-- Если id_student в БД автоинкрементный, УДАЛИТЕ явное указание ID из этих INSERT'ов (если оно есть) --")
    # for sql in generated_student_inserts:
    #     print(sql)

    # --- Вариант 2: Прямое заполнение БД (предполагаются автоинкрементные ID в таблицах) ---
    print("\nПопытка прямого заполнения БД (populate_database_directly)...")
    print("ВНИМАНИЕ: Это запишет данные в 'database/DataBase.db'.")
    print("Рекомендуется сделать бэкап вашей БД перед запуском, если там есть важные данные.")
    print(
        "Также, если таблицы 'study_group' и 'student' не пусты, могут возникнуть конфликты уникальности для 'Study_group' name.")

    # Очистка таблиц перед заполнением (РЕКОМЕНДУЕТСЯ ДЛЯ ТЕСТА, если не жалко старых данных)
    # conn_clean = None
    # try:
    #     conn_clean = sqlite3.connect('database/DataBase.db')
    #     cursor_clean = conn_clean.cursor()
    #     print("Очистка таблиц student и study_group...")
    #     cursor_clean.execute("DELETE FROM student;")
    #     cursor_clean.execute("DELETE FROM study_group;")
    #     # Сброс счетчиков автоинкремента для sqlite_sequence (если таблицы используют AUTOINCREMENT)
    #     cursor_clean.execute("DELETE FROM sqlite_sequence WHERE name='student';")
    #     cursor_clean.execute("DELETE FROM sqlite_sequence WHERE name='study_group';")
    #     conn_clean.commit()
    #     print("Таблицы очищены.")
    # except sqlite3.Error as e_clean:
    #     print(f"Ошибка при очистке таблиц: {e_clean}")
    # finally:
    #     if conn_clean:
    #         conn_clean.close()

    if input(f"Продолжить прямое заполнение БД по пути '{DB_FILE_PATH}'? (yes/no): ").lower() == 'yes':
        populate_database_directly()
    else:
        print(
            "Прямое заполнение отменено. Вы можете использовать сгенерированные SQL команды выше (если раскомментируете их генерацию).")