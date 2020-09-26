from name import Name
import jieba
import jieba.posseg as pseg
import json
from opencc import OpenCC
import re


def get_source(source, validate, character_number):
    print(">>开始生成词库...")
    jieba.enable_paddle()
    exist_name = dict()
    if validate:
        print(">>正在加载验证词库...")
        get_name_valid('Chinese_Names', exist_name)

    print(">>正在加载姓名词库...")
    print("**某些词库可能非常大，需要加载一段时间，请耐心等待**")
    names = set()

    # 默认
    if source == 0:
        if validate:
            names = exist_name
        else:
            get_name_dat('Chinese_Names', names, character_number)
    # 诗经
    elif source == 1:
        get_name_json('诗经/shijing', names, 'content', character_number)
    # 楚辞
    elif source == 2:
        get_name_txt('楚辞', names, character_number)
    # 论语
    elif source == 3:
        get_name_json("论语/lunyu", names, 'paragraphs', character_number)
    # 周易
    elif source == 4:
        get_name_txt('周易', names, character_number)
    # 唐诗
    elif source == 5:
        for i in range(0, 58000, 1000):
            get_name_json('唐诗/poet.tang.' + str(i), names, 'paragraphs',
                          character_number)
    # 宋诗
    elif source == 6:
        for i in range(0, 255000, 1000):
            get_name_json('宋诗/poet.song.' + str(i), names, 'paragraphs',
                          character_number)
    # 宋词
    elif source == 7:
        for i in range(0, 22000, 1000):
            get_name_json('宋词/ci.song' + str(i), names, 'paragraphs',
                          character_number)
    # 自定义词库
    elif source == 8:
        get_name_txt('自定义', names, character_number)
    else:
        print("词库序号输入错误")

    # 检查名字是否存在并添加性别
    if validate:
        print(">>正在验证姓名词库...")
        if source != 0:
            names = get_intersect(names, exist_name)

    print(">>正在筛选名字...")
    return names


def get_intersect(names, exist_name):
    result = set()
    for i in names:
        if i.first_name in exist_name.keys():
            i.gender = exist_name[i.first_name]
            result.add(i)
    return result


def get_name_valid(path, exist_names):
    with open('data/' + path + '.dat', encoding='utf-8') as f:
        for line in f:
            data = line.split(",")
            name = data[0][1:]
            gender = data[1].replace("\n", "")
            if name in exist_names:
                if gender != exist_names.get(name) or gender == "未知":
                    exist_names[name] = "双"
            else:
                exist_names[name] = gender


def get_name_dat(path, names, character_number):
    with open('data/' + path + '.dat', encoding='utf-8') as f:
        for line in f:
            data = line.split(",")
            name = data[0][1:]
            gender = data[1].replace("\n", "")
            if len(name) == character_number:
                names.add(Name(name, "", gender))


# 如果使用繁体字文章可以将注释部分取消，自动转化成简体
def get_name_txt(path, names, character_number):
    # cc = OpenCC('t2s')
    with open('data/' + path + '.txt', encoding='utf-8') as f:
        for string in f:
            # string = cc.convert(string)
            name = re.search(r'\w', string)
            if name is None:
                continue
            string_list = re.split("！？，。,.?! \n", string)
            for sentence in string_list:
                words = pseg.cut(sentence, use_paddle=True)
                for word, flag in words:
                    name = re.match(
                        r'^([\u4e00-\u9fa5]){' + str(character_number) + '}$',
                        word)
                    if name is not None:
                        names.add(Name(name.string, string, ""))


def get_name_json(path, names, column, character_number):
    cc = OpenCC('t2s')
    with open('data/' + path + '.json', encoding='utf-8') as f:
        data = json.loads(f.read())
        for j in range(0, len(data)):
            for string in data[j][column]:
                string = cc.convert(string)
                string_list = re.split("！？，。,.?! \n", string)
                for sentence in string_list:
                    words = pseg.cut(sentence, use_paddle=True)
                    for word, flag in words:
                        name = re.match(
                            r'^([\u4e00-\u9fa5]){' + str(
                                character_number) + '}$',
                            word)
                        if name is not None:
                            names.add(Name(name.string, string, ""))
