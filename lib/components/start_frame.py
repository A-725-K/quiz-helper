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
import tkinter.filedialog as fd
from tkinter import messagebox

from lib.datatypes.quiz import Quiz
from lib.components.help_dialog import HelpDialog
from lib.exceptions.parse_exception import ParseException


class StartFrame(tk.Frame):
    """
    Initial menu
    """
    def __init__(self, parent, icon_img):
        super().__init__(parent, bg='linen')
        self._parent = parent
        self._icon_img = icon_img

        tk.Button(
            master=self,
            text="Start Quiz",
            width=30,
            font=("Arial", 20),
            height=4,
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=self._start_handler,
        ).grid(row=0, column=0, padx=30, pady=20)

        tk.Button(
            master=self,
            text="About",
            width=16,
            font=("Helvetica", 16),
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=self._help_handler,
        ).grid(row=1, column=0)

        tk.Button(
            master=self,
            text="Quit",
            width=16,
            font=("Helvetica", 16),
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=parent.quit,
        ).grid(row=2, column=0, pady=10)

    def _help_handler(self):
        """
        Handle help button
        """
        HelpDialog(self, self._icon_img)

    def _start_handler(self):
        """
        Handle start quiz button
        """

        filetypes = (
            ("csv files", "*.csv"),
            ("All files", "*.*")
        )

        filename = ""
        quiz = None
        while not quiz:
            try:
                file = fd.askopenfile(filetypes=filetypes)
                if file is not None:
                    filename = file.name
                print(f"Input file chosen: {filename}")
                quiz = Quiz(filename)
            except AttributeError:
                print("No file choosen")
                return
            except (UnicodeDecodeError, ParseException):
                messagebox.showerror(
                    title="File error",
                    message="File not supported or malformed!",
                )
                file = None
                filename = None

        # forward quiz data structure to the controller
        self._parent.set_quiz(quiz)
