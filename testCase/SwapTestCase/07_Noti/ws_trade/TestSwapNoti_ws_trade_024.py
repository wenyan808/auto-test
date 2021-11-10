#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceWS import user01
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('成交')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_ws_trade_024:
    ids = ['TestSwapNoti_ws_trade_024']
    params = [{'case_name':'合约代码为空'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('' + params['case_name'])
        with allure.step('执行sub请求'):
            subs = {
                "req": "market..trade.detail",
                "size": 5,
                "id": "id1",
            }
            trade_info = user01.swap_sub(subs=subs)
            assert 'ok' in trade_info['status']
            pass
