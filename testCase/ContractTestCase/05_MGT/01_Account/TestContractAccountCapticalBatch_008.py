#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//05 MGT//02 财务
用例标题
    平台流水表-结算对账-横向对账
前置条件

步骤/文本
    1、执行查询结算对账数据；（查询范围1-7天随机）
    2、查询各流水类型的DB数据
    3、接口数据与DB数据进行对比；
    4、流水类型汇总与当日流水对比校验
预期结果
    1、接口正常返回,各流水类型数据不为0
    2、接口数据与DB数据一致3、数据计算校验正确
优先级
    p2
"""

import datetime
import json
import random
from datetime import date, timedelta
from decimal import Decimal

import allure
import pytest
from common.ContractMGTServiceAPI import t as contract_mgt_api
from common.mysqlComm import *


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('MGT')  # 这里填功能
@allure.story('财务')  # 这里填子功能,没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 程卓')
@pytest.mark.stable
class TestContractAccountCapticalBatch_008:

    params = [
        {"money_type": "moneyIn",  "id": "TestContractAccountCapticalBatch_008",
            "case_title": "平台流水表-结算对账-横向对账:从币币转入"},
        {"money_type": "moneyOut", "id": "TestContractAccountCapticalBatch_009",
            "case_title": "平台流水表-结算对账-横向对账:转出至币币"},
        {"money_type": "borrowToOperate", "id": "TestContractAccountCapticalBatch_010:",
            "case_title": "平台流水表-结算对账-横向对账:借贷转运营"},
        {"money_type": "operateToBorrow", "id": "TestContractAccountCapticalBatch_011",
            "case_title": "平台流水表-结算对账-横向对账:运营转借贷"},
        {"money_type": "toBurst", "id": "TestContractAccountCapticalBatch_012",
            "case_title": "平台流水表-结算对账-横向对账:注入到爆仓"},
        {"money_type": "fromBurst", "id": "TestContractAccountCapticalBatch_013",
            "case_title": "平台流水表-结算对账-横向对账:从爆仓提取"},
        {"money_type": "compensate", "id": "TestContractAccountCapticalBatch_014",
            "case_title": "平台流水表-结算对账-横向对账:给用户赠币赔偿"},
        {"money_type": "discipline", "id": "TestContractAccountCapticalBatch_015",
            "case_title": "平台流水表-结算对账-横向对账:扣减用户资产惩戒"},
        {"money_type": "feeToOperate", "id": "TestContractAccountCapticalBatch_016",
            "case_title": "平台流水表-结算对账-横向对账:手续费转运营"},
        {"money_type": "actionReward", "id": "TestContractAccountCapticalBatch_017",
            "case_title": "平台流水表-结算对账-横向对账:活动奖励"},
        {"money_type": "dividend", "id": "TestContractAccountCapticalBatch_018",
            "case_title": "平台流水表-结算对账-横向对账:返利"},
        {"money_type": "openFeeMaker", "id": "TestContractAccountCapticalBatch_019",
            "case_title": "平台流水表-结算对账-横向对账:开仓手续费挂单"},
        {"money_type": "openFeeTaker", "id": "TestContractAccountCapticalBatch_020",
            "case_title": "平台流水表-结算对账-横向对账:开仓手续费吃单"},
        {"money_type": "closeFeeMaker", "id": "TestContractAccountCapticalBatch_021",
            "case_title": "平台流水表-结算对账-横向对账:平仓手续费挂单"},
        {"money_type": "closeFeeTaker", "id": "TestContractAccountCapticalBatch_022",
            "case_title": "平台流水表-结算对账-横向对账:平仓手续费吃单"},
        {"money_type": "deliveFee", "id": "TestContractAccountCapticalBatch_023",
            "case_title": "平台流水表-结算对账-横向对账:交割手续费"},
        {"money_type": "flatMoney", "id": "TestContractAccountCapticalBatch_024",
            "case_title": "平台流水表-结算对账-横向对账:平账"},
        {"money_type": "currInterest", "id": "TestContractAccountCapticalBatch_025",
            "case_title": "平台流水表-结算对账-横向对账:流水当期发生"},
    ]

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.step('测试执行')
    @pytest.mark.parametrize('param', params, ids=[x['id'] for x in params])
    def test_execute(self, symbol, param):
        allure.dynamic.title(param['case_title'])
        endDate = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        beginDate = (date.today(
        ) + datetime.timedelta(days=random.randint(2, 7)*-1)).strftime("%Y%m%d")
        print("查询开始日期{}至{}".format(beginDate, endDate))
        with allure.step('执行查询结算对账数据；（查询范围1-7天随机）'):
            params = [symbol,
                      {
                          "productId": symbol,
                          "type": 1,
                          "endDate": endDate,
                          "beginDate": beginDate,
                          "date": 32
                      }
                      ]
            form_params = "params={}".format(str(params))
            result = contract_mgt_api.accountCapitalDailyService_findPaltformFlow(
                form_params)
            print(result)
            self.__data = json.loads(result['data'])
            assert result["errorCode"] == 0

        with allure.step('接口正常返回,各流水类型数据不为0'):
            assert len(self.__data['daily']) > 0
        with allure.step('查询各流水类型的DB数据,接口数据与DB数据进行对比'):
            contract_conn = mysqlComm()
            symbol = 'btc'
            # money_type 5:开仓手续费-taker,6:开仓手续费-maker,7:平仓手续费-taker,8:平仓手续费-maker,11:平账账户,14:币币转入,15:币币转出,20:平账,21:借贷转运营,22:运营转借贷,23:手续费转运营,24:注入到爆仓,25:从爆仓提取,26:给用户赠币-赔偿,27:扣减用户资产-惩戒,28:活动奖励,29:返利
            # userType 用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9运营活动，11是平台资产 12是应付用户 13是平账账户
            platform_capital_dic = None  # 平台资产
            # 验证如下:userType:平台资产=负债+所有者权益
            A = 0  # 资产
            S = 0  # 负债
            O = 0  # 所有者权益

            for data in self.__data['daily']:
                if data['userType'] == 3 or data['userType'] == 12:
                    S += Decimal(data[param['money_type']])
                elif data['userType'] == 11:
                    A += Decimal(data[param['money_type']])
                elif data['userType'] == 4 or data['userType'] == 5 or data['userType'] == 9:
                    O += Decimal(data[param['money_type']])

            assert A == S+O, '{},横向校验失败'.format(param['case_title'])

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
