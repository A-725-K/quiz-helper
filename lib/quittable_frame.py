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


class QuittableFrame(tk.Frame):
    """
    Abstraction that provides a method to exit or restart the session
    """
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

    def handle_quit(self):
        """
        Give the user the possibility to start a new quiz session or exit the
        program
        """
        for c in self.winfo_children():
            c.destroy()
        self.destroy()
        should_quit = messagebox.askyesno(
            title="Restart or exit",
            message="Do you want to exit the program?\n"
                    f"{' '*4}'YES' will exit\n"
                    f"{' '*4}'NO' will go back to the home page",
        )
        if should_quit:
            self._parent.quit()
            return

        print("Start a new session")
        self._parent.restart()
