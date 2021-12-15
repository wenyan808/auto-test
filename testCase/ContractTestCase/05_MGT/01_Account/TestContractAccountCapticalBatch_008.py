#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//05 MGT//02 转账
用例标题
    平台流水表-每日跑批:校验平账账户
前置条件

步骤/文本
    1、执行查询每日跑批数据；（查询范围1-7天随机）
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
@allure.story('转账')  # 这里填子功能,没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 程卓')
@pytest.mark.stable
class TestContractAccountCapticalBatch_007:

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.title('平台流水表-每日跑批:校验平账账户')
    @allure.step('测试执行')
    def test_execute(self):
        symbol = "BTC"
        endDateTime = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        beginDateTime = (date.today(
        ) + datetime.timedelta(days=random.randint(2, 7)*-1)).strftime("%Y%m%d")
        print("查询开始日期{}至{}".format(beginDateTime, endDateTime))
        with allure.step('执行查询每日跑批数据；（查询范围1-7天随机）'):
            params = [symbol,
                      {
                          "productId": symbol,
                          "type": 1,
                          "endDate": endDateTime,
                          "beginDate": beginDateTime,
                          "date": 32
                      }
                      ]
            form_params = "params={}".format(str(params))
            result = contract_mgt_api.accountCapitalDailyService_findPaltformFlow(
                form_params)
            print(result)
            self.__daily = json.loads(result['data'])
            assert result["errorCode"] == 0

        with allure.step('接口正常返回,各流水类型数据不为0'):
            assert len(self.__daily['daily']) > 0
        with allure.step('查询各流水类型的DB数据,接口数据与DB数据进行对比'):
            contract_conn = mysqlComm(biztype='contract')
            symbol = 'btc'
            # money_type 5:开仓手续费-taker,6:开仓手续费-maker,7:平仓手续费-taker,8:平仓手续费-maker,11:平账账户,14:币币转入,15:币币转出,20:平账,21:借贷转运营,22:运营转借贷,23:手续费转运营,24:注入到爆仓,25:从爆仓提取,26:给用户赠币-赔偿,27:扣减用户资产-惩戒,28:活动奖励,29:返利
            # userType 用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9平账账户，11是平台资产 12是应付用户 13是平账账户
            platform_capital_dic = None  # 平台资产
            for data in self.__daily['daily']:
                if data['userType'] == 13:
                    platform_capital_dic = data
                    break
            assert platform_capital_dic, '返回数据中未找到-平台资产,校验失败'
            # 平账账户验证如下:money_type:借贷转运营(21),运营转借贷(22),注入到爆仓（24）,从爆仓提取（25）,给用户赠币-赔偿（26）,扣减用户资产-惩戒（27）,手续费转运营(23),活动奖励（28）,返利（29）,平账（20）
            capital_param_dic = {
                "flatMoney": 20,
            }
            currInterest = 0  # 流水当期发生
            # 获取时间戳
            beginSqlStr = 'SELECT MAX(flow_end_time) as unixtime FROM t_daily_log t  where product_id="{}" AND batch_date ={} ORDER BY flow_end_time desc'.format(
                symbol, beginDateTime)
            rec_begin_dict = contract_conn.contract_selectdb_execute(
                "contract_trade", beginSqlStr)
            beginDateUnixTime = rec_begin_dict[0]["unixtime"]
            endSqlStr = 'SELECT MAX(flow_end_time) as unixtime FROM t_daily_log t  where product_id="{}" AND batch_date ={} ORDER BY flow_end_time desc'.format(
                symbol, endDateTime)
            rec_end_dict = contract_conn.contract_selectdb_execute(
                "contract_trade", endSqlStr)
            endDateUnixTime = rec_end_dict[0]["unixtime"]

            for key, value in capital_param_dic.items():
                sqlStr = 'SELECT SUM(money) as money FROM t_account_action WHERE create_time > {} AND create_time <= {} AND money_type = {} AND product_id = "{}" AND user_id=193798'.format(
                    beginDateUnixTime, endDateUnixTime, value, symbol)
                print(sqlStr)
                rec_dict_tuples = contract_conn.contract_selectdb_execute(
                    db='btc', sqlStr=sqlStr)
                money = 0.000000000000000000
                if rec_dict_tuples[0]["money"]:
                    currInterest += rec_dict_tuples[0]["money"]
                    money = rec_dict_tuples[0]["money"]
                assert money == Decimal(platform_capital_dic[key]), "{} 流水比对异常".format(
                    key)

            # 流水当期发生额比较
            assert currInterest == Decimal(
                platform_capital_dic["currInterest"]), '流水当期发生额不正确'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
