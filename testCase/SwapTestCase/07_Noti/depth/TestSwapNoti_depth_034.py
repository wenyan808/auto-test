#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : 张广南

import time
import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from tool.SwapTools import SwapTool
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_034:
    contract_code = DEFAULT_CONTRACT_CODE
    symbol = DEFAULT_SYMBOL
    ids = [
        'TestSwapNoti_depth_034',
        'TestSwapNoti_depth_036',
    ]
    params = [
        {'case_name': 'WS订阅深度 20档 卖盘>20档','exceptLength':20,'type':'step6'},
        {'case_name': 'WS订阅深度 150档 卖盘>150档', 'exceptLength': 150,'type':'step0'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            pass
        with allure.step('挂单更新深度'):
            for i in range (152):
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * (1+0.01*i), 2), direction='sell')
        with allure.step('查询redis深度更新'):
            for i in range (5):
                if SwapTool.opponentExist(symbol=cls.symbol, asks='asks'):
                    break
                else:
                    print('深度未更新,第{}次重试……'.format(i+1))
                    time.sleep(1)



    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境，撤销挂单'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code,params['type']),
                "id": "id5"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    if result['tick']['asks']:
                        flag = True
                        break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag, '未返回预期结果'
            pass
        with allure.step('验证：返回结果卖盘长度为{}'.format(params['exceptLength'])):
            flag = False
            for i in range(3):
                if len(result['tick']['asks']) == params['exceptLength']:
                    flag = True
                else:
                    print(f'深度未完全更新，第{i+1}次重试……')
                    time.sleep(1)
            assert flag,'多次重试，未还返回预期深度'
if __name__ == '__main__':
    pytest.main()
