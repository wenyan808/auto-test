#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211014
# @Author : HuiQing Yu
from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.case_content import epic, features
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_s084:

    ids = ['TestSwapNoti_ws_kline_084',
           'TestSwapNoti_ws_kline_090',
           'TestSwapNoti_ws_kline_096',
           'TestSwapNoti_ws_kline_102',
           'TestSwapNoti_ws_kline_108',
           'TestSwapNoti_ws_kline_114',
           'TestSwapNoti_ws_kline_120',
           'TestSwapNoti_ws_kline_126',
           'TestSwapNoti_ws_kline_132']
    params = [
        {
            "case_name": "合约已下市-1min",
            "period": "1min",
            "title": ids[0],
        },
        {
            "case_name": "合约已下市-5min",
            "period": "5min",
            "title": ids[1],
        },
        {
            "case_name": "合约已下市-15min",
            "period": "15min",
            "title": ids[2],
        },
        {
            "case_name": "合约已下市-30min",
            "period": "30min",
            "title": ids[3],
        },
        {
            "case_name": "合约已下市-60min",
            "period": "60min",
            "title": ids[4],
        },
        {
            "case_name": "合约已下市-4hour",
            "period": "4hour",
            "title": ids[5],
        },
        {
            "case_name": "合约已下市-1day",
            "period": "1day",
            "title": ids[6],
        },
        {
            "case_name": "合约已下市-1week",
            "period": "1week",
            "title": ids[7],
        },
        {
            "case_name": "合约已下市-1mon",
            "period": "1mon",
            "title": ids[8],
        }
    ]

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['title'])
        with allure.step('操作：获取合约'):
            contract_info = SwapTool.getContractStatus(instrument_status=0)
            if contract_info['isSkip']:
                assert False, '未找到已下市合约'
            pass
        with allure.step('操作：执行req请求'):
            self.contract_code = contract_info['data']['instrument_id']
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24
            subs = {
                "req": f"market.{self.contract_code}.kline.{params['period']}",
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'invalid topic' in result['err-msg']
            pass


if __name__ == '__main__':
    pytest.main()
