#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/15
# @Author  : Alex Li
"""

所属分组
    资金划转（含母子划转，借贷币划转）
用例标题
    母账户全仓划转到子账户逐仓（挂空单）
前置条件
    
步骤/文本
    1、登入U本位合约界面
    2、点击“划转”按钮
    3、币种选择（如：usdt）
    4、选择“USDT本位永续合约账户-USDT”划转到“USDT本位永续合约账户-BTC/USDT(逐仓)”
    5、输入划转金额（可转数量<划转金额<全仓账户权益）
    6、点击“确定按钮”

预期结果
    A)划转失败，报“可划转余额不足”
优先级
    1
"""


from common.LinearServiceAPI import t as linear_api
from pprint import pprint
import pytest
import allure
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('资金划转（含母子划转，借贷币划转)母子划转')  # 这里填功能
@allure.story('母账户划转到子账户')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestUSDTSwapTransfer_052:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, sub_uid):
        print("前置条件  {}".format(sub_uid))

    @allure.title('母账户全仓划转到子账户逐仓（挂空单）')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、登入合约界面'):
            pass
        with allure.step('2、进入子账号管理界面，点击“划转”按钮'):
            pass
        with allure.step('3、币种选择（如：BTC）'):
            pass
        with allure.step('4、选择“USDT本位永续合约账户-USDT”划转到“USDT本位永续合约账户-BTC/USDT(逐仓)”'):
            pass
        with allure.step('5、输入划转金额（可转数量<划转金额<全仓账户权益）'):
            pass
        with allure.step('6、点击“确定按钮”'):
            # 挂空单
            contract_code = "BTC_USDT"
            current = ATP.get_current_price(contract_code=contract_code)
            offset = 'open'
            direction = 'sell'
            res = ATP.current_user_make_order(
                contract_code=contract_code, price=current, volume=10, direction=direction, offset=offset)
            pprint(res)
            # 全仓
            margin_account = 'USDT'
            master_account_info = linear_api.linear_cross_account_info(
                margin_account=margin_account)

            pprint(master_account_info)
            # 可划转数量
            withdraw_available = -1
            # 全仓账户权益数量
            margin_balance = -1
            if master_account_info:
                margin_balance = float(
                    master_account_info['data'][0]['margin_balance'])
                withdraw_available = float(
                    master_account_info['data'][0]['withdraw_available'])
            # 划转金额大于可转数量
            assert margin_balance-withdraw_available >= 0, '账户权益数量<可划转数量'
            # 划转金额大于账户权益,可转数量<划转金额<账户权益
            amount = round(withdraw_available+0.0001, 4)
            if margin_balance > withdraw_available:
                amount = round(
                    withdraw_available+(margin_balance-withdraw_available)/2, 4)
            res = linear_api.linear_master_sub_transfer(from_margin_account='USDT', to_margin_account='BTC-USDT',
                                                        amount=amount,
                                                        sub_uid=sub_uid,
                                                        type='master_to_sub', asset="USDT")
            pprint(res)
            assert res['status'] == 'error', "划转金额大于可转数量执行成功！"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print(ATP.clean_market())
        # 撤销当前用户 某个品种所有限价挂单
        print(ATP.cancel_all_order())
        print(ATP.make_market_depth())


if __name__ == '__main__':
    pytest.main()
