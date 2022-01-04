#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient
import allure
import pytest

from common.SwapServiceWS import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_ws_trade_012:
    ids = ['TestSwapNoti_ws_trade_012']
    params = [{'case_name':'合约交割中'}]


    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        contract_info = SwapTool.getContractStatus(instrument_status=8)#这里拿了一个交割完成，待盘口合约状态还是交割中
        if contract_info['isSkip']:
            assert False, '未找到交割中合约'
        with allure.step('执行sub请求'):
            subs = {
                "sub": f"market.{contract_info['data']['instrument_id']}.trade.detail",
                "id": "id1",
            }
            trade_info = user01.swap_sub(subs=subs,keyword='status')
            pass
        with allure.step('验证：正常返回无报错'):
            assert 'ok' in trade_info['status']
