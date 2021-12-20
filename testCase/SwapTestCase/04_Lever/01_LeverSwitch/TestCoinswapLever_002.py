#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : HuiQing Yu

import random
import time

import allure
import pytest

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[3]['feature'])
@allure.story(features[3]['story'][1])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 叶永刚')
class TestCoinswapLever_002:

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境：撤单'):
            user01.swap_cancelall(contract_code=DEFAULT_CONTRACT_CODE)
            pass

    @allure.title('当前有挂单切换杠杆倍数测试')
    def test_execute(self, contract_code):
        with allure.step('操作: 挂个限价单'):
            latest_price = SwapTool.wcurrentPrice()
            user01.swap_order(contract_code=DEFAULT_CONTRACT_CODE,price=round(latest_price*0.5,2),direction='buy')
            time.sleep(1)
            pass
        with allure.step('操作: 获取可用的杠杆总数'):
            tmp = user01.swap_available_level_rate(contract_code=contract_code)
            availableLeverList = tmp['data'][0]['available_level_rate'].split(',')
            pass
        with allure.step('操作: 杠杆倍数切换为任意值'):
            availableLeverList.remove('5')
            i = random.choice(availableLeverList)
            r = user01.swap_switch_lever_rate(contract_code=contract_code, lever_rate=i)
            pass
        with allure.step('验证: 切换成功'):
            assert r['status'] == 'error' and '当前有挂单,无法切换倍数' in r['err_msg']
            pass


if __name__ == '__main__':
    pytest.main()
