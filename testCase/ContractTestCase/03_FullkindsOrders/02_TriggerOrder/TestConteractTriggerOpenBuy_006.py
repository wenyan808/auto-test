#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210930
# @Author : alex
    用例标题
        计划委托买入开多触发价等于最新价
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮
        3、输入触发价（如：50000，最新价：50000）
        4、输入买入价（如：45000）
        5、输入买入量10张
        6、点击买入开多按钮，弹框点击确认
    预期结果
        A)提示下单成功
        B)当前委托-计划委托列表查询创建订单（可能会触发订单）
    优先级
        1
    用例别名
        TestConteractTriggerOpenBuy_006
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceAPI import common_user_contract_service_api as common_contract_api
from pprint import pprint
import pytest
import allure
import time
from tool.atp import ATP


@allure.epic('交割合约')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('正常限价开仓')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : Alex Li', 'Case owner : 邱大伟')
class TestConteractTriggerOpenBuy_006:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, symbol_period):
        self.symbol = symbol
        print(symbol_period)
        self.symbol = symbol
        ATP.make_market_depth()

    @allure.title('计划委托买入开多触发价等于最新价')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        volume = 1
        direction = 'buy'
        offset = 'open'
        leverRate = 5
        trigger_type = "ge"
        contract_type = "this_week"
        print('\n步骤一:获取最近价\n')
        lastprice = ATP.get_current_price(contract_code=symbol_period)
        triggerPrice = round(lastprice, 2)
        orderPrice = round(lastprice, 2)
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50000）'):
            pass
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮，弹框点击确认'):
            common_contract_api.contract_order(
                symbol=symbol, contract_type="limit", volume=volume, direction="sell",
                offset=offset, lever_rate=leverRate)
            r = contract_api.contract_trigger_order(symbol=symbol, trigger_type=trigger_type, trigger_price=triggerPrice, contract_type=contract_type,
                                                    order_price=orderPrice, volume=volume, direction=direction,
                                                    offset=offset, lever_rate=leverRate)
            print(r)
            order_id = r['data']['order_id']
            print(order_id)

            ATP.make_market_depth(depth_count=2)
            time.sleep(1)
            res = contract_api.contract_trigger_openorders(
                symbol=symbol)
            print(res)
            hits = 0
            if(len(res["data"]["orders"]) > 0):
                for kw in res["data"]["orders"]:
                    if order_id == kw['order_id']:
                        hits += 1
                        break
                assert hits > 0

    @allure.step('恢复环境')
    def teardown(self):
        ATP.clean_market()
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
