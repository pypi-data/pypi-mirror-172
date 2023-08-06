from third_sdk.jd.api.rest.UnionOpenGoodsQueryRequest import UnionOpenGoodsQueryRequest
from third_sdk.jd.api.base import RestApi
from third_sdk.jd import appinfo
import time
import json
import hashlib
import requests
from urllib import parse
from typing import Union


SYSTEM_GENERATE_VERSION = "taobao-sdk-python-fengjinqi"

P_APPKEY = "app_key"
P_API = "method"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_JSON_PARAM_KEY = "360buy_param_json"

P_CODE = 'code'
P_SUB_CODE = 'sub_code'
P_MSG = 'msg'
P_SUB_MSG = 'sub_msg'

N_REST = '/routerjson'


class JdClient:

    def __init__(self, host='https://api.jd.com/routerjson', port=80, appkey='', secret='', timeout=30):
        self.__host = host
        self.__port = port
        self.__appkey = appkey
        self.__secret = secret
        self.__timeout = timeout

    def jd_union_open_goods_query(self, api: Union[UnionOpenGoodsQueryRequest, str] = None, access_token=None,
                                  **kwargs):
        if api is None:
            api = UnionOpenGoodsQueryRequest(self.__host, self.__port)
        return self.api_invoke(api, access_token, **kwargs)

    def api_invoke(self, api: Union[RestApi, str], access_token=None, version="1.0", method='POST', **kwargs):
        assert api is not None

        if type(api) == str:
            return _api_invoke(self.__host, method, self.__appkey, self.__secret, api, version, access_token, self.__timeout, **kwargs)

        api.set_app_info(appinfo(self.__appkey, self.__secret))
        for k, v in kwargs.items():
            setattr(api, k, v)
        return api.getResponse(access_token=access_token, timeout=self.__timeout)


def _get_application_parameters(**kwargs):
    application_parameter = {}
    for key, value in kwargs.items():
        if key and value:
            if key.startswith("_"):
                application_parameter[key[1:]] = value
            else:
                application_parameter[key] = value
    return application_parameter


def _sign(secret, parameters):
    str_parameters = ""
    if hasattr(parameters, "items"):
        keys = sorted(parameters.keys())
        str_parameters = "%s%s%s" % (secret,
                                     str().join('%s%s' % (key, parameters[key]) for key in keys),
                                     secret)
    a_sign = hashlib.md5(str_parameters.encode("utf-8")).hexdigest().upper()
    return a_sign


def _api_invoke(domain, http_method, appkey, secret, apiname, version, access_token, timeout, **kwargs):
    sys_parameters = {
        P_APPKEY: appkey,
        P_VERSION: version,
        P_API: apiname,
        P_TIMESTAMP: time.strftime("%Y-%m-%d %H:%M:%S.000%z", time.localtime()),
    }
    if access_token is not None:
        sys_parameters[P_ACCESS_TOKEN] = access_token
    if not domain.startswith('http'):
        url = 'http://' + domain
    else:
        url = domain
    if not url.endswith(N_REST) and not url.endswith(N_REST + '/'):
        url = url[:-1] if url.endswith('/') else url
        url = url + N_REST

    application_parameter = _get_application_parameters(**kwargs)
    sys_parameters[P_JSON_PARAM_KEY] = json.dumps(application_parameter, ensure_ascii=False,
                                                  default=lambda value: value.__dict__)
    sys_parameters[P_SIGN] = _sign(secret, sys_parameters)
    if http_method == 'POST':
        return requests.post(url, data=sys_parameters, timeout=timeout)
    else:
        url = url + "?" + parse.urlencode(sys_parameters)
        return requests.get(url, timeout=timeout)
