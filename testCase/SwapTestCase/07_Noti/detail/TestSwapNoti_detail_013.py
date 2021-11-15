#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:26 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil

@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('深度图&Overview')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_detail_013:
    ids = ['TestSwapNoti_detail_013']
    params = [{'case_name':'WS订阅 OverView'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub订阅'):
            subs = {
                "op": "sub",
                "sub": "market.overview",
                "zip": 1
            }
            result = retryUtil(ws_user01.swap_sub, subs, 'data')
            pass
        with allure.step('校验返回结果'):
            checked_col = ['amount', 'symbol', 'close', 'count', 'high', 'low', 'open', 'vol']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None, str(col) + '为None,不符合预期'
