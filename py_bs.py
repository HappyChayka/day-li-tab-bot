import glob
import fileinput

for i in glob.glob("*.txt"):
    with open(i, "a", encoding="utf8") as new_file:
        with open(i, "r", encoding="utf8") as old_file:
            for each_line in old_file:
                last_dot_case = each_line.rfind(".")
                each_line = each_line[:last_dot_case] + "\t" + each_line[last_dot_case + 1:]
                new_file.write(each_line)

