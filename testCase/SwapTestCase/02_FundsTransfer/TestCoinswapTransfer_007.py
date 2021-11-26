#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

import allure
import pytest

from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL


@allure.epic('反向永续')
@allure.feature('02资金划转')
@allure.story('02母子划转')
@allure.tag('Script owner : 张广南', 'Case owner : 叶永刚')
@pytest.mark.stable
class TestCoinSwapTransfer_007:

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            pass
        with allure.step('获取当前母账号可划转资金信息'):
            f_account_info = user01.swap_account_info(contract_code=cls.contract_code)
            cls.f_account=f_account_info['data'][0]['withdraw_available']
            print('母账户可划转金额={}'.format(cls.f_account))
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass
    @allure.title('母账户划转到子账号-划转金额大于可转数量')
    def test_execute(self, contract_code):
        with allure.step("操作：执行划转，母 划 子"):
            amount = float(self.f_account)+1
            result = user01.swap_master_sub_transfer(sub_uid='115395803',contract_code=self.contract_code,amount=amount,type='master_to_sub')
            pass
        with allure.step("验证：划转失败并提示-可划转余额不足"):
            assert 'error' in result['status'] and '可划转余额不足' in result['err_msg']
            pass



if __name__ == '__main__':
    pytest.main()
