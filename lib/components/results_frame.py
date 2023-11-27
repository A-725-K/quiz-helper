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

from lib.components.quittable_frame import QuittableFrame
from lib.enums.header_text import HeaderText


class ResultsFrame(QuittableFrame):
    """
    Display results of the test
    """
    def __init__(self, parent, quiz, summary):
        super().__init__(parent)

        self._parent = parent
        self._quiz = quiz
        self._summary = summary

        self._log_summary()

        for idx, (head, value) in enumerate(self._summary.items()):
            if head == HeaderText.RESULTS:
                continue
            t_entry = tk.Entry(self, font=('Arial', '14'), bd=2)
            t_entry.grid(row=idx, column=0, padx=20, pady=3)
            t_entry.insert(tk.END, head.value.title())
            t_entry.configure(
                cursor="arrow",
                state=tk.DISABLED,
                disabledforeground="black",
                disabledbackground="white",
            )
            t_entry = tk.Entry(self, font=('Arial', '14'), bd=2)
            t_entry.grid(row=idx, column=1, padx=20, pady=3)
            if head.name.endswith('RATIO'):
                value = f"{value:.2%}"
            t_entry.insert(tk.END, value)
            t_entry.configure(
                cursor="arrow",
                state=tk.DISABLED,
                disabledforeground="black",
                disabledbackground="white",
            )

        tk.Button(
            master=self,
            text="View Correction",
            font=("Arial", 12),
            height=2,
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=self._handle_view_answers,
        ).grid(row=len(self._summary), column=0, padx=30, pady=10)
        tk.Button(
            master=self,
            text="Quit",
            font=("Arial", 12),
            height=2,
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=super().handle_quit,
        ).grid(row=len(self._summary), column=1, padx=30, pady=10)

    def _handle_view_answers(self):
        self.destroy()
        self._parent.show_correction()

    def _log_summary(self):
        print("Summary:")
        for target, value in self._summary.items():
            print(f"  {target.value}: {value}")
