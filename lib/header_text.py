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
