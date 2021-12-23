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


@allure.epic(epic[1])
@allure.feature(features[3]['feature'])
@allure.story(features[3]['story'][1])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 叶永刚')
class TestCoinswapLever_001:

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境：杠杆改回原倍数'):
            time.sleep(3)#避免用例执行太快被访问限制
            user01.swap_switch_lever_rate(contract_code=DEFAULT_CONTRACT_CODE, lever_rate=5)
            pass

    @allure.title('当前无挂单切换杠杆倍数测试')
    def test_execute(self, contract_code):
        with allure.step('操作: 获取可用的杠杆总数'):
            availableLeverList = [1,2,3,10,20,30,50,75]
            pass
        with allure.step('操作: 杠杆倍数切换为任意值'):
            i = random.choice(availableLeverList)
            r = user01.swap_switch_lever_rate(contract_code=contract_code, lever_rate=i)
            pass
        with allure.step('验证: 切换成功'):
            assert r['status'] == 'ok' and int(i) == r['data']['lever_rate']
            pass


if __name__ == '__main__':
    pytest.main()
