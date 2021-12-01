#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211011
# @Author : DongLin Han

from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
@allure.tag('Script owner : 韩东林', 'Case owner : 柳攀峰')
@pytest.mark.stable
class TestSwapNoti_012:
    contract_code = DEFAULT_CONTRACT_CODE
    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.currentPrice = currentPrice()
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

    @allure.title('请求BBO(单个合约，即传参code)')
    def test_execute(self):
        with allure.step('操作：执行api-restful请求'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = api_user01.swap_bbo(contract_code=self.contract_code)
                if 'ticks' in result:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '未返回预期结果'

            pass
        with allure.step('验证：返回结果ask字段不为空'):
            assert result['ticks'][0]['ask']
            pass
        with allure.step('验证：返回结果bid字段不为空'):
            assert result['ticks'][0]['bid']
            pass


if __name__ == '__main__':
    pytest.main()
