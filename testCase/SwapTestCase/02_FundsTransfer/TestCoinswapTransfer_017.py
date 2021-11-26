#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : HuiQing Yu

import allure
import pytest
import random
from common.SwapServiceAPI import user01,user01Child01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from common.CommonUtils import currentPrice

@allure.epic('反向永续')
@allure.feature('资金划转')
@allure.story('母子划转')
@allure.tag('Script owner : Alex Li', 'Case owner : 叶永刚')
@pytest.mark.stable
class TestCoinSwapTransfer_017:

    ids = ["TestCoinSwapTransfer_017","TestCoinSwapTransfer_018"]
    params = [
        {
            "case_name": "母账户划转到子账号-有挂(多)单-可转数量<划转金额<账户权益",
            "ratio": 0.5,
            "direction":"buy"
        },{
            "case_name": "母账户划转到子账号-有挂(空)单-可转数量<划转金额<账户权益",
            "ratio": 1.5,
            "direction":"sell"
        }
    ]

    @classmethod
    def setup_class(cls):
        with allure.step("变量初始化"):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.latest_price = currentPrice()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤销挂单'):
            user01Child01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step("操作：挂单"):
            user01Child01.swap_order(contract_code=self.contract_code,price=round(self.latest_price*params['ratio'],2),
                              direction=params['direction'],)
            pass
        with allure.step('操作：获取当前子账号可划转资金信息'):
            c_account_info = user01Child01.swap_account_info(contract_code=self.contract_code)
            margin_balance=c_account_info['data'][0]['margin_balance']
            withdraw_available=c_account_info['data'][0]['withdraw_available']
            amount = round(random.uniform(withdraw_available, margin_balance),8)
            print('子账户：账户权益={}，划转金额={},可划转金额={}'.format(margin_balance,amount,withdraw_available))
            pass
        with allure.step("操作：执行划转，子 划 母"):
            result = user01.swap_master_sub_transfer(sub_uid='115395803',contract_code=self.contract_code,amount=amount,type='sub_to_master')
            pass
        with allure.step("验证：划转失败并提示-可划转余额不足"):
            assert 'error' in result['status'] and '可划转余额不足' in result['err_msg']
            pass



if __name__ == '__main__':
    pytest.main()
