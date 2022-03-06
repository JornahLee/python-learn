import requests  # pip3 install requests
from bs4 import BeautifulSoup  # pip3 install beautifulsoup4,依赖pip3 install lxml
import re
import time
import os
import pyperclip

headers = {
    # 存储任意的请求头信息
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def download_with_link(img_url: str):
    folder_name = 'imgs'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    print("download img", img_url)
    file_suffix = get_file_suffix(img_url)
    try:
        img_resp = requests.get(img_url, headers=headers)
        with open("imgs/" + str(time.time()) + file_suffix, 'wb') as f:
            f.write(img_resp.content)
    except Exception as e:
        print("error", e)


def get_file_suffix(url: str) -> str:
    return re.search(r"\.\w{3,5}$", url).group()


class Field:
    pass


def extract_field():
    global api_url, api_title
    content = f.read()
    soup = BeautifulSoup(content, "lxml")
    for a_url in soup.select('.tui-editor-contents p'):
        if a_url.text.startswith('https://'):
            api_url = a_url.text.replace('https://marketing-api.vivo.com.cn/openapi/', '')

    for title in soup.select('.doc-title'):
        api_title = title.text

    li = soup.select("tr")
    res = []
    for l in li:
        list = []
        for td in l.select('td'):
            list.append(td.text.rstrip())
        if list is not None and len(list) > 0:
            res.append(list)
    return res


def generate_dto(field_list: list, print_resp: bool):
    is_response = False
    request_field_str = api_title + ' '
    response_field_str = api_title + ' '
    for field in field_list:
        field_name = field[0]
        field_type = field[1]
        field_note = field[2]
        if field_name.__contains__('必填'):
            field_name = field_name.replace('必填', '')
            field_note = '必填!!!\n' + field_note
        # 先屏蔽response

        if 'code' == field_name:
            is_response = True
        format = "/**  {} */\n  {}  {}  {} ; \n"
        field_and_note = format.format(field_note, accessor, field_type, field_name)
        if is_response:
            response_field_str += field_and_note
        else:
            request_field_str += field_and_note
    if print_resp:
        print(response_field_str)
        pyperclip.copy(response_field_str)
    else:
        print(request_field_str)
        pyperclip.copy(request_field_str)


def generate_params(field_list: list):
    note_list = []
    map_put_list = []
    fun_param_list = []
    line_max_field = 3
    line_field_count = 0
    for field in field_list:
        field_name = field[0]
        field_type = field[1]
        field_note = field[2]
        if field_name.__contains__('必填'):
            field_name = field_name.replace('必填', '')
            field_note = '必填!!!   ' + field_note
        # 先屏蔽response
        if 'code' == field_name:
            break
        note_list.append('* @param ' + field_name + ' ' + field_note)
        map_put_list.append('requestBody.put("' + field_name + '",' + field_name + ');')
        fun_param_list.append(field_type + ' ' + field_name + ',')
        # print(field_type, field_name, ',')
        # line_field_count += 1
        # if line_field_count >= line_max_field:
        #     print(field_type, field_name, ',')
        #     line_field_count = 0
        # else:
        #     print(field_type, field_name, ',', end="")
    all_note = '* @param advertiserId\n'
    for note in note_list:
        all_note += note + '\n'
    all_field_str = ''
    for f in fun_param_list:
        all_field_str += f
    all_put_str = ''
    for put in map_put_list:
        all_put_str += put

    fun_ouput = '''
    /**
    * {}
    {}
    */
    public VivoResponse<Object> xxxx(String advertiserId,{}){{
    String url = "{}";
    URI uri = vivoApiKit.getUri(url, advertiserId);
    HashMap<String, Object> requestBody = new HashMap<>();
    {}
    HttpEntity<?> entity = new HttpEntity<>(requestBody);
    ResponseEntity<String> res = restTemplate.exchange(uri, HttpMethod.POST, entity, String.class);
    return vivoApiKit.gson.fromJson(res.getBody(), new TypeToken<VivoResponse<Object>>() {{
        }}.getType());}}
    '''.format(api_title, all_note, all_field_str[0:-1], api_url, all_put_str)
    print(fun_ouput)
    pyperclip.copy(fun_ouput)


if __name__ == '__main__':
    accessor = 'private'
    global api_url, api_title
    with open('xxx.html', encoding='utf-8') as f:
        extract_res = extract_field()
        generate_dto(extract_res, print_resp=False)
        print('----------------------------------------------------')
        print('----------------------------------------------------')
        # generate_params(extract_res)

    # for i in li:
    #     link = i.attrs["src"]
    #     if link.startswith("https"):
    #         real_link = link.split("?")[0]
    #         download_with_link(real_link)
