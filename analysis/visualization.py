import re
from analysis.models import Job

def all_list(list1):
    result = {}
    for i in set(list1):
        result[i] = list1.count(i)
    return result


def get_kv(list2):
    lists = []
    for k, v in list2.items():
        lists.append({
            "name": k,
            "value": v
        })
    return lists


def get_three(areas, edu):
    salary = []
    salary1 = []
    salary2 = []
    salary3 = []
    salary4 = []
    salary5 = []
    # 在校/应届 1-3 3-5 5-10 不限
    for x in areas:
        if x["education"] == edu:
            if x["experience"] == "在校生/应届生":
                salary1.append(x["salary"])
            if x["experience"] == "1-3年" or x["experience"] == "1年" or x["experience"] == "2年":
                salary2.append(x["salary"])
            if x["experience"] == "3-4年" or x["experience"] == "3-5年":
                salary3.append(x["salary"])
            if x["experience"] == "5-7年" or x["experience"] == "5-10年":
                salary4.append(x["salary"])
            if x["experience"] == "经验不限" or x["experience"] == "无需":
                salary5.append(x["salary"])
    if len(salary1) > 0:
        salary.append(round(sum(salary1) / len(salary1), 2))
    else:
        salary.append(0)
    salary.append(round(sum(salary2) / len(salary2), 2))
    salary.append(round(sum(salary3) / len(salary3), 2))
    salary.append(round(sum(salary4) / len(salary4), 2))
    salary.append(round(sum(salary5) / len(salary5), 2))
    return salary


def getBar():
    barData = []
    # 升序查找
    for i in Job.objects.all().order_by('jobLabel'):
        barData.append(i.jobLabel)
    bar = []
    barName = []
    barValue = []
    barList = all_list(barData)
    for k in barList.keys():
        barName.append(k)
    for v in barList.values():
        barValue.append(v)
    bar.append(barName)
    bar.append(barValue)
    # print(bar)
    return bar


def getPie():
    compScale = []
    pieData = []
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    c5 = 0
    c6 = 0
    for pie in Job.objects.all():
        compScale.append(pie.companyScale)
    for c in compScale:
        if c == "0-20人":
            c1 += 1
        if c == "20-99人":
            c2 += 1
        if c == "100-499人":
            c3 += 1
        if c == "500-999人":
            c4 += 1
        if c == "1000-9999人":
            c5 += 1
        if c == "10000人以上":
            c6 += 1
    pieData.append(
        {
            "name": "0-20人",
            "value": c1
        })
    pieData.append(
        {
            "name": "20-99人",
            "value": c2
        })
    pieData.append(
        {
            "name": "100-499人",
            "value": c3
        })
    pieData.append(
        {
            "name": "500-999人",
            "value": c4
        })
    pieData.append(
        {
            "name": "1000-9999人",
            "value": c5
        })
    pieData.append(
        {
            "name": "10000人以上",
            "value": c6
        }
    )
    # pieData = get_kv(all_list(compScale))
    # print(pieData)
    return pieData


def getMap():
    mapData = [{'name': '临汾', 'value': 10}, {'name': '西安', 'value': 80},
               {'name': '重庆', 'value': 3641}, {'name': '郑州', 'value': 40},
               {'name': '通辽', 'value': 11}, {'name': '中亭', 'value': 9},
               {'name': '酒仙', 'value': 1}, {'name': '阿城', 'value': 2},
               {'name': '金山', 'value': 1}, {'name': '温州', 'value': 14},
               {'name': '松柏', 'value': 3}, {'name': '新店', 'value': 14},
               {'name': '侨英', 'value': 8}, {'name': '广州', 'value': 730},
               {'name': '西宁', 'value': 2}, {'name': '深圳', 'value': 5786},
               {'name': '青岛', 'value': 97}, {'name': '南宁', 'value': 1},
               {'name': '天津', 'value': 17}, {'name': '白城', 'value': 2},
               {'name': '澄迈', 'value': 1}, {'name': '毕节', 'value': 1},
               {'name': '合肥', 'value': 8}, {'name': '武汉', 'value': 3827},
               {'name': '大庆', 'value': 2}, {'name': '珠海', 'value': 38},
               {'name': '嘉莲', 'value': 2}, {'name': '南昌', 'value': 12},
               {'name': '廊坊', 'value': 2}, {'name': '贵阳', 'value': 33},
               {'name': '开元', 'value': 16}, {'name': '昆明', 'value': 5},
               {'name': '福州', 'value': 51}, {'name': '石家', 'value': 1},
               {'name': '漳州', 'value': 20}, {'name': '厦禾', 'value': 2},
               {'name': '成都', 'value': 64}, {'name': '马尾', 'value': 1},
               {'name': '杭州', 'value': 3077}, {'name': '新民', 'value': 1},
               {'name': '鳌峰', 'value': 1}, {'name': '南京', 'value': 3046},
               {'name': '常州', 'value': 2}, {'name': '莆田', 'value': 25},
               {'name': '福建', 'value': 34}, {'name': '贵港', 'value': 18},
               {'name': '康乐', 'value': 1}, {'name': '南充', 'value': 1},
               {'name': '金华', 'value': 12}, {'name': '北京', 'value': 8186},
               {'name': '昆山', 'value': 9}, {'name': '衢州', 'value': 10},
               {'name': '无锡', 'value': 7}, {'name': '济南', 'value': 4},
               {'name': '厦门', 'value': 8788}, {'name': '苏州', 'value': 13},
               {'name': '珠江', 'value': 17}, {'name': '厦港', 'value': 20},
               {'name': '禾山', 'value': 15}, {'name': '德州', 'value': 10},
               {'name': '河源', 'value': 1}, {'name': '佛山', 'value': 8},
               {'name': '汕头', 'value': 1}, {'name': '金尚', 'value': 2},
               {'name': '宁波', 'value': 3}, {'name': '滨海', 'value': 6},
               {'name': '长沙', 'value': 24}, {'name': '丹东', 'value': 23},
               {'name': '前埔', 'value': 15}, {'name': '泉州', 'value': 850},
               {'name': '软件', 'value': 25}, {'name': '台江', 'value': 10},
               {'name': '上海', 'value': 5288}, {'name': '宁德', 'value': 50},
               {'name': '鹭江', 'value': 19}, {'name': '东莞', 'value': 15},
               {'name': '福清', 'value': 12}, {'name': '芜湖', 'value': 11}]

    return mapData


def getArea():
    area = []
    areaData = []
    salary = []
    for a in Job.objects.all():
        sal = [int(s) for s in re.findall("\d+", a.salary)]
        if len(sal) == 0:
            sal = [0]

        area.append({
            "education": a.education,
            "experience": a.experience,
            # "salary": "".join(list(filter(str.isdigit, a.salary)))
            "salary": sum(sal) / len(sal)
        })
    # print(sal)
    education = ["大专", "本科", "硕士", "不限"]
    experience = ["在校生/应届生", "1-3年", "3-5年", "5-10年", "经验不限"]
    areaData.append(experience)
    for i in education:
        salary.append(get_three(area, i))
    areaData.append(salary)
    # print(areaData)
    return areaData


def getRadar():
    radarData = []
    techs = []
    tech = []
    # .NET
    countNet = 0
    # python
    countPy = 0
    # java
    countJava = 0
    # c
    countC1 = 0
    # c#
    countC0 = 0
    # c++
    countC2 = 0
    # php
    countPhp = 0
    # html
    countH5 = 0
    # node.js
    countNode = 0
    # css
    countCss = 0
    # javascript
    countJs = 0
    # 全栈
    countAll = 0
    for r in Job.objects.all():
        techs.append(r.technology)
    for t in techs:
        if ".net" in t or ".NET" in t:
            countNet += 1
        if "python" in t or "Python" in t or "PYTHON" in t:
            countPy += 1
        if "java" in t or "Java" in t or "JAVA" in t:
            countJava += 1
        if "c语言" in t or "C语言" in t:
            countC1 += 1
        if "c#" in t or "C#" in t:
            countC0 += 1
        if "c++" in t or "C++" in t:
            countC2 += 1
        if "php" in t or "Php" in t or "PHP" in t:
            countPhp += 1
        if "html" in t or "Html" in t or "HTML" in t or "H5" in t:
            countH5 += 1
        if "node.js" in t or "Node.js" in t:
            countNode += 1
        if "css" in t or "CSS" in t:
            countCss += 1
        if "javascript" in t or "JavaScript" in t:
            countJs += 1
        if "全栈" in t:
            countAll += 1
    radarData.append(['技术栈'])
    tech.append(countAll)
    tech.append(countNet)
    tech.append(countPy)
    tech.append(countJava)
    tech.append(countC0)
    tech.append(countC1)
    tech.append(countC2)
    tech.append(countPhp)
    tech.append(countH5)
    tech.append(countNode)
    tech.append(countCss)
    tech.append(countJs)
    radarData.append(tech)
    # print(tech)
    return radarData
