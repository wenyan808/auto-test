#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/7 2:35 下午
# @Author  : HuiQing Yu

import json
import time
from decimal import Decimal

import allure
import pytest

from common.SwapServiceMGT import SwapServiceMGT
from common.mysqlComm import mysqlComm
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL


@allure.epic(epic[1])
@allure.feature(features[4]['feature'])
@allure.story(features[4]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 程卓')
@pytest.mark.stable
class TestSwapAccountCapticalBatch_405:
    ids = ['TestSwapAccountCapticalBatch_405']
    params = [{'title':'TestSwapAccountCapticalBatch_405','case_name': '平台流水表-结算对账-互换账户', 'userType': 5, 'userId': '1389608'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.mysqlClient = mysqlComm()
            cls.fund_flow_type = {
                "moneyIn": "从币币转入",
                "moneyOut": "转出至币币",
                "borrowToOperate": "借贷转运营",
                "operateToBorrow": "运营转借贷",
                "toBurst": "注入到爆仓",
                "fromBurst": "从爆仓提取",
                "compensate": "给用户赠币(赔偿)",
                "discipline": "扣减用户资产(惩戒)",
                "feeToOperate": "手续费转运营",
                "actionReward": "活动奖励",
                "dividend": "返利",
                "openFeeMaker": "开仓手续费挂单",
                "openFeeTaker": "开仓手续费吃单",
                "closeFeeMaker": "平仓手续费挂单",
                "closeFeeTaker": "平仓手续费吃单",
                "deliveFee": "交割手续费",
                "capitalFeeIn": "资金费-收入",
                "capitalFeeOut": "资金费-支出",
                "capitalFeeToOperate": "资金费转运营",
                "operateToCapitalFee": "运营转资金费",
                "flatMoney": "平账",
                "currInterest": "当期流水",
                "originalInterest": "实际 期初静态权益",
                "finalInterest": "流水 期未静态权益",
                "staticInterest": "实际 期未静态权益"
            }
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    def __dbResult(self,money_type,userId,dbName):
        sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                 f'WHERE create_time > "{self.beginDateTime}" ' \
                 f'and create_time<= "{self.endDateTime}" ' \
                 f'AND money_type =  {money_type} ' \
                 f'AND product_id = "{self.symbol}" ' \
                 f'AND user_id = "{userId}" '
        money = self.mysqlClient.selectdb_execute(dbSchema=dbName,sqlStr=sqlStr)
        if len(money) == 0 or money[0]['money'] is None:
            money = 0
        else:
            money = money[0]['money']
        return money

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param):
        allure.dynamic.title(param['title'])
        with allure.step('操作：执行查询'):
            sqlStr = 'SELECT end_time,id ' \
                     'FROM t_settle_log t ' \
                     'where progress_code=13 ' \
                     f'and product_id= "{self.symbol}" ' \
                     'order by end_time desc limit 2 '
            db_info = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            self.endDateTime = db_info[0]['end_time']
            self.beginDateTime = db_info[1]['end_time']
            request_params = [
                self.symbol,
                2,
                {
                    "productId": self.symbol,
                    "type": 2,
                    "endDateTime": self.endDateTime,
                    "beginDateTime": self.beginDateTime,
                    # "endDailyDateTime": "2021/12/13",
                    # "beginDailyDateTime": "2021/12/12",
                    # "date": 19,
                    "originSettleId": db_info[1]['id'],
                    "finalSettleId": db_info[0]['id'],
                    "reOpen": False,
                    "originTime": self.beginDateTime,
                    "finalTime": self.endDateTime
                }
            ]
            result = SwapServiceMGT.findPaltformFlow(params=request_params)
            # '用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9运营活动，11是平台资产 12是应付用户 13是平账账户',
            self.daily = json.loads(result['data'])
            pass
        with allure.step('操作:从接口返回中取出-互换账户-数据'):
            pay_money = None
            for data in self.daily['daily']:
                if data['userType'] == param['userType']:
                    pay_money = data
                    break
            assert pay_money, '返回数据中未找到-互换账户-数据，校验失败'
#################################################  【互换账户】交割手续费	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["deliveFee"]}-数据'):
            deliveFee = self.__dbResult(money_type=11,userId=param['userId'],dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["deliveFee"]}'):
            assert Decimal(pay_money['deliveFee']) == deliveFee, f'{self.fund_flow_type["deliveFee"]}-校验失败'
#################################################  【互换账户】资金费-收入	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["capitalFeeIn"]}-数据'):
            capitalFeeIn = - self.__dbResult(money_type=30,userId=param['userId'],dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["capitalFeeIn"]}'):
            assert Decimal(pay_money['capitalFeeIn']) == capitalFeeIn, f'{self.fund_flow_type["capitalFeeIn"]}-校验失败'
#################################################  【互换账户】资金费-支出	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["capitalFeeOut"]}-数据'):
            capitalFeeOut = - self.__dbResult(money_type=31,userId=param['userId'],dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["capitalFeeOut"]}'):
            assert Decimal(pay_money['capitalFeeOut']) == capitalFeeOut, f'{self.fund_flow_type["capitalFeeOut"]}-校验失败'
#################################################  【互换账户】资金费转运营	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["capitalFeeToOperate"]}-数据'):
            capitalFeeToOperate = self.__dbResult(money_type=32,userId=param['userId'],dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["capitalFeeToOperate"]}'):
            assert Decimal(pay_money['capitalFeeToOperate']) == capitalFeeToOperate, f'{self.fund_flow_type["capitalFeeToOperate"]}-校验失败'
#################################################  【互换账户】运营转资金费	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["operateToCapitalFee"]}-数据'):
            operateToCapitalFee = self.__dbResult(money_type=33,userId=param['userId'],dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["operateToCapitalFee"]}'):
            assert Decimal(pay_money['operateToCapitalFee']) == operateToCapitalFee, \
                f'{self.fund_flow_type["operateToCapitalFee"]}-校验失败'
#################################################  【互换账户】平账	####################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["flatMoney"]}-数据'):
            flatMoney = self.__dbResult(money_type=20,userId=param['userId'],dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["flatMoney"]}'):
            assert Decimal(pay_money['flatMoney']) == flatMoney, f'{self.fund_flow_type["flatMoney"]}-校验失败'
#################################################  【互换账户】当期流水	####################################################
        with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
            sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                     f'WHERE create_time > "{self.beginDateTime}" ' \
                     f'and create_time<= "{self.endDateTime}" ' \
                     f'AND money_type in (11,20,30,31,32,33) ' \
                     f'AND product_id = "{self.symbol}" ' \
                     f'AND user_id = {param["userId"]} '
            currInterest = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            if len(currInterest) == 0 or currInterest[0]['money'] is None:
                currInterest = 0
            else:
                currInterest = currInterest[0]['money']
        with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
            assert Decimal(pay_money['currInterest']) == currInterest, \
                f'{self.fund_flow_type["currInterest"]}-校验失败'
#################################################    【互换账户】实际 期初静态权益    #######################################
        with allure.step(f'验证:流水类型-{self.fund_flow_type["originalInterest"]}'):
            timeArray = time.localtime(int(self.beginDateTime) / 1000)
            settle_date = time.strftime("%Y%m%d", timeArray)
            sqlStr = 'SELECT TRUNCATE(sum(static_interest), 8) as money ' \
                     'FROM t_account_capital_his ' \
                     f'WHERE settle_date= "{settle_date}" ' \
                     'AND settle_id=1 ' \
                     f'AND product_id ="{self.symbol}" ' \
                     f'AND user_id={param["userId"]} '
            originalInterest = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            if len(originalInterest) == 0 or originalInterest[0]['money'] is None:
                originalInterest = 0
            else:
                originalInterest = originalInterest[0]['money']

            assert Decimal(pay_money['originalInterest']) == originalInterest, \
                f'{self.fund_flow_type["originalInterest"]}-校验失败'
#################################################    【互换账户】流水 期未静态权益    #######################################
        with allure.step(f'验证:流水类型-{self.fund_flow_type["finalInterest"]}'):
            sqlStr = 'select TRUNCATE(sum(money),8) as money from ( ' \
                     'SELECT sum(money) as money FROM t_account_action ' \
                     f'WHERE create_time > "{self.beginDateTime}" ' \
                     f'and create_time<= "{self.endDateTime}" ' \
                     f'AND money_type in (11,20,30,31,32,33) ' \
                     f'AND product_id = "{self.symbol}" ' \
                     f'AND user_id = {param["userId"]} '\
                     'union  ' \
                     'SELECT sum(static_interest) as money ' \
                     'FROM t_account_capital_his ' \
                     f'WHERE settle_date= "{settle_date}" ' \
                     'AND settle_id=1 ' \
                     f'AND product_id ="{self.symbol}" ' \
                     f'AND user_id={param["userId"]} ) a'
            finalInterest = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            if len(finalInterest) == 0 or finalInterest[0]['money'] is None:
                finalInterest = 0
            else:
                finalInterest = finalInterest[0]['money']
            assert Decimal(pay_money['finalInterest']) == finalInterest, \
                f'{self.fund_flow_type["finalInterest"]}-校验失败'
#################################################    【互换账户】实际 期未静态权益    #######################################
        with allure.step(f'验证:流水类型-{self.fund_flow_type["finalInterest"]}'):
            staticInterest_money = None
            for data in self.daily['originalcapital']:
                if data['userType'] == param['userType']:
                    staticInterest_money = data
                    break
            assert staticInterest_money, '返回数据中未找到-互换账户-数据，校验失败'
            sqlStr = 'SELECT sum(static_interest) as money ' \
                     'FROM t_account_capital_his ' \
                     f'WHERE settle_date= "{staticInterest_money["settleDate"]}" ' \
                     'AND settle_id=1 ' \
                     f'AND product_id ="{self.symbol}" ' \
                     f'AND user_id={param["userId"]}'
            staticInterest = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            if len(staticInterest) == 0 or staticInterest[0]['money'] is None:
                staticInterest = 0
            else:
                staticInterest = staticInterest[0]['money']
            assert Decimal(staticInterest_money['staticInterest']) == staticInterest, \
                f'{self.fund_flow_type["staticInterest"]}-校验失败'
#################################################    【平台资产】核对结果    ###############################################
            with allure.step(f'验证:核对结果 == 0'):
                accountCapitalCheck = None
                for data in self.daily['accountCapitalCheck']:
                    if data['userType'] == param['userType']:
                        accountCapitalCheck = data
                        break
                assert accountCapitalCheck, '返回数据中未找到-应付用户-数据，校验失败'
                assert Decimal(accountCapitalCheck['checkResult']) == 0, '核对结果不为0'