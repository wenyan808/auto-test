#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/18
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//03 正向永续//09 订单推送
用例标题
    订阅逐仓订单撮合（有订单撮合）
前置条件
    
步骤/文本
    成功建立和 WebSocket API 的连接之后，向server发送数据订阅，数据格式参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-5

预期结果
    订阅成功，返回'err-code': 0，订阅成功之后有新的推送
优先级
    0
"""

from pprint import pprint
import pytest
import allure
import time
from tool.atp import ATP
from common.LinearServiceWS import t as linear_service_ws


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('订单推送')  # 这里填功能
@allure.story('订阅逐仓订单撮合（有订单撮合）')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 柳攀峰')
# @pytest.mark.stable
class TestLinearNotification_017:

    @allure.step('前置条件:非colo域名')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        print("前置条件  {}".format(contract_code))

    @allure.title('订阅逐仓订单撮合（有订单撮合）')
    @allure.step('测试执行')
    def test_execute(self):
        contract_code = 'BSV-USDT'
        with allure.step('1、订阅逐仓订单撮合（有订单撮合）'):
            sub = {
                "op": "sub",
                "cid": 11538447,
                "topic": "matchOrders.{}".format(contract_code)
            }
            result = linear_service_ws.linear_notification(sub)
            pprint(result)
            # 订单撮合
            current = ATP.get_current_price(contract_code=contract_code)
            offset = 'open'
            direction = 'buy'
            order_price_type = "limit"
            ATP.common_user_make_order(order_price_type=order_price_type, contract_code=contract_code,
                                       price=current, volume=1, direction="sell", offset=offset)
            res = ATP.current_user_make_order(order_price_type=order_price_type, contract_code=contract_code,
                                              price=current, volume=1, direction=direction, offset=offset)
            pprint(res)

            time.sleep(1)

            result = linear_service_ws.linear_notification(sub)
            pprint(result)

            assert result["op"] == "sub" and result["err-code"] == 0

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        # 撤销当前用户 某个品种所有限价挂单


if __name__ == '__main__':
    pytest.main()
