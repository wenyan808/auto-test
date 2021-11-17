#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil,currentPrice

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_001:
    ids = [
           'TestSwapNoti_ws_kline_002',
           'TestSwapNoti_ws_kline_003',
           'TestSwapNoti_ws_kline_004',
           'TestSwapNoti_ws_kline_005',
           'TestSwapNoti_ws_kline_006',
           'TestSwapNoti_ws_kline_007',
           'TestSwapNoti_ws_kline_008',
           'TestSwapNoti_ws_kline_009',
           'TestSwapNoti_ws_kline_019'
           ]
    params = [
              {'case_name': 'WS订阅K线(sub)-5min', 'period': '5min'},
              {'case_name': 'WS订阅K线(sub)-15min', 'period': '15min'},
              {'case_name': 'WS订阅K线(sub)-30min', 'period': '30min'},
              {'case_name': 'WS订阅K线(sub)-60min', 'period': '60min'},
              {'case_name': 'WS订阅K线(sub)-4hour', 'period': '4hour'},
              {'case_name': 'WS订阅K线(sub)-1day', 'period': '1day'},
              {'case_name': 'WS订阅K线(sub)-1week', 'period': '1week'},
              {'case_name': 'WS订阅K线(sub)-1mon', 'period': '1mon'},
              {'case_name': 'WS订阅K线(sub)-1min', 'period': '1min'}
            ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()  # 最新价
        api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.01, 2), direction='buy')
        api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.01, 2), direction='sell')

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub请求'):
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id1"
            }
            result = retryUtil(ws_user01.swap_sub,subs,'tick')
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
            assert result['tick']['amount']>=0
            # 成交量张数。 值是买卖双边之和
            assert result['tick']['vol']>=0
            # 成交笔数。 值是买卖双边之和
            assert result['tick']['count']>=0
            pass



if __name__ == '__main__':
    pytest.main()
