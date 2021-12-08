#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : HuiQing Yu

import requests
from config.conf import MGT_INFO

class SwapServiceMGT:

    def __init__(self):
        mgt_info = eval(MGT_INFO)
        self.__url = mgt_info['host']
        self.TIMEOUT = 15
        self.token =mgt_info['user_info']['token']

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

SwapServiceMGT = SwapServiceMGT()
