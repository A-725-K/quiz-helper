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

import enum


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
