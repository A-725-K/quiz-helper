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
from PIL import ImageTk, Image
from tkinter import messagebox

from lib.components.results_frame import ResultsFrame
from lib.components.start_frame import StartFrame
from lib.components.quiz_ui import QuizUI


class MainWindow(tk.Tk):
    """
    Main window of the application
    """
    def __init__(self, width, height):
        super().__init__()

        self._quiz = None
        self._icon_img = ImageTk.PhotoImage(
            Image.open("res/imgs/icon.png").resize((100, 100)),
        )
        self._background_img = ImageTk.PhotoImage(
            Image.open("res/imgs/background.jpg").resize((width, height)),
        )

        self.title("Quiz Helper")
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.wm_iconphoto(False, self._icon_img)

        self._bg = tk.Label(self, image=self._background_img)
        self._bg.place(x=0, y=0, relwidth=1, relheight=1)

        self._end = tk.BooleanVar()
        self._start_frm = StartFrame(self, self._icon_img)
        self._results_frm = None

        # Custom logic when pressing "X" button to close the program
        # self.protocol('WM_DELETE_WINDOW', self._ask_exit_program)

        self._end.set(False)
        self._end.trace_add('write', self._handle_terminate)
        self._start_frm.pack(side=tk.BOTTOM, expand=True)

    def restart(self):
        """
        Restart the quiz from scratch
        """
        assert self._results_frm is not None
        self._results_frm.destroy()
        self._start_frm.destroy()
        self._end.set(False)
        self._quiz = None
        self._start_frm = StartFrame(self, self._icon_img)
        self._start_frm.pack(side=tk.BOTTOM, expand=True)

    def show_correction(self):
        self._results_frm = QuizUI(self, self._quiz, True, self._user_answers)
        self._results_frm.pack(side=tk.BOTTOM, expand=True)

    def _ask_exit_program(self):
        """
        Ask for confirmation when quitting the program
        """
        exit_ok = messagebox.askyesno(
            message="Do you want to quit?",
            title="Quiz Helper",
        )
        if exit_ok:
            self.quit()

    def _handle_terminate(self, _var, _index, _mode):
        """
        Show results and ask if want to exit or continue
        """
        if self._quiz is None:
            raise ValueError("Quiz cannot be undefined at this point")
        if not self._end.get():
            return
        summary = self._quiz.compute_results(self._user_answers)
        self._release_children(self)
        self._results_frm = ResultsFrame(self, self._quiz, summary)
        self._results_frm.pack(side=tk.BOTTOM, expand=True, pady=20)

    def _release_children(self, item):
        """
        Release all allocated items
        """
        for child in item.winfo_children():
            self._release_children(child)
        if item not in (self, self._bg):
            item.destroy()

    def terminate_quiz(self, user_answers):
        """
        Terminate the quiz and trigger the observer
        """
        self._user_answers = user_answers
        self._end.set(True)

    def set_quiz(self, value):
        """
        Receive quiz data structure
        """
        if value is None:
            raise ValueError("Quiz data structure cannot be none")
        self._quiz = value
        self._start_frm.pack_forget()
        print("Quiz is ready")
        QuizUI(self, self._quiz).pack(side=tk.BOTTOM, expand=True)

    def start(self):
        """
        Start the application
        """
        self.mainloop()
