import openpyxl
from openpyxl.comments import Comment


class CreateTemplate:
    def __init__(self, path):
        self.path = path

    def template_filling(self):
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            question_cell = sheet['A1']
            question_cell.value = 'ВОПРОС'
            question_cell_hint = sheet['A2']
            question_cell_hint.comment = Comment(text="колонка для записи вопросов (начинать с этой строки)",
                                                 author='<NAME>')
            answer_cell = sheet['B1']
            answer_cell.value = 'ОТВЕТ'
            answer_cell_hint = sheet['B2']
            answer_cell_hint.comment = Comment(text="колонка для записи ответов (начинать с этой строки)",
                                               author='<NAME>')
            clue_cell = sheet['C1']
            clue_cell.value = 'ПОДСКАЗКА'
            clue_cell_hint = sheet['C2']
            clue_cell_hint.comment = Comment(text="колонка для записи подсказок (начинать с этой строки)",
                                             author='<NAME>')
            workbook.save(self.path)

        except Exception:
            return "Error"
