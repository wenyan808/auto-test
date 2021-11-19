#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:10 下午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from common.SwapServiceAPI import user01 as api_user01
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('聚合行情')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_detail_001:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_detail_001']
    params = [{'case_name':'获取聚合行情','contract_code':contract_code}]


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

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('ws:执行sub请求'):
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice, 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice, 2),
                                  direction='sell')
            time.sleep(2)
            subs = {
                "sub": "market.{}.detail".format(params['contract_code']),
                "id": "id6"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    if result['tick']['ask'] and result['tick']['bid'] :
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag,'未返回预期结果'
            pass
        with allure.step('验证：返回结果各字段不为空'):
            checked_col = ['amount', 'ask', 'bid', 'close', 'count', 'high', 'id', 'low', 'open', 'vol']
            for col in checked_col:
                assert result['tick'][col], str(col) + '为None,不符合预期'
