#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from tool.atp import ATP
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(req 传参from,to)')  # 这里填子功能，没有的话就把本行注释掉
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
              {'case_name': '5min', 'period': '5min'},
              {'case_name': '15min', 'period': '15min'},
              {'case_name': '30min', 'period': '30min'},
              {'case_name': '60min', 'period': '60min'},
              {'case_name': '4hour', 'period': '4hour'},
              {'case_name': '1day', 'period': '1day'},
              {'case_name': '1week', 'period': '1week'},
              {'case_name': '1mon', 'period': '1mon'},
              {'case_name': '1min', 'period': '1min'}
              ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('成交更新k线'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell')
            time.sleep(1)#等待成交k线更新
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title('WS订阅K线(req)' + params['period'])
        with allure.step('执行sub请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 5
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = retryUtil(ws_user01.swap_sub,subs,'data')
            pass
        with allure.step('校验返回结果'):
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
