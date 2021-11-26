#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210916
# @Author : HuiQing Yu

import allure
import pytest
import random
import time
from common.CommonUtils import currentPrice
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[3]['feature'])
@allure.story(features[3]['story'][1])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 叶永刚')
class TestCoinswapLever_002:

    @allure.title('当前无挂单切换杠杆倍数测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('操作: 挂个限价单'):
            latest_price = currentPrice()
            user01.swap_order(contract_code=DEFAULT_CONTRACT_CODE,price=round(latest_price*0.5,2),direction='buy')
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
