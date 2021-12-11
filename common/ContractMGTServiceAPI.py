#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
from pprint import pprint
from config.conf import USERINFO
from common.util import api_http_get, api_http_from_post, rsa_encrpt
from config import conf
from config.conf import URL
import requests


class ContractMGTServiceAPI:

    def __init__(self, url):
        keyUrl = url + '/contract-manager-web/publicKey'
        keyRes = requests.get(keyUrl)
        tempToken = keyRes.headers['token']
        headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-language": "zh-CN",
            "token": tempToken,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        }
        keyRes = requests.get(url=keyUrl, headers=headers)
        key = keyRes.text
        public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
        password = rsa_encrpt('Alex@1982', public_key)
        tokeUrl = url+'/contract-manager-web/logon'
        params = {"userName": "alexli", "password": password,
                  "verification_code": "", "extends": {"smsCode": "", "gaCode": ""}}

        res = requests.post(url=tokeUrl, params=params, headers=headers)
        res.encoding = res.apparent_encoding
        self.__token = res.headers['token']
        self.__url = url

# 转账
    def accountActionService_saveTransfer(self, params):
        url = self.__url + '/contract-manager-web/service/accountActionService/saveTransfer'
        return api_http_from_post(url, params, {"token": self.__token})

    def checkTransferRecord(self, params):
        url = self.__url + '/contract-manager-web/service/transferRecordService/checkTransferRecord'
        return api_http_from_post(url, params, {"token": self.__token})
# 平账

    def accountActionService_save(self, params):
        url = self.__url + '/contract-manager-web/service/accountActionService/save'
        return api_http_from_post(url, params, {"token": self.__token})


t = ContractMGTServiceAPI(URL)
