import glob
import config
import sqlite3 as sql3
from io_proj_lib import import_line, how_many_lines, import_the_menu
from datetime import date


with sql3.connect(config.STUDENTS_DB) as connection:
    cursor = connection.cursor()


def create_table_students():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE ON CONFLICT IGNORE,
    day_month_bday VARCHAR(5),
    year_bday VARCHAR(4),
    class VARCHAR(3))''')


def create_table_menu_master():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_master(
    one TEXT UNIQUE ON CONFLICT IGNORE, 
    two TEXT UNIQUE ON CONFLICT IGNORE,
    three TEXT UNIQUE ON CONFLICT IGNORE,
    four TEXT UNIQUE ON CONFLICT IGNORE, 
    five TEXT UNIQUE ON CONFLICT IGNORE, 
    six TEXT UNIQUE ON CONFLICT IGNORE, 
    seven NONE, 
    eight TEXT UNIQUE ON CONFLICT IGNORE, 
    nine TEXT UNIQUE ON CONFLICT IGNORE, 
    ten TEXT UNIQUE ON CONFLICT IGNORE, 
    eleven TEXT UNIQUE ON CONFLICT IGNORE, 
    twelve TEXT UNIQUE ON CONFLICT IGNORE, 
    thirteen TEXT UNIQUE ON CONFLICT IGNORE, 
    fourteen NONE
    )''')

    cursor.execute('''
    INSERT INTO menu_master(
    one, two, three, four, five, six, 
    eight, nine, ten, eleven, twelve, thirteen)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', import_the_menu("2weekrotation.txt"))


def find_in_menu(bot_today=date.today()):
    zero = date(2024, 1, 8)  # 8
    delta = abs(bot_today - zero)
    delta = delta.days % 14
    try:
        cursor.execute("""
        SELECT * FROM menu_master
        """)
        records = cursor.fetchall()
        return [word for line in records for word in list(line)][delta]

    except sql3.Error as error:
        return error


def load_into_table(location):
    for ite in glob.glob(location):
        ite = ite.replace("\\", "/")

        for i in range(how_many_lines(ite)):
            cursor.execute('''
            INSERT INTO students(name, day_month_bday, year_bday, class) VALUES(?, ?, ?, ?)
            ''', import_line(ite, i)[1:])


def find_by_date(var_date, class_id=None):
    if class_id is not None:
        try:
            cursor.execute('''
                SELECT name, class, day_month_bday FROM students
                WHERE day_month_bday = ? AND class = ?
                ORDER BY name;
                ''', [str(var_date), str(class_id)])

            records = cursor.fetchall()
            return records
        except sql3.Error as error:
            return error
    else:
        try:
            cursor.execute('''
                SELECT name, class, day_month_bday FROM students
                WHERE day_month_bday = ?
                ORDER BY name;
                ''', [str(var_date)])

            records = cursor.fetchall()
            return records
        except sql3.Error as error:
            return error


def find_by_name(name, class_id=None):
    if class_id is not None:
        try:
            cursor.execute('''
                SELECT name, class, day_month_bday FROM students
                WHERE name LIKE ? AND class = ?
                ORDER BY name;
                ''', [f"%{name.title()}%".strip(), class_id])

            records = cursor.fetchall()
            return records

        except sql3.Error as error:
            return error
    else:
        try:
            cursor.execute('''
                SELECT name, class, day_month_bday FROM students
                WHERE name LIKE ?
                ORDER BY name;
                ''', [f"%{name.title()}%".strip()])

            records = cursor.fetchall()
            return records

        except sql3.Error as error:
            return error


if __name__ == "__main__":
    create_table_students()
    create_table_menu_master()
    load_into_table("classes_txt/*")
    connection.commit()
    connection.close()
