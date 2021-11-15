#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:31 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil

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
            cls.current_price = ATP.get_current_price()
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
        allure.dynamic.title('' + params['case_name'])
        with allure.step('执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code,params['percent']),
                "id": "test_depth_id"
            }
            result = retryUtil(ws_user01.swap_sub, subs, "tick")
            pass
        with allure.step('校验返回结果'):
            assert result['tick']['bids'] is not None
            allure.step("字段bids不为空校验通过")
            assert result['tick']['asks'] is not None
            allure.step("字段bids不为空校验通过")
            pass
