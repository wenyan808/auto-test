#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/13
# @Author  : Alex Li
"""
所属分组
    资金划转（含母子划转，借贷币划转)母子划转
用例标题
    子账户划转到母账户
前置条件
    
步骤/文本
    1、登入合约界面
    2、进入子账号管理界面，点击“划转”按钮
    3、币种选择（如：BTC）
    4、选择“主账号-币本位永续合约账户”划转到“子账号-币本位永续合约账户”
    5、输入划转金额（划转金额大于账户权益）
    6、点击“确定按钮”
预期结果
    A)划转失败，报“可划转余额不足”
优先级
    1
"""


from common.ContractServiceAPI import t as contranct_api
from pprint import pprint
import pytest
import allure

from tool.atp import ATP


@allure.epic('交割合约')  # 这里填业务线
@allure.feature('资金划转（含母子划转，借贷币划转)母子划转')  # 这里填功能
@allure.story('子账户划转到母账户，输入划转金额（划转金额大于账户权益）')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestContractTransfer_016:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, sub_uid):
        print("前置条件  {}".format(sub_uid))

    @allure.title('子账户划转到母账户')
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
            symbol = "BTC"
            sub_account_info = contranct_api.contract_sub_account_info(
                symbol=symbol, sub_uid=sub_uid)

            pprint(sub_account_info)
            # 子账户权益数量
            margin_balance = -1
            if sub_account_info:
                margin_balance = float(
                    sub_account_info['data'][0]['withdraw_available'])
            # 划转金额大于子账户权益
            amount = round(margin_balance+2, 2)
            res = contranct_api.contract_master_sub_transfer(symbol=symbol,
                                                             amount=amount,
                                                             sub_uid=sub_uid,
                                                             type='sub_to_master')
            pprint(res)
            assert res['status'] == 'error', "划转金额大于账户权益数量执行成功！"
            assert res['err_msg'] == '可划转余额不足', "划转金额大于账户权益数量执行成功！"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        print('\n恢复环境操作')
        print(ATP.clean_market())
        # 撤销当前用户 某个品种所有限价挂单
        print(ATP.cancel_all_order())
        print(ATP.make_market_depth())
        print(ATP.close_all_position())


if __name__ == '__main__':
    pytest.main()
