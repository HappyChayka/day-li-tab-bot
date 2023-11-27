import glob


def import_list(location):
    for i in glob.glob(location):
        with open(i, "r", encoding='utf8') as filename:
            for each_line in filename:
                k = [*each_line.split("\t"), i[:i.index(".")]]
                for u in range(len(k)):
                    if u >= len(k):
                        continue
                    k[u] = k[u].rstrip("\n")
                    k = [u for u in k if u]
                return k
