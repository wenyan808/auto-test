#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

import allure
import pytest
import time
from config.case_content import epic,features
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL


@allure.epic(epic[1])
@allure.feature(features[1]['feature'])
@allure.story(features[1]['story'][2])
@allure.tag('Script owner : 张广南', 'Case owner : 叶永刚')
@pytest.mark.stable
@pytest.mark.transfer
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
            amount = round(float(self.f_account)+1,6)
            for i in range(3):
                result = user01.swap_master_sub_transfer(sub_uid='115395803',contract_code=self.contract_code,amount=amount,type='master_to_sub')
                if '访问次数超出限制' in result['err_msg']:
                    print('接口限频，第{}次重试……'.format(i+1))
                    time.sleep(1)
                else:
                    break
            pass
        with allure.step("验证：划转失败并提示-可划转余额不足"):
            assert 'error' in result['status'] and '可划转余额不足' in result['err_msg']
            pass



if __name__ == '__main__':
    pytest.main()
