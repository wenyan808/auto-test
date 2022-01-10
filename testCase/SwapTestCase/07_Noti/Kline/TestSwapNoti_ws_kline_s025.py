#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.case_content import epic, features
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_s025:

    ids = ['TestSwapNoti_ws_kline_025',
           'TestSwapNoti_ws_kline_031',
           'TestSwapNoti_ws_kline_037',
           'TestSwapNoti_ws_kline_043',
           'TestSwapNoti_ws_kline_049',
           'TestSwapNoti_ws_kline_055',
           'TestSwapNoti_ws_kline_061',
           'TestSwapNoti_ws_kline_067',
           'TestSwapNoti_ws_kline_073']
    params = [
        {
            "case_name": "合约结算中-1min",
            "period": "1min",
            "title": ids[0],
        },
        {
            "case_name": "合约结算中-5min",
            "period": "5min",
            "title": ids[1],
        },
        {
            "case_name": "合约结算中-15min",
            "period": "15min",
            "title": ids[2],
        },
        {
            "case_name": "合约结算中-30min",
            "period": "30min",
            "title": ids[3],
        },
        {
            "case_name": "合约结算中-60min",
            "period": "60min",
            "title": ids[4],
        },
        {
            "case_name": "合约结算中-4hour",
            "period": "4hour",
            "title": ids[5],
        },
        {
            "case_name": "合约结算中-1day",
            "period": "1day",
            "title": ids[6],
        },
        {
            "case_name": "合约结算中-1week",
            "period": "1week",
            "title": ids[7],
        },
        {
            "case_name": "合约结算中-1mon",
            "period": "1mon",
            "title": ids[8],
        }
    ]


    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：获取结算中合约'):
            contract_info = SwapTool.getContractStatus(instrument_status=5)
            if contract_info['isSkip']:
                assert False,'未找到结算中合约'
        with allure.step('操作：执行sub请求'):
            self.contract_code = contract_info['data']['instrument_id']
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs,keyword='tick')
            pass
        with allure.step('校验返回结果'):
            # 请求topic校验
            assert result['ch'] == "market." + self.contract_code + ".kline." + params['period']
            # 开仓价校验，不为空
            assert result['tick']['open']
            # 收仓价校验
            assert result['tick']['close']
            # 最低价校验,不为空
            assert result['tick']['low']
            # 最高价校验,不为空
            assert result['tick']['high']
            # 币的成交量
            assert result['tick']['amount'] >= 0
            # 成交量张数。 值是买卖双边之和
            assert result['tick']['vol'] >= 0
            # 成交笔数。 值是买卖双边之和
            assert result['tick']['count'] >= 0
            pass




if __name__ == '__main__':
    pytest.main()
