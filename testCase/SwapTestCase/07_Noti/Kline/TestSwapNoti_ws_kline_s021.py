#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211013
# @Author : HuiQing Yu

import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_s021:

    ids = ['TestSwapNoti_ws_kline_021',
           'TestSwapNoti_ws_kline_027',
           'TestSwapNoti_ws_kline_033',
           'TestSwapNoti_ws_kline_039',
           'TestSwapNoti_ws_kline_045',
           'TestSwapNoti_ws_kline_051',
           'TestSwapNoti_ws_kline_057',
           'TestSwapNoti_ws_kline_063',
           'TestSwapNoti_ws_kline_069']
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


    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param):
        allure.dynamic.title(param['title'])
        with allure.step('操作：获取合约'):
            contract_info = SwapTool.getContractStatus(instrument_status=0)
            if contract_info['isSkip']:
                assert False,'未找到-已下市合约'
            pass
        with allure.step('操作：执行sub请求'):
            self.contract_code = contract_info['data']['instrument_id']
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, param['period']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs)
            pass
        with allure.step('校验返回结果'):
            assert 'invalid topic' in str(result),'下已市校验失败'
            pass



if __name__ == '__main__':
    pytest.main()
