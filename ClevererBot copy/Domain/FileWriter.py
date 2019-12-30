class FileWriter:
    def write_file(self, title, data):
        f = open(title, "w+")
        for el in data:
            f.write(el)
        f.close()