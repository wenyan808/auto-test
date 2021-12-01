#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu
from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_138:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_ws_kline_138',
           'TestSwapNoti_ws_kline_139',
           'TestSwapNoti_ws_kline_140',
           'TestSwapNoti_ws_kline_141',
           'TestSwapNoti_ws_kline_142',
           'TestSwapNoti_ws_kline_143']
    params = [
        {
            "case_name": "period不存在 合约不存在",
            "period": "1year",
            "contract_code":"BTC-BTC"
        },{
            "case_name": "period不存在 合约正确",
            "period": "1year",
            "contract_code": contract_code
        },{
            "case_name": "period为空",
            "period": "",
            "contract_code":contract_code
        },{
            "case_name": "不传period",
            "period": None,
            "contract_code":contract_code
        },{
            "case_name": "合约代码为空",
            "period": "1min",
            "contract_code":""
        },{
            "case_name": "不传合约代码",
            "period": "1min",
            "contract_code":None
        }
    ]

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：发送req请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "req": "market.{}.kline.{}".format(params['contract_code'],params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'invalid topic' or 'invalided kline type' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
