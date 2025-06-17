from datetime import datetime, time
from bs4 import BeautifulSoup
from selenium import webdriver


def get_schedule(url):
    schedule_data = []
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find(class_="schedule")
    if elements.find_next().text == "На эту неделю занятия не поставлены":
        string = "На эту неделю занятия не поставлены 😘"
        return string
    else:
        days = elements.find_all(class_="schedule__day")
        for day in days:
            day_data = {}
            date = day.find(class_="schedule__date").text
            day_data["date"] = date
            lessons = day.find_all(class_="lesson")
            lessons_data = []
            for lesson in lessons:
                lesson_data = {}
                time_elements = lesson.find(class_="lesson__time").find_all("span")
                start_time = time_elements[0].get_text()
                end_time = time_elements[2].get_text()
                time = f"{start_time}-{end_time}"
                lesson_data["time_start"] = start_time
                lesson_data["time_end"] = end_time

                name_lesson = (
                    lesson.find(class_="lesson__subject").find_all("span")[5].text
                )
                lesson_data["name_lesson"] = name_lesson
                lesson_type = lesson.find(class_="lesson__type").text
                lesson_data["lesson_type"] = lesson_type
                teacher_element = lesson.find(class_="lesson__teachers")
                if teacher_element is not None:
                    teacher = (
                        lesson.find(class_="lesson__teachers").find_all("span")[2].text
                    )
                else:
                    teacher = ""
                lesson_data["teacher"] = teacher

                place = (
                    lesson.find(class_="lesson__places")
                    .find(class_="lesson__link")
                    .find_all("span")
                )
                spot = f"{place[1].text}, {place[6].text}{place[7].text}"
                lesson_data["spot"] = place[1].text
                lesson_data["auditory"] = place[7].text

                print(time)
                print(name_lesson)
                print(lesson_type)
                print(f"Преподаватель: {teacher}")
                print(spot)
                print("_" * 40)
                lessons_data.append(lesson_data)
            day_data["lessons"] = lessons_data
            schedule_data.append(day_data)
    print("Exit")
    driver.quit()
    return schedule_data
