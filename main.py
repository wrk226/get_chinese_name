from pypinyin import pinyin, lazy_pinyin, Style
from name_set import get_source


def check_pinyin(name, constrain):
    for i in lazy_pinyin(name):
        if i in constrain:
            return True
    return False


def check_init(name, constrain):
    for i in pinyin(name, style=Style.FIRST_LETTER):
        if i in constrain:
            return True
    return False


def check_character(name, constrain):
    for i in name:
        if i in constrain:
            return True
    return False


# 长辈姓名--删掉所有读音相同的字--例：加入“伟”，则结果中不会出现任何读音为we的字（为伟位微卫...）
banned_list = lazy_pinyin("可悦思平笑华世永念沁建宏中人春山雨国清溪瑞峰")
# 名字开头字母--删掉所有以此字母开头的字--例：加入“w”，则结果中不会出现任何拼音以w开头的字（卫瓦望卧...）
bad_init = list("eqrsxy")
# 不想要的名字--删掉所有相同的字--例：加入“贵”，则结果中不会出现“贵”字
bad_words = list("富贵民国军卫义二三四"
                 "介少大毛伟帅攻立生田"
                 "水火金木土才花凤龙春"
                 "艳芳淑杰俊志强昌银婷"
                 "丽芬发梅蛋铁铜娜宝春"
                 "夏秋冬武力天地圣神佛"
                 "老乾坤云")
# 笔画数--名字的笔画总数的范围--例：王伟，名字笔画总数为6（不计姓氏）
stroke_number = [0, 200]

# 字数--名字的字数--例：王伟，字数为1
character_number = 2

# 姓--不会影响名字的生成，仅仅影响输出
last_name = "王"

# 允许叠字--例：欢欢，西西
replicate = False

# 选择词库
# 0: "默认", 1: "诗经", 2: "楚辞", 3: "论语",
# 4: "周易", 5: "唐诗", 6: "宋诗", 7: "宋词"
# 8: 自定义
name_source = 1

# 是否筛选名字--仅输出默认库中存在的名字
name_validate = True

# 是否筛选性别--仅输出与默认库中对应名字性别相同的名字--仅当开启名字筛选时有效
filter_gender = True

# 性别--男/女--仅当开启名字筛选时有效
gender = "女"

names = list()
with open("names.txt", "w+", encoding='utf-8') as f:
    for i in get_source(name_source, name_validate, character_number):
        if i.stroke_number < stroke_number[0] or stroke_number[1] < i.stroke_number:
            continue
        if i.count != character_number:
            continue
        if name_validate and filter_gender and (i.gender != gender or i.gender=="双"):
            continue
        if check_init(i.first_name, bad_init):
            continue
        if check_pinyin(i.first_name, banned_list):
            continue
        if check_character(i.first_name, bad_words):
            continue
        if not replicate and i.first_name[0] == i.first_name[1]:
            continue
        names.append(i)
    print(">>正在输出结果...")
    names.sort()
    for i in names:
        f.write(last_name + str(i) + "\n")
    print(">>输出完毕，请查看目录中的\"names.txt\"文件")
