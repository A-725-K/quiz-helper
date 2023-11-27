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

import tkinter as tk
from tkinter import messagebox

from lib.quittable_frame import QuittableFrame
from lib.question_frame import QuestionFrame


class QuizUI(QuittableFrame):
    """
    UI for the quiz flow
    """
    def __init__(self, parent, quiz, show_results=False, user_answers=[]):
        super().__init__(parent)

        self._parent = parent
        self._quiz = quiz
        self._curr_idx = 0
        self._user_answers = user_answers

        self._questions_frames = []
        for qidx, question in enumerate(self._quiz.questions):
            self._questions_frames.append(
                QuestionFrame(
                    self,
                    question,
                    show_results,
                    self._user_answers[qidx] if show_results else [],
                ),
            )
        self._num_of_questions = len(self._questions_frames)
        self._questions_frames[self._curr_idx].pack()

        self._lower_third = tk.Frame(self._parent, bg='linen')
        self._lower_third_lower = tk.Frame(self._lower_third, bg='linen')
        self._idx_label = tk.Label(
            self._lower_third,
            text=f"{self._curr_idx + 1}/{self._num_of_questions}",
            font=("Helvetica", 16),
            bg='linen',
        )
        self._idx_label.pack(pady=5)
        self._prev_btn = tk.Button(
            self._lower_third_lower,
            text="<< Prev",
            font=("Helvetica", 16),
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=self._prev_handler,
            state=tk.DISABLED,
        )
        self._prev_btn.pack(side=tk.LEFT, padx=20, pady=5)
        self._next_btn = tk.Button(
            self._lower_third_lower,
            text="Next >>",
            font=("Helvetica", 16),
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=self._next_handler,
        )
        self._next_btn.pack(side=tk.RIGHT, padx=20, pady=5)

        if not show_results:
            self._submit_btn = tk.Button(
                self._lower_third_lower,
                text="Submit!",
                font=("Helvetica", 16),
                cursor="hand1",
                bg="black",
                fg="orange",
                activebackground="orange",
                activeforeground="black",
                command=self._handle_submit,
            )
        else:
            self._submit_btn = tk.Button(
                self._lower_third_lower,
                text="Quit",
                font=("Helvetica", 16),
                cursor="hand1",
                bg="black",
                fg="orange",
                activebackground="orange",
                activeforeground="black",
                command=self._handle_quit,
            )

        self._submit_btn.pack(padx=20, pady=5)
        self._lower_third_lower.pack()
        self._lower_third.pack(side=tk.BOTTOM, pady=20)

    def _handle_quit(self):
        """
        Give the user the possibility to start a new session or exit the
        program
        """
        self._lower_third.destroy()
        super().handle_quit()

    def _handle_submit(self):
        """
        Submit the answers and check the results
        """
        msg = "Are you sure you want to submit your answers and terminate " \
              "the quiz?"
        submit_ok = messagebox.askyesno(title="Submit results", message=msg)
        if not submit_ok:
            return
        print("Answers submitted")
        self._lower_third.destroy()
        self.destroy()
        self._parent.terminate_quiz(
            [
                [idx for idx, choice in enumerate(qsf.choices) if choice.get()]
                for qsf in self._questions_frames
            ]
        )

    def _btn_handler(self, inc):
        """
        Hide or show frames based of the current index
        """
        self._questions_frames[self._curr_idx].pack_forget()
        self._curr_idx = (self._curr_idx + inc) % self._num_of_questions
        self._idx_label.configure(
            text=f"{self._curr_idx + 1}/{self._num_of_questions}",
        )
        self._idx_label.update()
        self._questions_frames[self._curr_idx].pack()

        prev_state, next_state = tk.NORMAL, tk.NORMAL
        prev_cursor, next_cursor = "hand1", "hand1"
        if self._curr_idx == 0:
            prev_state = tk.DISABLED
            prev_cursor = ""
        if self._curr_idx == self._num_of_questions - 1:
            next_state = tk.DISABLED
            next_cursor = ""

        self._prev_btn.config(state=prev_state, cursor=prev_cursor)
        self._next_btn.config(state=next_state, cursor=next_cursor)

    def _prev_handler(self):
        """
        Go to the previous question
        """
        if self._curr_idx == 0:
            return
        self._btn_handler(-1)

    def _next_handler(self):
        """
        Go to the next question
        """
        if self._curr_idx == self._num_of_questions - 1:
            return
        self._btn_handler(1)
