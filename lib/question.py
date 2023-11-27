from dataclasses import dataclass


@dataclass
class Question:
    """
    Representation of questions of the quiz
    """
    def __init__(self, text, answers, correct_answers, label=""):
        if not text:
            raise ValueError("Question cannot have empty text")
        if len(answers) < 1:
            raise ValueError("Question must have at least an answer")
        if len(correct_answers) < 1:
            raise ValueError("Question must have at least one correct answer")

        self.text = text
        self.label = label
        self.answers = answers
        self.correct_answers = correct_answers
        self.number_of_answers = len(self.answers)

    def log(self):
        print(f"[LABEL]: {self.label}")
        print(f"[QUESTION]: {self.text}")
        print("[ANSWERS]:")
        for j, ans in enumerate(self.answers):
            print(f"{j}) {ans}")
        print("[CORRECT ANSWERS]:")
        for j, ans in enumerate(self.correct_answers):
            print(f"{j}) {ans}")
        print("\n")
