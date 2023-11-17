#!/usr/bin/env python3

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

"""
Program to test my knowledge with multiple choice quizzes
"""
import csv
import enum
import tkinter as tk
import tkinter.filedialog as fd
from dataclasses import dataclass
from PIL import ImageTk, Image
from tkinter import messagebox

__version__ = '1.0'
__author__ = 'A-725-K (Andrea Canepa)'


class ParseException(Exception):
    """
    To represent a generic parsing errors in input files
    """


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

        # forward quiz data structure to the controller
        self._parent.set_quiz(quiz)


class HeaderText(enum.Enum):
    RESULTS = "results"
    CORRECT = "correct answers"
    TOTAL = "total answers"
    RATIO = "correct answer %"
    ONLY_CORRECT = "only correct"
    ONLY_CORRECT_TOTAL = "only correct total"
    ONLY_CORRECT_RATIO = "only correct %"
    TOTALLY_CORRECT = "totally correct"
    PARTIALLY_CORRECT = "partially correct"
    TOTALLY_WRONG = "totally wrong"
    TOTALLY_CORRECT_RATIO = "totally correct %"


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


class MainWindow(tk.Tk):
    """
    Main window of the application
    """
    def __init__(self):
        super().__init__()

        self._quiz = None
        self._icon_img = ImageTk.PhotoImage(
            Image.open("res/imgs/icon.png").resize((100, 100)),
        )
        self._background_img = ImageTk.PhotoImage(
            Image.open("res/imgs/background.jpg").resize((720, 480)),
        )

        self.title("Quiz Helper")
        self.geometry("720x480")
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


def main():
    """
    Entry point
    """
    MainWindow().start()


if __name__ == "__main__":
    main()
