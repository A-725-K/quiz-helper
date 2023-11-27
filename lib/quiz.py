import csv

from lib.parse_exception import ParseException
from lib.question import Question
from lib.header_text import HeaderText


class Quiz:
    """
    Representation of the quiz
    """
    def __init__(self, filename):
        if not filename:
            raise AttributeError(f"No file choosen: {filename}")

        self._questions = []
        self._num_of_questions = 0
        self._from_file(filename)

    @property
    def questions(self):
        """
        Obtain questions
        """
        return self._questions

    def _from_file(self, filename):
        """
        Read questions of the quiz from file
        """
        lines = []
        with open(filename, "r", encoding="utf8") as quiz_file:
            reader = csv.reader(quiz_file, delimiter=",")
            lines = list(reader)

        if len(lines) < 1:
            raise ParseException("Quiz should contain at least a question")

        for i, line in enumerate(lines):
            if len(line) != 3:
                raise ParseException(f"Error at line {i}: Wrong # of fields")
            label = line[0]
            text = line[1]
            answers, correct_answers = self._parse_answers(line[2])
            self._questions.append(
                Question(text, answers, correct_answers, label),
            )
            self._num_of_questions += 1
            # self._questions[i].log()

    def _parse_answers(self, line):
        """
        Collect the answers and separate the correct ones
        """
        answers, correct_answers = [], []
        fields = line.split(":")
        for i, field in enumerate(fields):
            if field.startswith("@"):
                field = field[1:]
                correct_answers.append(i)
            answers.append(field)

        if len(correct_answers) == 0:
            raise ParseException("Questions have at least one correct answer")

        return answers, correct_answers

    def compute_results(self, user_answers):
        """
        Calculate the results of the tests and return a small summary
        """
        if len(user_answers) != self._num_of_questions:
            raise ValueError("Wrong number of answers")

        results = []
        correct, total = 0, 0
        only_correct, only_correct_total = 0, 0
        for qidx, question in enumerate(self._questions):
            n_ans = len(question.answers)
            only_c = len(question.correct_answers)
            total += n_ans
            only_correct_total += only_c
            if question.correct_answers == user_answers[qidx]:
                results.append(1)
                correct += n_ans
                only_correct += only_c
                continue

            got_result = False
            for aidx, _ in enumerate(question.answers):
                if (
                    aidx in question.correct_answers and
                    aidx in user_answers[qidx]
                ):
                    if not got_result:
                        got_result = True
                        results.append(0)
                    correct += 1
                    only_correct += 1
                elif (
                    aidx not in question.correct_answers and
                    aidx not in user_answers[qidx]
                ):
                    correct += 1
            if not got_result:
                results.append(-1)

        return {
            HeaderText.RESULTS: results,
            HeaderText.CORRECT: correct,
            HeaderText.TOTAL: total,
            HeaderText.RATIO: correct / total,
            HeaderText.ONLY_CORRECT: only_correct,
            HeaderText.ONLY_CORRECT_TOTAL: only_correct_total,
            HeaderText.ONLY_CORRECT_RATIO: only_correct / only_correct_total,
            HeaderText.TOTALLY_CORRECT: len(
                list(filter(lambda x: x > 0, results)),
            ),
            HeaderText.PARTIALLY_CORRECT: len(
                list(filter(lambda x: x == 0, results)),
            ),
            HeaderText.TOTALLY_WRONG: len(
                list(filter(lambda x: x < 0, results)),
            ),
            HeaderText.TOTALLY_CORRECT_RATIO: len(
                list(filter(lambda x: x > 0, results)),
            ) / len(self._questions)
        }
