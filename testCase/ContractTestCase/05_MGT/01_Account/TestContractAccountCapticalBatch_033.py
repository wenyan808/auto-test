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
    1、执行查询结算对账数据；
    2、查询各流水类型的DB数据
    3、接口数据与DB数据进行对比；
    4、流水类型汇总与当日流水对比校验
预期结果
    1、接口正常返回,各流水类型数据不为0
    2、接口数据与DB数据一致3、数据计算校验正确
优先级
    p2
"""

import json
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
class TestContractAccountCapticalBatch_033:

    params = [
        {"money_type": "moneyIn",  "case_name": "TestContractAccountCapticalBatch_033",
            "case_title": "平台流水表-结算对账-横向对账:从币币转入"},
        {"money_type": "moneyOut", "case_name": "TestContractAccountCapticalBatch_034",
            "case_title": "平台流水表-结算对账-横向对账:转出至币币"},
        {"money_type": "borrowToOperate", "case_name": "TestContractAccountCapticalBatch_035:",
            "case_title": "平台流水表-结算对账-横向对账:借贷转运营"},
        {"money_type": "operateToBorrow", "case_name": "TestContractAccountCapticalBatch_036",
            "case_title": "平台流水表-结算对账-横向对账:运营转借贷"},
        {"money_type": "toBurst", "case_name": "TestContractAccountCapticalBatch_037",
            "case_title": "平台流水表-结算对账-横向对账:注入到爆仓"},
        {"money_type": "fromBurst", "case_name": "TestContractAccountCapticalBatch_038",
            "case_title": "平台流水表-结算对账-横向对账:从爆仓提取"},
        {"money_type": "compensate", "case_name": "TestContractAccountCapticalBatch_039",
            "case_title": "平台流水表-结算对账-横向对账:给用户赠币赔偿"},
        {"money_type": "discipline", "case_name": "TestContractAccountCapticalBatch_040",
            "case_title": "平台流水表-结算对账-横向对账:扣减用户资产惩戒"},
        {"money_type": "feeToOperate", "case_name": "TestContractAccountCapticalBatch_041",
            "case_title": "平台流水表-结算对账-横向对账:手续费转运营"},
        {"money_type": "actionReward", "case_name": "TestContractAccountCapticalBatch_042",
            "case_title": "平台流水表-结算对账-横向对账:活动奖励"},
        {"money_type": "dividend", "case_name": "TestContractAccountCapticalBatch_043",
            "case_title": "平台流水表-结算对账-横向对账:返利"},
        {"money_type": "openFeeMaker", "case_name": "TestContractAccountCapticalBatch_044",
            "case_title": "平台流水表-结算对账-横向对账:开仓手续费挂单"},
        {"money_type": "openFeeTaker", "case_name": "TestContractAccountCapticalBatch_045",
            "case_title": "平台流水表-结算对账-横向对账:开仓手续费吃单"},
        {"money_type": "closeFeeMaker", "case_name": "TestContractAccountCapticalBatch_046",
            "case_title": "平台流水表-结算对账-横向对账:平仓手续费挂单"},
        {"money_type": "closeFeeTaker", "case_name": "TestContractAccountCapticalBatch_047",
            "case_title": "平台流水表-结算对账-横向对账:平仓手续费吃单"},
        {"money_type": "deliveFee", "case_name": "TestContractAccountCapticalBatch_048",
            "case_title": "平台流水表-结算对账-横向对账:交割手续费"},
        {"money_type": "flatMoney", "case_name": "TestContractAccountCapticalBatch_049",
            "case_title": "平台流水表-结算对账-横向对账:平账"},
        {"money_type": "currInterest", "case_name": "TestContractAccountCapticalBatch_050",
            "case_title": "平台流水表-结算对账-横向对账:流水当期发生"},
    ]

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.step('测试执行')
    @pytest.mark.parametrize('param', params)
    def test_execute(self, symbol, param):
        allure.dynamic.title(param['case_name'])
        # 构造请求参数
        contract_conn = mysqlComm()
        sqlStr = 'SELECT id,settle_date,end_time FROM t_settle_log WHERE progress_code=13 ADN product_id= "{}" ORDER BY id DESC LIMIT 2 '.format(
            symbol)
        rec_dict_tuples = contract_conn.selectdb_execute(
            dbSchema='btc', sqlStr=sqlStr)
        if(len(rec_dict_tuples) != 2):
            pytest.skip(msg="无结算对账记录")
        beginDate = rec_dict_tuples[1]["settle_date"]
        endDate = rec_dict_tuples[0]["settle_date"]
        beginDateTime = rec_dict_tuples[1]["end_time"]
        endDateTime = rec_dict_tuples[0]["end_time"]
        originSettleId = rec_dict_tuples[1]["id"]
        finalSettleId = rec_dict_tuples[0]["id"]
        contract_conn
        with allure.step('执行查询结算对账数据'):
            params = [symbol,
                      {
                          "productId": symbol,
                          "type": 2,
                          "endDate": endDate,
                          "beginDate": beginDate,
                          "date": 33,
                          "beginDateTime": beginDateTime,
                          "endDateTime": endDateTime,
                          "originSettleId": originSettleId,
                          "finalSettleId": finalSettleId,
                          "reOpen": False,
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
        with allure.step('查询接口数据会计恒等式是否成立'):
            symbol = 'btc'
            # money_type 5:开仓手续费-taker,6:开仓手续费-maker,7:平仓手续费-taker,8:平仓手续费-maker,11:平账账户,14:币币转入,15:币币转出,20:平账,21:借贷转运营,22:运营转借贷,23:手续费转运营,24:注入到爆仓,25:从爆仓提取,26:给用户赠币-赔偿,27:扣减用户资产-惩戒,28:活动奖励,29:返利
            # userType 用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9运营活动，11是平台资产 12是应付用户 13是平账账户
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


if __name__ == '__main__':
    pytest.main()
