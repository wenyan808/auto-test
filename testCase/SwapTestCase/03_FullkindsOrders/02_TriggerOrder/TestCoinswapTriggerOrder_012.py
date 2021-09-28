#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 邱大伟

#script by: lss
用例编号
    TestCoinswapTriggerOrder_012
所属分组
    计划委托
用例标题
    撤销计划委托订单开仓测试
前置条件
    不要触发
步骤/文本
    1、登录币本位永续界面
    2、选择BTC/USD，选择杠杆5X，点击开仓-计划按钮
    3、输入触发价（如：50000）
    4、输入买入价，偏离最新价不要成交（如：40000）
    5、输入买入量10张
    6、点击买入开多按钮后弹框确认后有结果A
    7、查看当前委托列表中的计划委托有结果B
    8、点击撤销按钮有结果C
    9、检查历史委托-计划委托界面有结果D
预期结果
    A)提示下单成功
    B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
    C)提示撤销申请成功，当前委托-计划委托列表订单消失
    D)在历史委托-计划委托中有撤销订单记录，且各项信息和下单数据一致
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

from config.conf import URL, ACCESS_KEY, COMMON_ACCESS_KEY, SECRET_KEY, COMMON_SECRET_KEY


@allure.epic('所属分组')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('撤销计划委托订单开仓测试')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapTriggerOrder_012:

    @allure.step('前置条件')
    def setup(self):
        print(''' 不要触发 ''')

    @allure.title('撤销计划委托订单开仓测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、登录币本位永续界面'):
            print(''' 选择正常限价下单 ''')
            self.current_user = SwapService(url=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
            self.common_user = SwapService(url=URL, access_key=COMMON_ACCESS_KEY, secret_key=COMMON_SECRET_KEY)
            self.contract_type = "this_week"
            self.contract_code = "EOS-USD"
            self.symbol = "EOS"
            self.lever_rate = 5
            latest_swap_trade = self.current_user.swap_trade(contract_code=self.contract_code)
            print("步骤一(0): 获取最新价")
            data_r_swap_trade = latest_swap_trade.get("tick").get("data")
            self.last_price = float(data_r_swap_trade[0].get("price"))
            self.trigger_price = self.last_price
            self.trigger_type = "ge"
            self.order_price = round(self.last_price * 0.9, 1)
        with allure.step('2、选择BTC/USD，选择杠杆5X，点击开仓-计划按钮'):
            r_new_open = self.current_user.swap_trigger_order(contract_code=self.contract_code, trigger_type=self.trigger_type, trigger_price=self.trigger_price, order_price=self.order_price, volume=10, direction="buy", offset="open", lever_rate=self.lever_rate)
            assert r_new_open.get("status") == "ok", f"下单失败: {r_new_open}"
            order_id_open = r_new_open.get("data").get("order_id")
        with allure.step('3、输入触发价（如：50000）'):
            pass
        with allure.step('4、输入买入价，偏离最新价不要成交（如：40000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮后弹框确认后有结果A'):
            pass
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            time.sleep(3)
            all_order_plans = self.current_user.swap_trigger_openorders(contract_code=self.contract_code).get("data").get("orders")
            checked = False
            for o in all_order_plans:
                if o.get("order_id") == order_id_open:
                    expected_info = {"symbol": self.symbol, "trigger_type": self.trigger_type, "volume": 10, "direction": "buy", "offset": "open", "trigger_price": self.trigger_price, "order_price": self.order_price, "status": 2}
                    assert common.util.compare_dict(expected_info, o)
                    checked = True
                    break
            if not checked:
                raise BaseException("在当前委托单{all_order_plans}中未找到计划委托单{order_id}".format(all_order_plans=all_order_plans, order_id=order_id_open))
        with allure.step('8、点击撤销按钮有结果C'):
            r_cancel_order = self.current_user.swap_trigger_cancel(contract_code=self.contract_code, order_id=order_id_open)
            assert r_cancel_order.get("status") == "ok", f"撤单失败: {r_cancel_order}"
            time.sleep(3)
        with allure.step('9、检查历史委托-计划委托界面有结果D'):
            """
                contract_code	true	string	合约代码		BTC-USD
                trade_type	true	int	交易类型		0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多；后台是根据该值转换为offset和direction，然后去查询的； 其他值无法查询出结果
                status	true	String	订单状态		多个以英文逗号隔开，计划委托单状态：0:全部（表示全部结束状态的订单）、4:已委托、5:委托失败、6:已撤单
                create_date	true	int	日期		可随意输入正整数，如果参数超过90则默认查询90天的数据
                page_index	false	int	页码，不填默认第1页	1	第几页，不填默认第一页
                page_size	false	int	不填默认20，不得多于50	20	不填默认20，不得多于50
                sort_by	false	string	排序字段（降序），不填默认按照created_at降序	"created_at"：按订单创建时间进行降序，"update_time"：按订单更新时间进行降序
            """
            all_his_orders = self.current_user.swap_trigger_hisorders(contract_code=self.contract_code, trade_type=1, status="6", create_date=7).get("data").get("orders")
            actual_order = [i for i in all_his_orders if i.get("order_id") == order_id_open]
            assert len(actual_order) == 1, f"找不到期望的计划委托单或有多个这样的计划委托单, 实际单号列表为: {all_his_orders}"
            actual_order = actual_order[0]
            expected_info = {"symbol": self.symbol, "trigger_type": self.trigger_type, "volume": 10, "direction": "buy", "offset": "open", "trigger_price": self.trigger_price, "order_price": self.order_price, "status": 6}
            assert common.util.compare_dict(expected_info, actual_order)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
