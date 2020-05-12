from pypinyin import lazy_pinyin
from stroke_number import get_stroke_number


class Name:
    __slots__ = "first_name", "stroke_number", "count", "index", "source", "gender"

    def __init__(self, first_name, source, gender):
        self.first_name = first_name
        self.stroke_number = get_stroke_number(first_name)
        self.count = len(first_name)
        self.index = ""
        spell = lazy_pinyin(first_name)
        for word in spell:
            self.index += word
        self.source = source
        self.gender = gender

    def __eq__(self, other):
        return self.index == other.index

    def __ne__(self, other):
        return not self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

    def __str__(self):
        return self.first_name + "\t" + str(
            self.gender)+"\t"+str(self.stroke_number) + "\t" + self.source

    def __hash__(self):
        return hash(self.first_name)
