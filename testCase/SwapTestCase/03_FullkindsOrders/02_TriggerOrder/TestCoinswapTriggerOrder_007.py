#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_007
所属分组
    计划委托
用例标题
    计划止盈最优5/10/20挡
前置条件
    有持仓且大于等于10张，
    触发价大于最新价
步骤/文本
    1、登录币本位永续界面
    2、在当前持仓tab选择持仓BTC/USD多单，点击计划委托按钮
    3、选择计划止盈按钮
    4、输入触发价，触发价高于开仓均价和收益率自动计算（如：50000）
    4、输入卖出价选择最优5/10/20档任意一档
    5、输入卖出量10张
    6、点击止盈按钮有结果A
    7、查看当前委托列表中的计划委托有结果B
预期结果
    A)提示下单成功
    B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
用例作者
    邱大伟
自动化作者
    刘双双
"""
import common.util
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api, SwapService
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time

from config.conf import URL, ACCESS_KEY, SECRET_KEY, COMMON_ACCESS_KEY, COMMON_SECRET_KEY


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('计划止盈最优5/10/20挡')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_007:

    @allure.step('前置条件')
    def setup(self):
        print(''' 有持仓且大于等于10张，触发价大于最新价 ''')
        self.current_user = SwapService(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
        self.common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
        self.contract_type = "this_week"
        self.contract_code = "EOS-USD"
        self.symbol = "EOS"
        latest_swap_trade = self.current_user.swap_trade(contract_code=self.contract_code)
        positions_data = self.current_user.swap_account_position_info(contract_code=self.contract_code).get("data")
        print("步骤一(0): 获取最新价")
        data_r_swap_trade = latest_swap_trade.get("tick").get("data")
        self.last_price = float(data_r_swap_trade[0].get("price"))
        for each_symbol in positions_data:
            if each_symbol.get("symbol") == self.symbol:
                # 判断数量
                positions = each_symbol.get("positions")
                for p in positions:
                    available = int(p.get("available"))
                    if available >= 10:
                        print("步骤一：已满足持仓量要求，进行下一步")
                        return
                    else:
                        print("为了使持仓量满足条件, 先进行一次卖->买")
                        print("步骤一(1): 挂一个卖单")
                        r_temp_sell = self.current_user.swap_order(contract_code=self.contract_code, price=self.last_price, volume=10, direction="sell", offset="open", lever_rate=5, order_price_type="limit")
                        assert r_temp_sell.get("status") == "ok", f"下(卖)单失败：{r_temp_sell}"
                        print("步骤一(2): 挂一个买单")
                        r_temp_buy = self.current_user.swap_order(contract_code=self.contract_code, price=self.last_price, volume=10, direction="buy", offset="open", lever_rate=5, order_price_type="limit")
                        assert r_temp_buy.get("status") == "ok", f"下(买)单失败，{r_temp_buy}"
                        print("步骤一(3): 等待3s成交")
                        time.sleep(3)
                        positions_data = self.current_user.swap_account_position_info(contract_code=self.contract_code).get("data")
                        for each_symbol in positions_data:
                            if each_symbol.get("symbol") == self.symbol:
                                # 判断数量
                                positions = each_symbol.get("positions")
                                for p in positions:
                                    available = int(p.get("available"))
                                    assert available >= 10, "经过一次卖->买之后，可平量依然不足10"
                                    return
        raise BaseException("该账号在未开通{symbol}的合约交易或在{symbol}下可冻结资产不足".format(symbol=self.symbol))

    @allure.title('计划止盈最优5/10/20挡')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录币本位永续界面'):
            self.trigger_price = round(self.last_price * 1.1, 1)
            self.order_price = self.trigger_price
            tp_order_plan = self.current_user.swap_trigger_order(contract_code=self.contract_code, trigger_type="ge", trigger_price=self.trigger_price, order_price=self.order_price, order_price_type="optimal_5", volume=10, direction="sell", offset="close", lever_rate=5)
            assert tp_order_plan.get("status") == "ok", f"下计划止盈单失败, {tp_order_plan}"
            self.tp_order_id = tp_order_plan.get("data").get('order_id')
        with allure.step('2、在当前持仓tab选择持仓BTC/USD多单，点击计划委托按钮'):
            pass
        with allure.step('3、选择计划止盈按钮'):
            pass
        with allure.step('4、输入触发价，触发价高于开仓均价和收益率自动计算（如：50000）'):
            pass
        with allure.step('4、输入卖出价选择最优5/10/20档任意一档'):
            pass
        with allure.step('5、输入卖出量10张'):
            pass
        with allure.step('6、点击止盈按钮有结果A'):
            time.sleep(3)
            all_order_plans = self.current_user.swap_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            for o in all_order_plans:
                if o.get("order_id") == self.tp_order_id:
                    expected_info = {"symbol": self.symbol, "trigger_type": "ge", "volume": 10, "order_type": 1, "direction": "sell", "offset": "close", "trigger_price": self.trigger_price, "order_price": 0, "order_price_type": "optimal_5", "status": 2}
                    assert common.util.compare_dict(expected_info, o)
                    return
            raise BaseException("在当前委托单{all_order_plans}中未找到计划委托单{tp_order_id}".format(all_order_plans=all_order_plans, tp_order_id=self.tp_order_id))
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('撤单')
        r_cancel = self.current_user.swap_trigger_cancel(contract_code=self.contract_code, order_id=self.tp_order_id)
        assert r_cancel.get("status") == "ok", f"撤单失败: {r_cancel}"


if __name__ == '__main__':
    pytest.main()
