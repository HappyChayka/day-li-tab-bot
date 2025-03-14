import glob
import os
import sqlite3 as sql3
from students.io_proj_lib import import_line, how_many_lines, import_menu, read_from_docx
from datetime import date


STUDENT_SQL_KEYS = "name", "day_month_bday", "year_bday", "class"

with sql3.connect(os.getenv("STUDENTS_DB")) as connection:
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


def load_into_menu(location):
    data = import_menu(location)
    cursor.execute('''
    INSERT INTO menu_master(
    one, two, three, four, five, six, 
    eight, nine, ten, eleven, twelve, thirteen)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)


def delete_menu_master():
    cursor.execute("""
    DROP TABLE menu_master""")


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


def load_into_table_txt(location):
    for ite in glob.glob(location):
        ite = ite.replace("\\", "/")

        for i in range(how_many_lines(ite)):
            cursor.execute('''
            INSERT INTO students(name, day_month_bday, year_bday, class) VALUES(?, ?, ?, ?)
            ''', import_line(ite, i)[1:])


def load_into_table_list(data):
    for line in data:
        cursor.execute('''
        INSERT INTO students(name, day_month_bday, year_bday, class) VALUES(?, ?, ?, ?)
        ''', line)


def find_by_date(var_date, class_id=None):
    params = [str(var_date)]
    class_str = ""
    if class_id is not None:
        class_str = "AND class = ?"
        params.append(class_id)

    try:
        cursor.execute(f'''
            SELECT name, class, day_month_bday FROM students
            WHERE day_month_bday = ? {class_str}
            ORDER BY name;
            ''', params)

        records = cursor.fetchall()
        return records
    except sql3.Error as error:
        return error



def find_by_name(name, class_id=None):
    params = [f"%{name.title()}%".strip()]
    class_str = ""
    if class_id is not None:
        class_str = "AND class = ?"
        params.append(str(class_id))
    try:
        cursor.execute(f'''
            SELECT name, class, day_month_bday FROM students
            WHERE name LIKE ? {class_str}
            ORDER BY name;
            ''', params)

        records = cursor.fetchall()
        return records

    except sql3.Error as error:
        return error


def sqlize_insert(keys) -> (str, str):
    """returns keys and question marks for SQL execute statements, i.e.
    \n('id,name,address', '?,?,?')"""
    return ",".join(map(str, keys)), ",".join(list("?" * len(keys)))

def sqlize_update(keys) -> str:
    """returns keys and question marks for SQL execute statements, i.e.
        \n(name = ?, address = ?)"""
    return ",".join([f"{key} = ?" for key in keys])


def add_entry(**data):
    sql_keys, sql_huhs = sqlize_insert(data.keys())

    cursor.execute(f'''
        INSERT INTO students({sql_keys}) 
        VALUES({sql_huhs})
    ''', [data[key] for key in STUDENT_SQL_KEYS if key in data.keys()])


def rewrite_entry(entry_id, **data):
    sql_keys = sqlize_update(data.keys())

    cursor.execute(f'''
        UPDATE students
        SET {sql_keys}
        WHERE id = ?
    ''', [data[key] for key in STUDENT_SQL_KEYS if key in data.keys()] + [entry_id])



if __name__ == "__main__":
    #     create_table_students()
    # delete_menu_master()
    # create_table_menu_master()
    # load_into_menu("2weekrotation.txt")
    #     connection.commit()
    #     load_into_table_list(read_from_docx("docx_files/*.docx"))
    new_chel = {"name": "Джаудат Сабиров", "day_month_bday": "20.08", "class": "9Б"}
    add_entry(**new_chel)
    connection.commit()
    connection.close()
