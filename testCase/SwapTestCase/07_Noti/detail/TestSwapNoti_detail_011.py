#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:31 下午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')
@allure.feature('行情')
@allure.story('深度图&Overview')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_detail_011:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_detail_007',
           'TestSwapNoti_detail_008',
           'TestSwapNoti_detail_009',
           'TestSwapNoti_detail_010',
           'TestSwapNoti_detail_011',
           'TestSwapNoti_detail_012',
           ]
    params = [
              {'case_name': '深度图 合约不存在', 'percent': 'percent10','contract_code':'BTC-BTC'},
              {'case_name': '深度图 合约代码错误', 'percent': 'percent10','contract_code':'BTC-USDT'},
              {'case_name': '深度图 不传合约代码', 'percent': 'percent10','contract_code':None},
              {'case_name': '深度图 合约代码传空', 'percent': 'percent10','contract_code':''},
              {'case_name': '深度图 percent!=10', 'percent': 'percent15','contract_code':contract_code},
              {'case_name': '深度图 percent为空', 'percent': '','contract_code':contract_code},
              ]



    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(params['contract_code'],params['percent']),
                "id": "test_depth_id"
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示为 invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass

if __name__ == '__main__':
    pytest.main()