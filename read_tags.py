class Read_tags:

    def __init__(self, filename):
        self.file = open(filename, "r", encoding="UTF-8")

    def get_tags_list(self):
        return list(map(lambda line: line.replace("\n", ""), self.file.readlines()))

