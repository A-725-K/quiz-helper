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


class QuestionFrame(tk.Frame):
    """
    UI for displaying the user a question and the related answers
    """
    def __init__(self, parent, question, show_results=False, user_answers=[]):
        super().__init__(parent, bg='linen')

        self._choices = []
        self._checkboxes = []

        tk.Label(
            master=self,
            text=question.text,
            wraplength=600,
            justify=tk.LEFT,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief=tk.RIDGE,
            padx=10,
            pady=5,
            bg="LemonChiffon2"
        ).pack(fill=tk.X, expand=True, padx=20, pady=10)

        for idx, ans in enumerate(question.answers):
            self._choices.append(tk.BooleanVar())
            text_color = "black"
            check_state = tk.NORMAL
            if show_results:
                check_state = tk.DISABLED
                if idx in question.correct_answers and idx in user_answers:
                    text_color = "green"
                elif idx in question.correct_answers or idx in user_answers:
                    text_color = "red"

            chkb = tk.Checkbutton(
                master=self,
                text=f" {ans}",
                variable=self._choices[idx],
                wraplength=600,
                font=("Courier", 10),
                onvalue=True,
                offvalue=False,
                height=2,
                padx=10,
                cursor="hand1",
                bg='linen',
                highlightthickness=0, bd=0,
                justify=tk.LEFT,
                compound=tk.LEFT,
                state=check_state,
                disabledforeground=text_color,
            )
            chkb.pack(anchor="w")

            if show_results and idx in user_answers:
                chkb.select()

    @property
    def choices(self):
        """
        The choices property
        """
        return self._choices
