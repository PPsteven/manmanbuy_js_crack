import base64
import time
from urllib.parse import quote
import hashlib
import collections

def get_basic_auth_str(username, password):
  temp_str = username + ':' + password
  bytesString = temp_str.encode(encoding="utf-8")  # 转成bytes string
  encodestr = base64.b64encode(bytesString)  # base64 编码
  return 'Basic ' + encodestr.decode() 

def decode_basic_auth_str(auth_str):
    bytesString = auth_str.encode("utf-8")
    decode_str = base64.b64decode(bytesString)
    return decode_str.decode("utf-8")


def create_form_data(link, secret):
    """
    生成 form_data, 通过模拟前端JS逻辑
    :param link: 网站的网址
    :param secret:
    :return: form_data

    >>> create_form_data('http://item.jd.hk/10429555538.html', 'c5c3f201a8e8fc634d37a766a0299218')
    """

    form_data = {
        'method': 'getHistoryTrend',
        'key': link,
        't': str(int(time.time() * 100000))[:13] # 13 位时间戳
    }

    form_data = collections.OrderedDict( # 按照 key 排序
        sorted(
            form_data.items(),
            key=lambda x: x[0])
    )

    token = secret # secret 不变
    for k, v in form_data.items():
        token += quote(k, safe='') + quote(v, safe='') # Python 默认不转义斜杠(safe) //, 前端 JavaScript 转义
    token += secret
    token = token.upper() # 转成大写
    m = hashlib.md5()
    m.update(token.encode('utf-8')) # 生成 md5 码
    token = m.hexdigest().upper() 
    form_data['token'] = token  # 添加 token 
    return form_data

if __name__ == '__main__':
    auth_str = get_basic_auth_str('Tom', 'test') # Basic VG9tOnRlc3Q=
    decode_str = decode_basic_auth_str('VG9tOnRlc3Q=') # Tom:test
    data = create_form_data(
    'https://item.jd.com/10429555538.html', 'c5c3f201a8e8fc634d37a766a0299218')

    