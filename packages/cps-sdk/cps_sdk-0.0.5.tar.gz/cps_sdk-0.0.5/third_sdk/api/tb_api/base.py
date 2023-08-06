from third_sdk import top
import time
import hashlib
import requests
from typing import Union


SYSTEM_GENERATE_VERSION = "taobao-sdk-python-fengjinqi"

P_APPKEY = "app_key"
P_API = "method"
P_SESSION = "session"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"

P_CODE = 'code'
P_SUB_CODE = 'sub_code'
P_MSG = 'msg'
P_SUB_MSG = 'sub_msg'

N_REST = '/router/rest'


class TbClient:

    def __init__(self, host='http://gw.api.taobao.com/router/rest', port=80, appkey='', secret='', timeout=30):
        self.__host = host
        self.__port = port
        self.__appkey = appkey
        self.__secret = secret
        self.__timeout = timeout

    def taobao_tbk_dg_material_optional(self, api: Union[top.api.TbkDgMaterialOptionalRequest, str] = None, access_token=None,
                                        **kwargs):
        """
        物料搜索
        """
        if api is None:
            api = top.api.TbkDgMaterialOptionalRequest(self.__host, self.__port)
        return self.api_invoke(api, access_token, **kwargs)

    def taobao_tbk_dg_item_info_get(self, api: Union[top.api.TbkItemInfoGetRequest, str] = None, access_token=None, **kwargs):
        """
        商品详情查询(简版)
        """
        if api is None:
            api = top.api.TbkItemInfoGetRequest(self.__host, self.__port)
        return self.api_invoke(api, access_token, **kwargs)

    def api_invoke(self, api: Union[top.api.base.RestApi, str], access_token=None, method='POST', **kwargs):
        """
        api 调用通用方法
        """
        assert api is not None
        if type(api) == str:
            return _api_invoke(self.__host, method, self.__appkey, self.__secret, api, access_token, self.__timeout, **kwargs)
        api.set_app_info(top.appinfo(self.__appkey, self.__secret))
        for k, v in kwargs.items():
            setattr(api, k, v)
        return api.getResponse(authrize=access_token, timeout=self.__timeout)


def _get_request_header():
    return {
             'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
             "Cache-Control": "no-cache",
             "Connection": "Keep-Alive",
    }


def _get_application_parameters(**kwargs):
    p = {}
    for key, value in kwargs.items():
        if key and value:
            if key.startswith("_"):
                p[key[1:]] = value
            else:
                p[key] = value
    return p


def _sign(sec, parameters):
    # ===========================================================================
    # '''签名方法
    # @param sec: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    # ===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        keys = list(parameters.keys())
        keys.sort()

        parameters = "%s%s%s" % (sec,
                                 str().join('%s%s' % (key, parameters[key]) for key in keys),
                                 sec)
    return hashlib.md5(parameters.encode('utf8')).hexdigest().upper()


def _api_invoke(domain, http_method, appkey, secret, apiname, access_token, timeout, **kwargs):
    sys_parameters = {
        P_FORMAT: 'json',
        P_APPKEY: appkey,
        P_SIGN_METHOD: "md5",
        P_VERSION: '2.0',
        P_TIMESTAMP: str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),
        P_PARTNER_ID: SYSTEM_GENERATE_VERSION,
        P_API: apiname,
    }
    if access_token is not None:
        sys_parameters[P_SESSION] = access_token
    application_parameter = _get_application_parameters(**kwargs)
    sign_parameter = sys_parameters.copy()
    sign_parameter.update(application_parameter)
    sys_parameters[P_SIGN] = _sign(secret, sign_parameter)
    sys_parameters.update(sign_parameter)

    header = _get_request_header()
    return requests.request(http_method, domain, data=sys_parameters, headers=header, timeout=timeout)
