#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211011
# @Author : DongLin Han

from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from tool.SwapTools import SwapTool
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
@allure.tag('Script owner : 韩东林', 'Case owner : 柳攀峰')
@pytest.mark.stable
class TestSwapNoti_011:
    contract_code = DEFAULT_CONTRACT_CODE
    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.currentPrice = SwapTool.currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * 0.5, 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * 1.5, 2),
                                  direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤盘'):
            time.sleep(1)
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @allure.title('请求深度(150档不合并)')
    def test_execute(self):
        with allure.step('操作：执行api-restful请求'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                result = api_user01.swap_depth(contract_code=self.contract_code, type='step6')
                if 'tick' in result:
                    if result['tick']['asks'] and result['tick']['bids']:
                        flag = True
                        break
                time.sleep(1)
                print(f'未返回预期结果，第{i + 1}次重试………………………………')
            assert flag, '未返回预期结果'

            pass
        with allure.step('验证：返回结果asks字段不为空'):
            assert result['tick']['asks']
            pass
        with allure.step('验证：返回结果bids字段不为空'):
            assert result['tick']['bids']
            pass




if __name__ == '__main__':
    pytest.main()
