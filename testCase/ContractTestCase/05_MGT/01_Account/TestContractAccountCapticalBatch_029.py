#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//05 MGT//02 财务
用例标题
    平台流水表-结算对账:校验交易手续费
前置条件

步骤/文本
    1、执行查询结算对账数据
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
class TestContractAccountCapticalBatch_029:

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.title('平台流水表-结算对账:校验交易手续费')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        # userType 用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9运营活动，11是平台资产 12是应付用户 13是平账账户
        userType = 4
        # 构造请求参数
        contract_conn = mysqlComm()
        sqlStr = 'SELECT id,settle_date,end_time FROM t_settle_log WHERE progress_code=13 AND product_id= "{}" ORDER BY id DESC LIMIT 2 '.format(
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

        with allure.step('查询各流水类型的DB数据,接口数据与DB数据进行对比'):
            symbol = 'btc'
            # money_type 5:开仓手续费-taker,6:开仓手续费-maker,7:平仓手续费-taker,8:平仓手续费-maker,11:交割手续费,14:币币转入,15:币币转出,20:平账,21:借贷转运营,22:运营转借贷,23:手续费转运营,24:注入到爆仓,25:从爆仓提取,26:给用户赠币-赔偿,27:扣减用户资产-惩戒,28:活动奖励,29:返利
            platform_capital_dic = None  # 平台资产
            for data in self.__data['daily']:
                if data['userType'] == userType:
                    platform_capital_dic = data
                    break
            assert platform_capital_dic, '返回数据中未找到-平台资产,校验失败'
            # 应付外债验证如下:money_type:币币转入（14）,币币转出（15）,借贷转运营(21),运营转借贷(22),平账（20）
            capital_param_dic = {"feeToOperate": 23,
                                 "openFeeMaker": 6,
                                 "openFeeTaker": 5,
                                 "closeFeeMaker": 8,
                                 "closeFeeTaker": 7,
                                 "flatMoney": 20,
                                 }
            currInterest = 0  # 流水当期发生

            for key, value in capital_param_dic.items():
                sqlStr = 'SELECT SUM(money) as money FROM t_account_action WHERE create_time > {} AND create_time <= {} AND money_type = {} AND product_id = "{}" AND user_id=193799'.format(
                    beginDateTime, endDateTime, value, symbol)
                print(sqlStr)
                rec_dict_tuples = contract_conn.selectdb_execute(
                    dbSchema='btc', sqlStr=sqlStr)
                money = 0.0
                if rec_dict_tuples[0]["money"]:
                    currInterest += rec_dict_tuples[0]["money"]
                    money = rec_dict_tuples[0]["money"]
                assert money == Decimal(
                    platform_capital_dic[key]), "{} 流水比对异常".format(key)
            # 实际期初静态权益,original_interest(期初),static_interest(期未)
            sqlStr = 'SELECT original_interest,static_interest FROM t_account_capital_his WHERE settle_date="{}" AND product_id="{}" AND user_type={}'.format(
                beginDate, symbol, userType
            )
            print(sqlStr)
            rec_dict_tuples = contract_conn.selectdb_execute(
                dbSchema='btc', sqlStr=sqlStr)
            # 前一个期未当本期的期初
            begin_static_interest = rec_dict_tuples[0]["static_interest"]

            originalcapital_dic = None
            for data in self.__data['originalcapital']:
                if data['userType'] == userType:
                    originalcapital_dic = data
                    break
            assert platform_capital_dic, '返回数据中未找到-平台资产,校验失败'
            assert begin_static_interest == Decimal(
                originalcapital_dic["staticInterest"])
            # 流水期末静态权益
            curr_static_interest = begin_static_interest+currInterest

            # 实际期末静态权益
            sqlStr = 'SELECT original_interest,static_interest FROM t_account_capital_his WHERE settle_date="{}" AND product_id="{}" AND user_type={}'.format(
                endDate, symbol, userType
            )
            rec_dict_tuples = contract_conn.selectdb_execute(
                dbSchema='btc', sqlStr=sqlStr)
            end_original_interest = rec_dict_tuples[0]["original_interest"]
            end_static_interest = rec_dict_tuples[0]["static_interest"]
            assert end_original_interest == begin_static_interest

            finalcapital_dic = None
            for data in self.__data['finalcapital']:
                if data['userType'] == userType:
                    finalcapital_dic = data
                    break
            assert finalcapital_dic, '返回数据中未找到-平台资产,校验失败'
            assert end_static_interest == Decimal(
                finalcapital_dic["staticInterest"])

            # 核对
            assert end_static_interest == curr_static_interest

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
