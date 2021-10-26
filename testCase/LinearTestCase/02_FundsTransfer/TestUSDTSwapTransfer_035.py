#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/15
# @Author  : Alex Li
"""

所属分组
    资金划转（含母子划转，借贷币划转）
用例标题
    跨账户划转,逐仓划转到逐仓
前置条件
    
步骤/文本
    1、登入U本位合约界面
    2、点击“划转”按钮
    3、币种选择（如：usdt）
    4、选择“USDT本位永续合约账户-USDT”划转到“USDT本位永续合约账户-BTC/USDT(逐仓)”
    5、输入划转金额（划转金额大于逐仓账户权益数量）
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
@allure.story('跨账户划转')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestUSDTSwapTransfer_035:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, sub_uid):
        print("前置条件  {}".format(sub_uid))

    @allure.title('跨账户划转,逐仓划转到逐仓')
    @allure.step('测试执行')
    def test_execute(self, sub_uid):
        with allure.step('1、登入合约界面'):
            pass
        with allure.step('2、进入子账号管理界面，点击“划转”按钮'):
            pass
        with allure.step('3、币种选择（如：BTC）'):
            pass
        with allure.step('4、选择“主账号-币本位永续合约账户”划转到“子账号-币本位永续合约账户”'):
            pass
        with allure.step('5、输入划转金额（划转金额大于账户权益）'):
            pass
        with allure.step('6、点击“确定按钮”'):
            # 逐仓
            contract_code = 'BTC-USDT'
            master_account_info = linear_api.linear_account_info(
                contract_code=contract_code)

            pprint(master_account_info)
            # 权益数量
            margin_balance = -1
            if master_account_info:
                margin_balance = float(
                    master_account_info['data'][0]['margin_balance'])
            # 划转金额大于可转数量
            amount = round(margin_balance+2, 2)
            res = linear_api.linear_transfer_inner(from_margin_account=contract_code, to_margin_account='ETH-USDT',
                                                   amount=amount, asset="USDT")
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
