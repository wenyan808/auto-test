#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:10 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceAPI import user01
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil

@allure.epic('反向永续')
@allure.feature('')
@allure.story('')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_detail_001:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_detail_001',
           'TestSwapNoti_detail_002',
           'TestSwapNoti_detail_003',
          ]
    params = [{'case_name':'获取聚合行情','contract_code':contract_code},
              {'case_name':'合约不存在','contract_code':'BTC-BTC'},
              {'case_name':'合约代码错误','contract_code':'BTC-USDT'}]


    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('ws:执行sub请求'):
            subs = {
                "sub": "market.{}.detail".format(params['contract_code']),
                "id": "id6"
            }
            result = retryUtil(ws_user01.swap_sub, subs, ["tick", "ask"])
            pass
        with allure.step('校验返回结果'):
            checked_col = ['amount', 'ask', 'bid', 'close', 'count', 'high', 'id', 'low', 'open', 'vol']
            for col in checked_col:
                assert result['tick'][col] is not None, str(col) + '为None,不符合预期'
