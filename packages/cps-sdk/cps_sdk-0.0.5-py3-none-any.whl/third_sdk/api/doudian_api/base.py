import hashlib
import json
import time
import hmac
from hashlib import sha256
import requests
from urllib.parse import urlencode


def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def hmac_sha256(k, s):
    m = hmac.new(k, s, digestmod=sha256)
    return m.hexdigest()


def _get_sort_dict(dict_val):
    new_val = {}
    keys = sorted(list(dict_val.keys()))
    for k in keys:
        new_val[k] = dict_val[k]
    return new_val


class DouDianClient:

    def __init__(self, host='openapi-fxg.jinritemai.com', appkey='', secret='', get_access_token_func=None):
        self.__host = host if host.startswith("http") else 'https://' + host
        self.__appkey = appkey
        self.__secret = secret
        self.__get_access_token_func = get_access_token_func

    def buyin_kolMaterialsProductsSearch(self, **kwargs):
        return self.api_invoke('buyin.kolMaterialsProductsSearch', version='2', **kwargs)

    def api_invoke(self, api_name, version="1", **kwargs):
        now = int(time.time())
        api_path = "/" + api_name.replace('.', "/")
        params = _get_sort_dict(kwargs)
        sign = self._get_sign(api_name, version, now, params)
        query = {
            'method': api_name,
            'app_key': self.__appkey,
            'access_token': self.__get_access_token_func(),
            'timestamp': now,
            'v': version,
            'sign_method': 'hmac-sha256',
            'sign': sign
        }
        query = _get_sort_dict(query)
        url = self.__host + api_path + '?' + urlencode(query)
        return requests.post(url, json=params)

    def _get_sign(self, api_name, version, timestamp, params):
        s = f'{self.__secret}app_key{self.__appkey}method{api_name}param_json{json.dumps(params, ensure_ascii=False).replace(" ", "")}timestamp{timestamp}v{version}{self.__secret}'
        return hmac_sha256(self.__secret.encode('utf-8'), s.encode('utf-8'))
