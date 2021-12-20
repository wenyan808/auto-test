#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : HuiQing Yu
import base64
import requests
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from config.conf import MGT_INFO, DEFAULT_SYMBOL


class SwapServiceMGT(object):

    def __init__(self):
        mgt_info = eval(MGT_INFO)
        self.__url = mgt_info['host']
        self.TIMEOUT = 15
        # 登入获取token
        keyUrl = 'http://test5-contract-hw.dm.huobiapps.com/swap-manager-web/publicKey'
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
        rsakey = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt('HB@230032mgt'.encode()))
        password = cipher_text.decode()
        request_path = 'http://test5-contract-hw.dm.huobiapps.com/swap-manager-web/logon'
        data = {"userName": "yuhuiqing", "password": password,
                "verification_code": "", "extends": {"smsCode":"","gaCode":""}}
        res = requests.post(url=request_path, data=data,headers=headers)
        res.encoding = res.apparent_encoding
        print(res.headers['token'])
        self.token = res.headers['token']

    # =============================================================#
    #                                                              #
    #                         MGT  Interface                       #
    #                                                              #
    # =============================================================#
    # 各种请求,获取数据方式
    def http_request(self, url, data, method, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept-language": "zh-CN",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        try:
            if 'GET' in method:
                response = requests.get(url, data, headers=headers, timeout=self.TIMEOUT)
            elif 'POST' in method:
                response = requests.post(url, data, headers=headers, timeout=self.TIMEOUT)

            print('\033[1;32;49m%s\033[0m' % f'\n请求地址= {url}\n请求参数 = {data}')
            print('\033[1;32;49m%s\033[0m' % f'返回结果 = {str(response.json())}')
            if response.status_code == 200:
                return response.json()
            else:
                return response.text
        except Exception as e:
            print("httpPost failed, detail is:%s" % e)
            return {"status": "fail", "msg": "%s" % e}

    # 获取平台流程表信息
    def findPaltformFlow(self, params=None):
        headers = {
            'token': self.token,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        request_path = '/swap-manager-web/service/accountCapitalDailyService/findPaltformFlow'
        data = f'params={str(params)}'
        return self.http_request(self.__url + request_path, method='POST', data=data, add_to_headers=headers)
    # MGT 转账申请
    def saveTransfer(self, symbol=None,userAmountList=None, transType=None, quantity=None, transferOutAccount=None,
                     transferInAccount=None):
        headers = {
            'token': self.token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        params = [
            symbol,
            {
                "userAmountList": userAmountList,
                "productId": symbol,
                "type": transType,
                "quantity": quantity,
                "transferOutAccount": transferOutAccount,
                "transferInAccount": transferInAccount,
                "remark": "Automation Test"
            }
        ]
        request_path = '/swap-manager-web/service/accountActionService/saveTransfer'
        data = str(params).replace('None','null')
        data = f'params={data}'
        return self.http_request(self.__url + request_path, method='POST', data=data, add_to_headers=headers)

    # MGT 转账审核
    def checkTransferRecord(self,transferId=None):
        headers = {
            'token': self.token,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        params = [ transferId,1,'']
        request_path = '/swap-manager-web/service/transferRecordService/checkTransferRecord'
        data = f'params={str(params)}'
        return self.http_request(self.__url + request_path, method='POST', data=data, add_to_headers=headers)

    # MGT 平账
    def flat(self,symbol=None,flatAccount=None,uid=None,money=None):
        headers = {
            'token': self.token,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        if symbol is None:
            symbol = DEFAULT_SYMBOL

        params = [
            symbol,
            {
                "productId": symbol,
                "flatAccount": flatAccount,
                "uid": uid,
                "money": money,
                "remark": "Automation Test"
            }
        ]
        request_path = '/swap-manager-web/service/accountActionService/save'
        data = str(params).replace('None', 'null')
        data = f'params={str(data)}'
        return self.http_request(self.__url + request_path, method='POST', data=data, add_to_headers=headers)

SwapServiceMGT = SwapServiceMGT()
