# quiz-helper: Test your knowledge and revise important topics.
#
# Copyright (C) 2023 A-725-K (Andrea Canepa)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

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
