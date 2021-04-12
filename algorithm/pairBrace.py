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


def get_content_between_brace(content: str, brace_number: int):
    brace_number -= 1
    stack = Stack()
    res = {}
    try:
        for i in range(0, len(content)):
            if content[i] == '{':
                stack.push({'{': i})
            elif content[i] == '}':
                frame = stack.pop()
                res[frame['{']] = i
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


if __name__ == '__main__':
    # print("soup", 123, sep=':')
    # str="123"
    # print(str[0:3])
    print(get_content_between_brace("{{}}", 2))
    # {111{AAa}222}333{BBB}{CCC}DDD{FFF}
    print(get_content_between_brace("""
    {111{AAa}222}333{BBB}{CCC}DDD{FFF}
    """, 4))
