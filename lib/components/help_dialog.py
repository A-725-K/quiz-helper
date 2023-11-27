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


class HelpDialog(tk.Toplevel):
    """
    Help dialog window
    """
    def __init__(self, parent, icon_img):
        super().__init__(parent)

        self.title("Quiz Helper v. 1.0")
        self.geometry("620x240")
        self.resizable(False, False)
        self.bind("<Return>", self._ok_handler)
        self.wm_iconphoto(False, icon_img)

        upper_frame = tk.Frame(master=self)
        lower_frame = tk.Frame(master=self)

        self._img = icon_img

        text = """
        Quiz Helper v. 1.0 is a tool to help you focus on your knowledge
        base as well as prepare fun quiz to share with other people!
        It provides a straightforward interface to let anyone starts
        ASAP without any difficulties in the setup of the session.

        Developed in Python3 with the aid of the TKinter framework.
        """

        tk.Label(master=upper_frame, image=self._img).pack(side=tk.LEFT)
        tk.Label(
            master=upper_frame,
            text=text,
            justify=tk.LEFT,
            font=("Helvetica", 12),
        ).pack(side=tk.LEFT)
        tk.Button(
            master=lower_frame,
            text="Got it!",
            font=("Helvetica", 16),
            width=20,
            cursor="hand1",
            bg="black",
            fg="orange",
            activebackground="orange",
            activeforeground="black",
            command=self._ok_handler,
        ).pack()

        upper_frame.pack(padx=10, pady=10)
        lower_frame.pack(pady=20)

    def _ok_handler(self, _event=None):
        """
        Handle ok/close button
        """
        self.destroy()
