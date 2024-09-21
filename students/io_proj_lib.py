import glob
from docx import Document


def read_from_docx(location):
    output = list()
    for file_name in glob.glob(location):
        word_doc = Document(file_name)
        for table in word_doc.tables:
            for row in table.rows:
                base_line = list(map(lambda x: x.text.strip(), row.cells))
                if "Дата" in base_line[2] or len(base_line[1]) == 0:
                    continue
                student_line = base_line[1:]
                student_line.append(file_name[file_name.rfind("\\") + 1:file_name.find(" ")].strip())
                line = formalize_bday(student_line)
                output.append(line)
    return output


def formalize_bday(line):
    day, month, year = line[1].split(".")
    return [line[0], f"{day}.{month}", year, line[2]]


def import_menu(location):
    output_list = []
    with open(location, "r", encoding='utf8') as filename:
        point_menu = []
        for line in filename:
            if line.strip("\n").strip() not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
                if line.strip():
                    if line.strip("\n").strip() not in ["Завтрак", "Обед", "Полдник", "Первый ужин", "Второй ужин"]:
                        line = f"* {line}"
                    else:
                        line = f"\n{line}"
                    point_menu.append(f"{line}")
            else:
                point_menu = "".join(point_menu)
                if point_menu:
                    output_list.append(point_menu)
                point_menu = []
    return output_list


def import_line(location, line_pos):
    with open(location, "r", encoding='utf8') as filename:
        for j, k in enumerate(filename):
            # Если номер строки соответствует номеру в аргументе, то:
            if j == line_pos:
                k = [*k.split("\t"), location[location.index("/") + 1:location.index(".")]]
                # Избавляемся от нежелательных символов
                for u in range(len(k)):
                    if u >= len(k):
                        continue
                    k[u] = k[u].rstrip("\n")
                    k = [u for u in k if u]
                filename.close()
                return k


def how_many_lines(location):
    c = 0
    with open(location, "r", encoding='utf8') as filename:
        for _ in filename:
            c += 1
    return c
