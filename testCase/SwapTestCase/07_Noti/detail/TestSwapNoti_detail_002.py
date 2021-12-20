#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:10 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_detail_002:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
           'TestSwapNoti_detail_002',
           'TestSwapNoti_detail_003',
           'TestSwapNoti_detail_004',
           'TestSwapNoti_detail_005',
          ]
    params = [
              {'case_name':'合约不存在','contract_code':'BTC-BTC'},
              {'case_name':'合约代码错误','contract_code':'BTC-USDT'},
              {'case_name':'不传合约代码','contract_code':None},
              {'case_name':'合约代码错为空','contract_code':''},
            ]


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
        with allure.step('ws:执行sub请求'):
            subs = {
                "sub": "market.{}.detail".format(params['contract_code']),
                "id": "id6"
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('校验返回结果'):
            assert 'invalid topic' in result['err-msg'],'无效的topic'
            pass

if __name__ == '__main__':
    pytest.main()