# SheludeBot

Telegram bot for SPbPU (Peter the Great St. Petersburg Polytechnic University) students — attendance tracking, schedule lookup, and presence list export.

**Bot:** [@Poly_Tracker_Bot](https://t.me/Poly_Tracker_Bot)

## Features

| Command / Button | Description |
|------------------|-------------|
| Авторизоваться | Multi-step FSM: select education type → institute → faculty → group → course → find student by name |
| Информация | Show current user info from DB |
| Отметиться | Mark attendance — checks geolocation (haversine) and time window (±20 min from class start) |
| Расписание | Scrape and display current week's schedule from SPbPU website |
| Списки присутствующих | Generate an Excel file with attendance records for the current academic year |

## Stack

| Component | Technology |
|-----------|-----------|
| Bot framework | [aiogram 3.x](https://docs.aiogram.dev/) (async) |
| State machine | `aiogram.fsm` — `StatesGroup` with 7 states for authorization flow |
| Database | SQLite via `sqlite3` (`DataBase.db`) |
| Schedule scraping | Selenium (Firefox) + BeautifulSoup, SPbPU schedule page |
| Geolocation check | `haversine` library — Euclidean distance on Earth surface |
| Excel export | `openpyxl` |
| Scheduling | `APScheduler` (async, weekly cleanup) |
| Config | `python-dotenv` — `TOKEN` from `.env` |

## Authorization flow (FSM)

```
/start
  └── education type (Бакалавриат / Магистратура / ...)
        └── institute
              └── faculty
                    └── group
                          └── course
                                └── student name → stored in DB
```

## Attendance check

- Window: **20 minutes before** class start up to class end
- Geolocation: student sends location → `haversine(student_coords, campus_coords)` — must be within campus radius
- Result written to SQLite

## Schedule scraping (`sites/purse.py`)

Opens the group's schedule URL in Firefox via Selenium, extracts `.schedule__day` → `.lesson` blocks with start/end times, room, subject, and teacher. Returns "no classes this week" message if the block is empty.

## Project structure

```
SheduleBot/
├── main.py              # Bot entry point, Dispatcher setup
├── app/
│   ├── handlers.py      # All message/callback handlers, FSM logic
│   └── keyboards.py     # Reply and inline keyboards
├── database/
│   ├── requests.py      # All SQLite queries
│   ├── createTables.py  # Schema creation
│   ├── random_data.py   # Test data generator
│   └── DataBase.db      # SQLite database
└── sites/
    └── purse.py         # SPbPU schedule scraper
```

## Setup

```bash
pip install aiogram python-dotenv haversine openpyxl apscheduler selenium beautifulsoup4
echo "TOKEN=your_bot_token" > .env
python main.py
```

Requires Firefox + geckodriver for schedule scraping.
