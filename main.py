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
Program to test knowledge with multiple choice quizzes
"""

__version__ = '1.0'
__author__ = 'A-725-K (Andrea Canepa)'

from lib.components.main_window import MainWindow


def main():
    """
    Entry point
    """
    MainWindow(800, 600).start()


if __name__ == "__main__":
    main()
