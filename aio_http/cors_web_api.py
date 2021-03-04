# examples/server_simple.py
import json
from threading import Lock, Thread
import six
from google.cloud import translate_v2 as translate
import html
import time
import asyncio
from aiohttp import web
import aiohttp_cors

secret = 'moersi2021'
mutex = Lock()
char_count = 0
max_count = 10000


def translate_text(text, target, source=None):
    global char_count
    try:
        mutex.acquire()
        char_count += len(text)
        if char_count > max_count:
            return '今日翻译量字数已到达上限,{}'.format(max_count)
    finally:
        mutex.release()
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    try:
        translate_client = translate.Client()
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        # source_language
        if source is None:
            result = translate_client.translate(text, target_language=target)
        else:
            result = translate_client.translate(text, source_language=source, target_language=target)

        # print(u"Text: {}".format(result["input"]))
        # print(u"Translation: {}".format(result["translatedText"]))
        # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
        return html.unescape(result["translatedText"])
    except Exception as e:
        print(e)


@asyncio.coroutine
async def handle(request):
    req_body = await request.text()
    param_obj = json.loads(req_body)
    global secret
    post_secret = param_obj['secret']
    res = {}
    if post_secret != secret:
        res['错误'] = '密码错误'
    else:
        source_language = None
        try:
            source_language = param_obj['sourceLanguage']
            if source_language == '':
                source_language = None
        except KeyError as error:
            print('not send param:', error)
        text = param_obj['text']
        print(param_obj['targetLanguages'])
        tar_lan_list = param_obj['targetLanguages']
        for tar_lan in tar_lan_list:
            print(tar_lan)
            res[tar_lan] = translate_text(text, tar_lan, source_language)
    return web.json_response(res)


def flush_count():
    global char_count
    while 1:
        time.sleep(60 * 60 * 24)
        # time.sleep(5)
        mutex.acquire()
        print(time.asctime(), '今日翻译字符量: {}'.format(char_count))
        char_count = 0
        mutex.release()
    pass


if __name__ == '__main__':
    t1 = Thread(target=flush_count)
    t1.start()
    app = web.Application()

    cors = aiohttp_cors.setup(app)
    resource = cors.add(app.router.add_resource("/translate"))
    route = cors.add(
        resource.add_route("POST", handle), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })
    web.run_app(app, port=8111)
