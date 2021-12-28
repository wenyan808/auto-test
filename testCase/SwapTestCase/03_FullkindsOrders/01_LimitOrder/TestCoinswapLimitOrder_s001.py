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
@allure.story(features[2]['story'][1])
@pytest.mark.stable
@allure.tag('Script owner : 陈维', 'Case owner : 吉龙')
class TestCoinswapLimitOrder_s001:
    ids = ["TestCoinswapLimitOrder_001","TestCoinswapLimitOrder_002"]
    params = [
        {   "title":"TestCoinswapLimitOrder_001",
            "case_name": "限价委托输入价格下单买入开多后撤单测试",
            "ratio": 0.9,
            "direction": "buy",
            "trade_type":1
        },{"title":"TestCoinswapLimitOrder_002",
            "case_name": "限价委托输入价格下单卖出开空后撤单测试",
            "ratio": 1.1,
            "direction": "sell",
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
            time.sleep(1)
            user01.swap_cancelall(contract_code=cls.contract_code)#避免用例失败未能撤销订单
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['title'])
        with allure.step('操作：下限价单，格为当前价一半，使订单挂盘'):
            limit_order = user01.swap_order(contract_code=self.contract_code,price=round(self.latest_price*params['ratio'],2),
                                            direction=params['direction'])
        with allure.step('验证：下单成功'):
            order_id = limit_order['data']['order_id']
            assert 'ok' in limit_order['status'] and order_id
        with allure.step('操作：获取订单信息'):
            limit_order_info = user01.swap_order_info(order_id=order_id,contract_code=self.contract_code)
            pass
        with allure.step('验证：订单信息与下单一致'):
            assert self.contract_code == limit_order_info['data'][0]['contract_code'],'合约状态不一致'
            assert 1 == limit_order_info['data'][0]['volume'],'下单数量校验失败'
            assert params['direction'] == limit_order_info['data'][0]['direction'],'下单方向校验失败'
            assert 5 == limit_order_info['data'][0]['lever_rate'],'下单杠杆校验失败'
            assert 1 == limit_order_info['data'][0]['order_type'],'订单类型校验失败'
            assert 1 or 3 == limit_order_info['data'][0]['status'],'订单状态校验失败'
            assert 0 == limit_order_info['data'][0]['is_tpsl'],'止盈止损是否设置校验失败'
            assert round(self.latest_price*params['ratio'],2) == limit_order_info['data'][0]['price'],'下单价格校验失败'
        with allure.step("操作：获取用户资金信息-得出冻结资金"):
            time.sleep(1)
            account_info = user01.swap_account_info(contract_code=self.contract_code)
            cur_margin_frozen =account_info['data'][0]['margin_frozen']
        with allure.step('验证：冻结保证金'):
            assert cur_margin_frozen == limit_order_info['data'][0]['margin_frozen'], '冻结保证金校验失败'
        with allure.step("操作：查询限价单列表-未成交委托"):
            flag = False
            for i in range(3):
                limit_list = user01.swap_openorders(contract_code=self.contract_code,page_size=1,page_index=1,trade_type=params['trade_type'])
                if len(limit_list['data']['orders']) == 1 and order_id == limit_list['data']['orders'][0]['order_id']:
                    flag = True
                    break
                else:
                    print('获取限价委托列表数据，第{}次重试……'.format(i+1))
                    time.sleep(1)
        with allure.step("验证：订单存在限价委托列表中"):
            assert flag,'订单未存在列表中'
        with allure.step("操作：撤销订单"):
            user01.swap_cancelall(contract_code=self.contract_code)
            time.sleep(1)
        with allure.step("验证：冻结资金恢复"):
            account_info = user01.swap_account_info(contract_code=self.contract_code)
            cur_margin_frozen = account_info['data'][0]['margin_frozen']
            assert cur_margin_frozen == 0E-18, '冻结保证金校验失败'
            pass

if __name__ == '__main__':
    pytest.main()
