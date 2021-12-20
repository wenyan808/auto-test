#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//05 MGT//02 转账
用例标题
    结算中-系统爆仓账户    
前置条件
    
步骤/文本
    1、打开MGT后台管理系统
    2、点击财务-财务工具-平账，流水类型选择（系统爆仓账户），平种标识如（XRP），输入金额，备注
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

from common.ContractMGTServiceAPI import t as contract_mgt_api
from common.mysqlComm import *


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('MGT')  # 这里填功能
@allure.story('平账')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 程卓')
@pytest.mark.unstable
class TestContractMGTtransfer_045:

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.title('结算中-系统爆仓账户')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('打开MGT后台管理系统点击财务-财务工具-平账，流水类型选择（系统爆仓账户），平种标识如（XRP），输入金额'):
            params = ["XRP",
                      {
                          "productId": "XRP",
                          "flatAccount": 2,
                          "uid": None,
                          "money": "1",
                          "remark": "00"
                      }
                      ]
            form_params = "params={}".format(
                str(params)).replace('None', 'null')
            result = contract_mgt_api.accountActionService_save(
                form_params)
            print(result)
        with allure.step('点击转账记录，查看转账单子是否成功'):
            assert result["errorCode"] == 0 and result["data"]["errorMsg"] == "添加平账流水失败，原因：此合约在非交易状态中, 无法进行系统划转"
        record_id = 0
        with allure.step('点击转账记录，查看转账单子是否成功'):
            contract_btc_conn = mysqlComm()
            symbol = 'XRP'
            sqlStr = f'select id from t_flat_money_record where product_id="{symbol}" ' \
                     f'AND flat_status=2 order by id desc limit 1'
            rec_dict_tuples = contract_btc_conn.selectdb_execute(
                'XRP', sqlStr)
            assert rec_dict_tuples != None
            if(len(rec_dict_tuples) > 0):
                record_id = rec_dict_tuples[0]["id"]
                assert record_id > 0

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
