import re

def is_number(n):
    return re.match(r'^[-+]?[0-9]+\.?[0-9]*$', str(n))

def is_chinese_digits(n):
    return re.match(r'[零壹贰叁肆伍陆柒捌玖拾佰仟萬億角分一二两俩三四五六七八九十百千万亿]+', n)

def chinese2digits(money):
    trad_dict = {
        '零': 0, '〇': 0,
        '壹': 1, '一': 1,
        '贰': 2, '二': 2, '两': 2, '俩': 2,
        '叁': 3, '三': 3,
        '肆': 4, '四': 4,
        '伍': 5, '五': 5,
        '陆': 6, '六': 6,
        '柒': 7, '七': 7,
        '捌': 8, '八': 8,
        '玖': 9, '九': 9,
        '拾': 10, '十': 10,
        '佰': 100, '百': 100,
        '仟': 1000, '千': 1000,
        '萬': 10000, '万': 10000,
        '億': 100000000, '亿': 100000000,
        '角': 0.1,
        '分': 0.01
    }
    if is_chinese_digits(money):
        total = 0.00
        base_unit = 0.001
        dynamic_unit = 0.001
        for i in range(len(money) - 1, -1, -1):
            if money[i] in ['圆', '元', '整']:
                base_unit = 1
                dynamic_unit = 1
                continue
            v = trad_dict.get(money[i])
            if v > 10:
                if v > base_unit:
                    base_unit = v
                else:
                    dynamic_unit = base_unit * v
            elif v < 1:
                base_unit = v
            elif v == 10:
                if i == 0:
                    if dynamic_unit > base_unit:
                        total = total + dynamic_unit * v
                    else:
                        total = total + base_unit * v
                else:
                    dynamic_unit = base_unit * v
            else:
                if dynamic_unit > base_unit:
                    total = total + dynamic_unit * v
                else:
                    total = total + base_unit * v
        return total
