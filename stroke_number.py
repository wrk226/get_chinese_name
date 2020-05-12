stroke_dic = dict()
with open('data/stoke.dat', encoding='utf-8') as f:
    data = f.readlines()
    for string in data:
        temp = string.split("|")
        temp[2] = temp[2].replace("\n", "")
        stroke_dic[temp[1]] = int(temp[2])


def get_stroke_number(word):
    total = 0
    for i in word:
        total += stroke_dic[i]
    return total
