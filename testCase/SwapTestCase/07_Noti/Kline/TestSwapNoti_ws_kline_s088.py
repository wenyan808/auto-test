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
class TestSwapNoti_ws_kline_s088:

    ids = ['TestSwapNoti_ws_kline_088',
           'TestSwapNoti_ws_kline_094',
           'TestSwapNoti_ws_kline_100',
           'TestSwapNoti_ws_kline_106',
           'TestSwapNoti_ws_kline_112',
           'TestSwapNoti_ws_kline_118',
           'TestSwapNoti_ws_kline_124',
           'TestSwapNoti_ws_kline_130',
           'TestSwapNoti_ws_kline_136']
    params = [
        {
            "case_name": "合约结算-1min",
            "period": "1min",
            "title": ids[0],
        },
        {
            "case_name": "合约结算-5min",
            "period": "5min",
            "title": ids[1],
        },
        {
            "case_name": "合约结算-15min",
            "period": "15min",
            "title": ids[2],
        },
        {
            "case_name": "合约结算-30min",
            "period": "30min",
            "title": ids[3],
        },
        {
            "case_name": "合约结算-60min",
            "period": "60min",
            "title": ids[4],
        },
        {
            "case_name": "合约结算-4hour",
            "period": "4hour",
            "title": ids[5],
        },
        {
            "case_name": "合约结算-1day",
            "period": "1day",
            "title": ids[6],
        },
        {
            "case_name": "合约结算-1week",
            "period": "1week",
            "title": ids[7],
        },
        {
            "case_name": "合约结算-1mon",
            "period": "1mon",
            "title": ids[8],
        }
    ]

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param):
        allure.dynamic.title(param['title'])
        with allure.step('操作：获取合约'):
            contract_info = SwapTool.getContractStatus(instrument_status=0)
            if contract_info['isSkip']:
                assert False, '未找到结算中合约'
            pass
        with allure.step('操作：执行req请求'):
            self.contract_code = contract_info['data']['instrument_id']
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24
            subs = {
                "req": f"market.{self.contract_code}.kline.{param['period']}",
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = ws_user01.swap_sub(subs)
            pass
        with allure.step('验证：返回结果提示invalid topic'):
            assert 'error' in result['status'], 'status-校验失败'
            assert 'invalid topic' in result['err-msg'], 'err-msg-校验失败'
            pass


if __name__ == '__main__':
    pytest.main()
