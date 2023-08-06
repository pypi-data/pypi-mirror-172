from enum import Enum, auto, unique
from typing import List


@unique
class ActivityTimeStatus(Enum):
    BEFORE = auto()
    NOW = auto()
    AFTER = auto()


@unique
class Columns(Enum):
    """Columns to use in activities table."""
    START = "Start"
    END = "End"
    TOTAL = "Total"
    ETA = "ETA"
    TITLE = "Title"
    VARIATION = "Variation"
    STATUS = "Status"

    @classmethod
    def parse_str(cls, input_str: str) -> List:
        """Parse column names and return list of columns."""
        result = []
        words_1 = input_str.split(",")
        words_2 = input_str.split()
        if len(words_2) > len(words_1):
            words = words_2
        else:
            words = words_1
        for word in words:
            for element in cls:
                if element.value.upper() == word.upper():
                    result.append(element)
        return result
