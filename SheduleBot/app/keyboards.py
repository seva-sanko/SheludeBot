from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
import database.requests as bd  # Предполагается такой импорт

import database.requests as bd

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✖️Отмена")]],
    resize_keyboard=True,
    input_field_placeholder="Choose the button",
)

geo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍Отправить местоположение", request_location=True)],
        [KeyboardButton(text="✖️Отмена")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Send your geolocation",
)

# клавиатура при старте
first_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отметиться"), KeyboardButton(text="Информация")], [KeyboardButton(text="Расписание"),
         KeyboardButton(text="Списки присутствующих")], [KeyboardButton(text="Авторизоваться")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose the button",
)


def get_education_kb():
    buttons = [
        [InlineKeyboardButton(text="Бакалавриат", callback_data="education_бакалавр")],
        [InlineKeyboardButton(text="Магистратура", callback_data="education_магистр")],
        # Кнопка "Отмена" здесь может сбрасывать FSM и возвращать в главное меню
        [InlineKeyboardButton(text="✖️ Отмена авторизации", callback_data="cancel_auth_process")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_institute_kb(education, page):
    institutes = bd.get_institute(education)
    ITEMS_PER_PAGE = 7
    pages = (len(institutes) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if institutes else 1

    keyboard_layout = [
        [InlineKeyboardButton(text="🔙 К выбору формы обучения", callback_data="back_to_education_selection")],
    ]

    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = page * ITEMS_PER_PAGE
    current_page_institutes = institutes[start_index:end_index] if institutes else []

    for el in current_page_institutes:
        keyboard_layout.append(
            [InlineKeyboardButton(text=el["Institute"], callback_data=f"id_institute_{el['id_institute']}")])

    # Логика добавления кнопки "Добавить институт"
    # Показываем, если список пуст на первой странице или если это последняя страница (даже если не пустая)

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"institute_page_{page - 1}"))
    if page < pages:
        pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"institute_page_{page + 1}"))

    if pagination_buttons:
        keyboard_layout.append(pagination_buttons)
    keyboard_layout.append([InlineKeyboardButton(text="✖️ Отмена авторизации", callback_data="cancel_auth_process")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)


def get_fuclty_kb(institute_id, education, page):  # fuclty - опечатка
    faculties = bd.get_fuclty(institute_id, education)
    ITEMS_PER_PAGE = 7
    pages = (len(faculties) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if faculties else 1

    keyboard_layout = [
        # callback_data для кнопки "Назад" должен содержать информацию для восстановления предыдущего шага
        [InlineKeyboardButton(text="🔙 К выбору института", callback_data=f"back_to_institute_selection_{education}")]
        # Передаем education
    ]

    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = page * ITEMS_PER_PAGE
    current_page_faculties = faculties[start_index:end_index] if faculties else []

    for el in current_page_faculties:
        keyboard_layout.append([InlineKeyboardButton(text=el["Fuclty"], callback_data=f"id_fuclty_{el['id_fuclty']}")])


    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"fuclty_page_{page - 1}"))
    if page < pages:
        pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"fuclty_page_{page + 1}"))

    if pagination_buttons:
        keyboard_layout.append(pagination_buttons)
    keyboard_layout.append([InlineKeyboardButton(text="✖️ Отмена авторизации", callback_data="cancel_auth_process")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)


def get_group_kb(fuclty_id, course, education, page):
    groups_from_db = bd.get_groups(fuclty_id, course, education)
    ITEMS_PER_PAGE = 7
    pages = (len(groups_from_db) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if groups_from_db else 1

    keyboard_layout = [
        [InlineKeyboardButton(text="🔙 К выбору направления", callback_data=f"back_to_faculty_selection")]
        # Нужны institute_id и education
    ]

    navigation_buttons_row = []
    max_courses = 4 if "бакалавр" in education.lower() else 2
    if course > 1:
        navigation_buttons_row.append(
            InlineKeyboardButton(text=f"{course - 1} курс", callback_data=f"course_{course - 1}"))
    if course < max_courses:
        navigation_buttons_row.append(
            InlineKeyboardButton(text=f"{course + 1} курс", callback_data=f"course_{course + 1}"))
    if navigation_buttons_row:
        keyboard_layout.append(navigation_buttons_row)

    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = page * ITEMS_PER_PAGE
    current_page_groups = groups_from_db[start_index:end_index] if groups_from_db else []

    for el in current_page_groups:
        keyboard_layout.append(
            [InlineKeyboardButton(text=el["Study_group"], callback_data=f"id_study_group_{el['id_study_group']}")])

    if (not groups_from_db and page == 1) or (page == pages):
        print(f"  (fuclty_id: {fuclty_id}, course: {course}, education: {education}, page: {page})")
        keyboard_layout.append([InlineKeyboardButton(text="➕ Моей группы нет / Добавить",
                                                     callback_data=f"request_add_group_faculty_{fuclty_id}_course_{course}_edu_{education}")])

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"study_group_page_{page - 1}_{course}"))
    if page < pages:
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"study_group_page_{page + 1}_{course}"))

    if pagination_buttons:
        keyboard_layout.append(pagination_buttons)
    keyboard_layout.append([InlineKeyboardButton(text="✖️ Отмена авторизации", callback_data="cancel_auth_process")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)


def get_student_kb(group_id, page):
    students = bd.get_student(group_id)
    ITEMS_PER_PAGE = 7
    pages = (len(students) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if students else 1

    keyboard_layout = [
        [InlineKeyboardButton(text="🔙 К выбору группы", callback_data=f"back_to_group_selection")]
        # Нужны fuclty_id, course, education
    ]

    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = page * ITEMS_PER_PAGE
    current_page_students = students[start_index:end_index] if students else []

    for el in current_page_students:
        keyboard_layout.append(
            [InlineKeyboardButton(text=el["Student"], callback_data=f"id_student_{el['id_student']}")])

    if (not students and page == 1) or (page == pages):
        keyboard_layout.append([InlineKeyboardButton(text="➕ Моего ФИО нет / Добавить",
                                                     callback_data=f"request_add_student_to_group_{group_id}")])

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"student_page_{page - 1}"))
    if page < pages:
        pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"student_page_{page + 1}"))

    if pagination_buttons:
        keyboard_layout.append(pagination_buttons)
    keyboard_layout.append([InlineKeyboardButton(text="✖️ Отмена авторизации", callback_data="cancel_auth_process")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)

