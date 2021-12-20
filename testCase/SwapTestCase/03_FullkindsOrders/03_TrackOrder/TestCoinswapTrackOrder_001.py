#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : 余辉青


import allure
import pytest
import time

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from tool.SwapTools import SwapTool
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][3])
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 封泰')
class TestCoinswapTrackOrder_001:
    ids = ["TestCoinswapTrackOrder_001_buy",
           "TestCoinswapTrackOrder_001_sell",
           "TestCoinswapTrackOrder_002_buy",
           "TestCoinswapTrackOrder_002_sell",
           ]
    params = [
        {
            "case_name": "跟踪委托单-理论价格下撤单测试",
            "direction": "buy",
            "ratio":0.99,
            "order_price_type": "formula_price",
            "trade_type":1
        }, {
            "case_name": "跟踪委托单-理论价格下撤单测试",
            "direction": "sell",
            "order_price_type": "formula_price",
            "ratio": 1.01,
            "trade_type":2
        },{
            "case_name": "跟踪委托单-最优档下撤单测试",
            "direction": "buy",
            "ratio":0.99,
            "order_price_type": "optimal_5",
            "trade_type":1
        }, {
            "case_name": "跟踪委托单-最优档下撤单测试",
            "direction": "sell",
            "order_price_type": "optimal_5",
            "ratio": 1.01,
            "trade_type":2
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01.swap_track_cancelall(contract_code=cls.contract_code)  # 避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：下跟踪委托单'):
            track_order = user01.swap_track_order(contract_code=self.contract_code, volume=1, offset='open',
                                                  lever_rate=5, callback_rate=0.05,
                                                  active_price=round(self.latest_price*params['ratio'],2),
                                                  order_price_type=params['order_price_type'],
                                                  direction=params['direction'])
            pass
        with allure.step('验证：下单成功'):
            order_id = track_order['data']['order_id_str']
            assert 'ok' in track_order['status'] and order_id
            pass
        with allure.step("验证：存在跟踪委托当前委托列表"):
            time.sleep(1)#等待数据更新
            cur_list_order = user01.swap_track_openorders(contract_code=self.contract_code,trade_type=params['trade_type'],page_index=1,page_size=3)
            flag = False
            for order in cur_list_order['data']['orders']:
                if order_id in order['order_id_str']:
                    flag = True
                    break
            assert flag,'未存在当前委托列表'
            pass
        with allure.step("操作：撤销跟踪委托"):
            user01.swap_track_cancel(contract_code=self.contract_code,order_id=order_id)
            pass
        with allure.step("验证：存在跟踪委托历史委托中"):
            time.sleep(1)#等待操作更新
            his_list_order = user01.swap_track_hisorders(contract_code=self.contract_code,status=6,trade_type=params['trade_type'],create_date=1,page_size=3,page_index=1)
            flag = False
            for order in his_list_order['data']['orders']:
                if order_id in order['order_id_str']:
                    flag = True
                    break
            assert flag, '未存在历史委托列表'
            pass



if __name__ == '__main__':
    pytest.main()
