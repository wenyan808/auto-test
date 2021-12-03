#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211104
# @Author : HuiQing Yu


import time

import allure
import pytest

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
@pytest.mark.stable
class TestSwapTriggerCancelAll_001:

    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->计划委托下单(多单)'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            trigger_price = round(cls.currentPrice, 2)
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= cls.currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            cls.orderInfoList = []
            for i in range (3):
                orderInfo = user01.swap_trigger_order(contract_code=cls.contract_code, trigger_price=trigger_price,
                                                           trigger_type=trigger_type,offset='open',
                                                           order_price=trigger_price, direction='buy', volume=1)
                cls.orderInfoList.append(orderInfo['data']['order_id'])
            pass

    def test_execute(self, contract_code):
        with allure.step('*->计划委托订单全部撤单'):
            time.sleep(1)
            cancelResult = user01.swap_trigger_cancelall(contract_code=contract_code)
            pass
        with allure.step('验证撤单订单结果返回'):
            assert cancelResult['status'] == 'ok'
            for orderId in self.orderInfoList:
                assert str(orderId) in cancelResult['data']['successes']
            pass



if __name__ == '__main__':
    pytest.main()
