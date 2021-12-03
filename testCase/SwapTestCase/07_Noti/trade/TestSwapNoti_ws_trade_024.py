#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 4:03 下午
# @Author  : HuiQing Yu
import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][5])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_ws_trade_024:
    ids = ['TestSwapNoti_ws_trade_024']
    params = [{'case_name': '合约代码为空'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub请求'):
            subs = {
                "req": "market..trade.detail",
                "size": 5,
                "id": "id1",
            }
            trade_info = ws_user01.swap_sub(subs=subs)
            pass
        with allure.step('验证:返回结果提示 invalid topic'):
            assert 'err-msg' in trade_info,'预期报错,实际未报错校验不通过'
            assert 'invalid topic' in trade_info['err-msg'], f'未传合代码预期应该提示invalid topic，实际返回：{trade_info}'
            pass
