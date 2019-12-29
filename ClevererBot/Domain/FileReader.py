import markdown
import re

class FileReader:
   
    def markdownToQA(self, file):
        questions_and_answers = []
        for faq in file.read().split("##"):

            if faq.strip():
                print(faq)
                qa = faq.split("?")
                questions_and_answers.append(QA(qa[0] + "?", qa[1]))
        return QACollection(questions_and_answers)

    def read_file_from_path(self, path):
        f = open(path, 'r')
        return f.read()