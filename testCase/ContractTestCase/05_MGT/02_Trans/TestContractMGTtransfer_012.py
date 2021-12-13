#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//05 MGT//02 转账
用例标题
    结算中-运营账户转账到借贷账户    
前置条件
    
步骤/文本
    1、打开MGT后台管理系统
    2、点击财务-财务工具-转账申请，流水类型选择（运营转借贷），平种标识如（XRP），输入金额，备注
    3、输入用户的UID以及金额
    4、点击‘提交申请’按钮
    5、点击转账审核-查看详情，点击“审核通过”按钮
    6、点击转账记录，查看转账单子是否成功"
预期结果
    转账单成功
优先级
    p2
"""

import allure
import pytest
from _pytest.mark import param
from common.ContractMGTServiceAPI import t as contract_mgt_api
from common.mysqlComm import *


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('MGT')  # 这里填功能
@allure.story('转账')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 程卓')
@pytest.mark.unstable
class TestContractMGTtransfer_002:

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.title('结算中-运营账户转账到借贷账户')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('打开MGT后台管理系统点击财务-财务工具-转账申请，流水类型选择（运营转借贷），平种标识如（XRP），输入金额'):
            params = ["XRP", {
                "userAmountList": [],
                "productId":"XRP",
                "type":22,
                "quantity":"1",
                "transferOutAccount":9,
                "transferInAccount":3,
                "remark":"类型"}
            ]
            form_params = "params={}".format(str(params))
            result = contract_mgt_api.accountActionService_saveTransfer(
                form_params)
            print(result)
        with allure.step('点击转账记录，查看转账单子是否成功'):
            assert result["errorCode"] == 0
        record_id = 0
        with allure.step('点击转账记录，查看转账单子是否成功'):
            contract_trade_conn = mysqlComm(biztype='contract')
            symbol = 'XRP'
            quantity = 1
            sqlStr = f'select id from t_transfer_data where product_id="{symbol}" ' \
                     f'AND amount= {quantity} AND transfer_status=6 order by id desc limit 1'
            rec_dict_tuples = contract_trade_conn.contract_selectdb_execute(
                'contract_trade', sqlStr)
            assert rec_dict_tuples != None
            if(len(rec_dict_tuples) > 0):
                record_id = rec_dict_tuples[0]["id"]
                assert record_id > 0
        if record_id > 0:
            with allure.step('点击审核，是否成功'):
                params = [record_id, 1, '']
                form_params = "params={}".format(str(params))
                result = contract_mgt_api.checkTransferRecord(form_params)
                assert result["errorCode"] == 0

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
