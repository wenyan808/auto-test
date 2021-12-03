#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

import allure
import pytest
import time

from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01 as api_user01
from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_011:
    ids = [
           'TestSwapNoti_ws_kline_011',
           'TestSwapNoti_ws_kline_012',
           'TestSwapNoti_ws_kline_013',
           'TestSwapNoti_ws_kline_014',
           'TestSwapNoti_ws_kline_015',
           'TestSwapNoti_ws_kline_016',
           'TestSwapNoti_ws_kline_017',
           'TestSwapNoti_ws_kline_018',
           'TestSwapNoti_ws_kline_020'
           ]
    params = [
              {'case_name': 'WS订阅K线(req)-5min', 'period': '5min'},
              {'case_name': 'WS订阅K线(req)-15min', 'period': '15min'},
              {'case_name': 'WS订阅K线(req)-30min', 'period': '30min'},
              {'case_name': 'WS订阅K线(req)-60min', 'period': '60min'},
              {'case_name': 'WS订阅K线(req)-4hour', 'period': '4hour'},
              {'case_name': 'WS订阅K线(req)-1day', 'period': '1day'},
              {'case_name': 'WS订阅K线(req)-1week', 'period': '1week'},
              {'case_name': 'WS订阅K线(req)-1mon', 'period': '1mon'},
              {'case_name': 'WS订阅K线(req)-1min', 'period': '1min'}
              ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('成交更新k线'):
            cls.currentPrice = currentPrice()  # 最新价
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行req请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 5
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'data' in result:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '重试3次未返回预期结果'
            pass
        with allure.step('验证点:返回字段非空校验'):
            # 请求topic校验
            for data in result['data']:
                # 开仓价校验，不为空
                assert data['open'] is not None
                # 收仓价校验
                assert data['close'] is not None
                # 最低价校验,不为空
                assert data['low'] is not None
                # 最高价校验,不为空
                assert data['high'] is not None
                # 币的成交量
                assert data['amount'] >= 0
                # 成交量张数。 值是买卖双边之和
                assert data['vol'] >= 0
                # 成交笔数。 值是买卖双边之和
                assert data['count'] >= 0
            pass


if __name__ == '__main__':
    pytest.main()
