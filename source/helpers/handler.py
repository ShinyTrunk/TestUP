import openpyxl


class Handler:
    def __init__(self, path):
        self.path = path

    def processing(self):
        try:
            questions_pack = []

            workbook = openpyxl.load_workbook(self.path)
            workbook.active = 0
            sheet = workbook.active

            for index in list(sheet.values)[1:]:
                questions_pack.append(list(index[:]))

            return questions_pack

        except Exception:
            return "Error"
