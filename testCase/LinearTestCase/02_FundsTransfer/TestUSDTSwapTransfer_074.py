#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/18
# @Author  : Alex Li
"""

所属分组
    资金划转（含母子划转，借贷币划转）
用例标题
    子账户逐仓划转到母账户逐仓
前置条件
    
步骤/文本
    1、登入U本位合约界面
    2、点击“划转”按钮
    3、币种选择（如：usdt）
    4、选择“USDT本位永续合约账户-USDT”划转到“USDT本位永续合约账户-BTC/USDT(逐仓)”
    5、输入划转金额（可转数量<逐仓账户权益）
    6、点击“确定按钮”

预期结果
    A)划转失败，报“可划转余额不足”
优先级
    1
"""


from pprint import pprint

import allure
import pytest

from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('资金划转（含母子划转，借贷币划转)母子划转')  # 这里填功能
@allure.story('子账户逐仓划转到母账户逐仓')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestUSDTSwapTransfer_074:

    @allure.step('前置条件')
    def setup(self):
        print("前置条件")

    @allure.title('子账户逐仓划转到母账户逐仓')
    @allure.step('测试执行')
    def test_execute(self, sub_uid, symbol, contract_code):
        with allure.step('1、登入合约界面'):
            pass
        with allure.step('2、进入子账号管理界面，点击“划转”按钮'):
            pass
        with allure.step('3、币种选择（如：BTC）'):
            pass
        with allure.step('4、选择“USDT本位永续合约账户-USDT”划转到“USDT本位永续合约账户-BTC/USDT(逐仓)”'):
            pass
        with allure.step('5、输入划转金额（可转数量<逐仓账户权益）'):
            pass
        with allure.step('6、点击“确定按钮”'):

            # 子账户逐仓
            asset = linear_api.get_trade_partition(contract_code)
            master_account_info = linear_api.linear_sub_account_info(
                contract_code=contract_code, sub_uid=sub_uid)

            pprint(master_account_info)
            # 权益数量
            margin_balance = -1
            if master_account_info:
                margin_balance = float(
                    master_account_info['data'][0]['margin_balance'])
            # 划转金额大于可转数量
            amount = round(margin_balance+2, 2)
            res = linear_api.linear_master_sub_transfer(from_margin_account=contract_code, to_margin_account=contract_code,
                                                        amount=amount,
                                                        sub_uid=sub_uid,
                                                        type='sub_to_master', asset=asset)
            pprint(res)
            assert res['status'] == 'error', "划转金额大于可转数量执行成功！"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
