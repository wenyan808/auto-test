#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:10 下午
# @Author  : HuiQing Yu

import allure
import pytest
import time

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01 as api_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
@allure.tag('Script owner : 韩东林', 'Case owner : 柳攀峰')
@pytest.mark.stable
class TestSwapNoti_014:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_014']
    params = [{'case_name':'获取批量聚合行情','contract_code':contract_code}]


    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.currentPrice = currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*0.5, 2), direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.5, 2), direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤盘'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作:执行api-restful请求'):
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice, 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice, 2),
                                  direction='sell')
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                result = api_user01.swap_batch_merged(contract_code=self.contract_code)
                if 'ticks' in result:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag,'未返回预期结果'
            pass
        with allure.step('验证：返回结果各字段不为空'):
            checked_col = ['id', 'ts', 'bid', 'ask', 'contract_code', 'open','close','high', 'low', 'amount', 'count', 'vol']
            for col in checked_col:
                assert result['ticks'][0][col], str(col) + '为None,不符合预期'
