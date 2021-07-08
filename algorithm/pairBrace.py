import re


class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self, data):
        """
        进栈函数
        """
        self.stack.append(data)

    def pop(self):
        """
        出栈函数，
        """
        return self.stack.pop()

    def get_top(self):
        """
        取栈顶
        """
        return self.stack[-1]


def get_content_between_brace(content: str, brace_number: int, b_type: [str]):
    brace_number -= 1
    stack = Stack()
    res = {}
    try:
        for i in range(0, len(content)):
            if content[i] == b_type[0]:
                stack.push({b_type[0]: i})
            elif content[i] == b_type[1]:
                frame = stack.pop()
                res[frame[b_type[0]]] = i
    except LookupError:
        print("错误 缺少 { 或者 } , index: ", i)
    print()
    li = list(res.keys())
    li.sort()
    # return li[brace_number], res[li[brace_number]]
    return content[li[brace_number]:res[li[brace_number]] + 1]


def get_content_between_brace_v2(content: str, brace_number: int):
    # todo 有严重的bug。 {}{}123{}111，无法正常获取，
    # todo 如果brace_number=2，永远无法达到，栈的深度为嵌套括号的数，而非从左往右的左括号数量

    # todo 栈，解决嵌套问题，很棒！！ 比如调用栈、括号嵌套
    stack = Stack()
    res_str = []
    is_reach = 0
    try:
        for i in range(0, len(content)):
            if content[i] == '{':
                stack.push({'{': i})
                if len(stack.stack) == brace_number:
                    is_reach = 1
            elif content[i] == '}':
                if len(stack.stack) == brace_number:
                    is_reach = 0
                stack.pop()
            if is_reach:
                res_str.append(content[i])
    except LookupError:
        print("错误 缺少 { 或者 } , index: ", i)
    res_str.append('}')
    return res_str


def work_fun():
    with open('data.txt', encoding='utf-8') as f:
        text = f.read()
        for i in range(1, 200):
            body = get_content_between_brace(text, i, ['{', '}'])

            all_field_in_rs = []
            for yin in re.findall(r'".*"', body):
                all_field_in_rs.append(yin.replace('"', ''))

            # customColNameMatcher = re.search(r'(?<=statistics.put)\(".*;', body, re.M | re.I)
            put_matcher = re.search(r'(?<=statistics.put).*', body)
            put_source = put_matcher.group()
            if 'scale' in put_source:
                calc_rule = get_content_between_brace(put_source, 2, ['(', ')'])
            else:
                calc_rule = re.search(r',.+', put_source).group()
            # print('put_source: ', put_source)
            # put_source = put_source.replace('(', '')
            # put_source = put_source.replace(')', '')
            put_split = put_source.split(',')
            diy_col = put_split[0]

            result_intercept = re.search(r'scale.*\(', body)
            if result_intercept is not None:
                scale = result_intercept.group()
                pass
            else:
                scale = 'none-scale'
            # print('---------------------')
            diy_col = re.sub(r'["\(\);,]', '', diy_col)
            calc_rule = re.sub(r'["\(\);,]', '', calc_rule)
            scale = re.sub(r'["\(\);,]', '', scale)

            # 匹配单词
            # calc_rule
            calc_fields = ''
            word_reg = re.findall(r'\b[\d\w]+\b', calc_rule)
            for word in word_reg:
                # print('match word :', word)
                if word not in all_field_in_rs and word not in 'cost':
                    calc_fields += word + '(not in !),'
                else:
                    calc_fields += word + ','

            print(diy_col, ' ', calc_rule.replace(' ', ''), ' ', scale, ' ', calc_fields[0:-1])
            # all field with ""

            # for p in all_field_in_rs:
            #     print(p, end=' ')
            # print(all_field_in_rs)
            # print()
            # print('---------------------')

        pass
    pass


if __name__ == '__main__':
    work_fun()
    pass
    # print("soup", 123, sep=':')
    # str="123"
    # print(str[0:3])
    # print(get_content_between_brace("{{}}", 2))
    # {111{AAa}222}333{BBB}{CCC}DDD{FFF}
    # print(get_content_between_brace("""
    # 1{1}23{2}1{3}23{4}12{5}31{6}23{7}
    # """, 4))
