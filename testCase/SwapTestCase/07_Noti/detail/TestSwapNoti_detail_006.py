#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:31 下午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('深度图&Overview')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_detail_006:
    ids = ['TestSwapNoti_detail_006']
    params = [{'case_name':'深度图 percent=10','percent':'percent10'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('更新深度'):
            cls.current_price = currentPrice()
            for i in range(10):
                api_user01.swap_order(contract_code=cls.contract_code,
                                      price=round(cls.current_price * (1 - i * 0.01), 2),
                                      direction='buy')
                api_user01.swap_order(contract_code=cls.contract_code,
                                      price=round(cls.current_price * (1 + i * 0.01), 2),
                                      direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤单'):
            api_user01.swap_cancelall(cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code,params['percent']),
                "id": "test_depth_id"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    if result['tick']['asks'] and result['tick']['bids']:
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '未返回预期结果'
            pass
            pass
        with allure.step('验证：返回的bids和asks不为空'):
            assert result['tick']['bids']
            assert result['tick']['asks']
            pass
