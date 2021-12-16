#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/7 2:35 下午
# @Author  : HuiQing Yu

import json
from datetime import date, timedelta
from decimal import Decimal
import random
import allure
import pytest

from common.SwapServiceMGT import SwapServiceMGT
from common.mysqlComm import mysqlComm
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[4]['feature'])
@allure.story(features[4]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 程卓')
@pytest.mark.stable
class TestSwapAccountCapticalBatch_204:
    ids = ['TestSwapAccountCapticalBatch_204']
    params = [{'title':'TestSwapAccountCapticalBatch_204','case_name': '平台流水表-单日0-24流水-交易手续费', 'userType': 4, 'type':3,'userId': '1389607'}]
    DB_contract_trade = mysqlComm('contract_trade')
    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
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
                "currInterest": "当期流水"
            }
            cls.endDateTime = (date.today() + timedelta(days=-1)).strftime("%Y/%m/%d")
            cls.beginDateTime = (date.today() + timedelta(days=-8)).strftime("%Y/%m/%d")
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param, DB_btc):
        allure.dynamic.title(param['title'])
        with allure.step('操作：执行查询'):
            request_params = [
                self.symbol,
                param['type'],
                {
                    "productId": self.symbol,
                    "type": param['type'],
                    "endDateTime": self.endDateTime,
                    "beginDateTime": self.beginDateTime,
                    "endDailyDateTime": self.endDateTime,
                    "beginDailyDateTime": self.beginDateTime
                }
            ]
            result = SwapServiceMGT.findPaltformFlow(params=request_params)
            # '用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9运营活动，11是平台资产 12是应付用户 13是平账账户',
            self.daily = json.loads(result['data'])
            pass
        with allure.step('操作:从接口返回中取出-交易手续费-数据'):
            pay_money = None
            for data in self.daily['daily']:
                if data['userType'] == param['userType']:
                    pay_money = data
                    break
            assert pay_money, '返回数据中未找到-交易手续费-数据，校验失败'
#################################################  【交易手续费】手续费转运营	############################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["feeToOperate"]}-数据'):
            feeToOperate = self.__dbResult(money_type=23,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["feeToOperate"]}'):
            assert Decimal(pay_money['feeToOperate']) == feeToOperate, f'{self.fund_flow_type["feeToOperate"]}-校验失败'
#################################################  【交易手续费】开仓手续费挂单	############################################
        # 交易手术续中的 手术费是应付用户中的手术费取反
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["openFeeMaker"]}-数据'):
            sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                     f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                     f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                     f'AND money_type =  6 ' \
                     f'AND product_id = "{self.symbol}" ' \
                     f'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) '
            money = DB_btc.dictCursor(sqlStr)
            if len(money) == 0 or money[0]['money'] is None:
                money = 0
            else:
                money = money[0]['money']
            openFeeMaker = - money
        with allure.step(f'验证:流水类型-{self.fund_flow_type["openFeeMaker"]}'):
            assert Decimal(pay_money['openFeeMaker']) == openFeeMaker, f'{self.fund_flow_type["openFeeMaker"]}-校验失败'
#################################################  【交易手续费】开仓手续费吃单	############################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["openFeeTaker"]}-数据'):
            # 交易手术续中的 手术费是应付用户中的手术费取反
            with allure.step(f'操作:从DB获取-{self.fund_flow_type["openFeeMaker"]}-数据'):
                sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                         f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                         f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                         f'AND money_type =  5 ' \
                         f'AND product_id = "{self.symbol}" ' \
                         f'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) '
                money = DB_btc.dictCursor(sqlStr)
                if len(money) == 0 or money[0]['money'] is None:
                    money = 0
                else:
                    money = money[0]['money']
                openFeeTaker = - money
        with allure.step(f'验证:流水类型-{self.fund_flow_type["openFeeTaker"]}'):
            assert Decimal(pay_money['openFeeTaker']) == openFeeTaker, f'{self.fund_flow_type["openFeeTaker"]}-校验失败'
#################################################  【交易手续费】平仓手续费挂单	############################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["closeFeeMaker"]}-数据'):
            # 交易手术续中的 手术费是应付用户中的手术费取反
            with allure.step(f'操作:从DB获取-{self.fund_flow_type["openFeeMaker"]}-数据'):
                sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                         f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                         f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                         f'AND money_type =  8 ' \
                         f'AND product_id = "{self.symbol}" ' \
                         f'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) '
                money = DB_btc.dictCursor(sqlStr)
                if len(money) == 0 or money[0]['money'] is None:
                    money = 0
                else:
                    money = money[0]['money']
                closeFeeMaker = - money
        with allure.step(f'验证:流水类型-{self.fund_flow_type["closeFeeMaker"]}'):
            assert Decimal(pay_money['closeFeeMaker']) == closeFeeMaker, f'{self.fund_flow_type["closeFeeMaker"]}-校验失败'
#################################################  【交易手续费】平仓手续费吃单	############################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["closeFeeTaker"]}-数据'):
            # 交易手术续中的 手术费是应付用户中的手术费取反
            with allure.step(f'操作:从DB获取-{self.fund_flow_type["openFeeMaker"]}-数据'):
                sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                         f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                         f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                         f'AND money_type =  7 ' \
                         f'AND product_id = "{self.symbol}" ' \
                         f'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) '
                money = DB_btc.dictCursor(sqlStr)
                if len(money) == 0 or money[0]['money'] is None:
                    money = 0
                else:
                    money = money[0]['money']
                closeFeeTaker = - money
        with allure.step(f'验证:流水类型-{self.fund_flow_type["closeFeeTaker"]}'):
            assert Decimal(pay_money['closeFeeTaker']) == closeFeeTaker, f'{self.fund_flow_type["closeFeeTaker"]}-校验失败'
#################################################  【交易手续费】平账	####################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["flatMoney"]}-数据'):
            flatMoney = self.__dbResult(money_type=20,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["flatMoney"]}'):
            assert Decimal(pay_money['flatMoney']) == flatMoney, f'{self.fund_flow_type["flatMoney"]}-校验失败'
#################################################  【交易手续费】当期流水	################################################
        with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
            sqlStr = 'select sum(money) as money from ( ' \
                     'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                     f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                     f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                     f'AND money_type in (20,23) ' \
                     f'AND product_id = "{self.symbol}" ' \
                     f'AND user_id = {param["userId"]} ' \
                     f'union ' \
                     'SELECT TRUNCATE(-sum(money),8) as money FROM t_account_action ' \
                     f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                     f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                     f'AND money_type in (5,6,7,8) ' \
                     f'AND product_id = "{self.symbol}" ' \
                     f'AND user_id  not in (11186266, 1389607, 1389608, 1389609, 1389766) ) a '
            currInterest = DB_btc.dictCursor(sqlStr)
            if len(currInterest) == 0 or currInterest[0]['money'] is None:
                currInterest = 0
            else:
                currInterest = currInterest[0]['money']
        with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
            assert Decimal(pay_money['currInterest']) == currInterest, \
                f'{self.fund_flow_type["currInterest"]}-校验失败'

    def __dbResult(self,money_type,userId,dbName):
        sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                 f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                 f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                 f'AND money_type =  {money_type} ' \
                 f'AND product_id = "{self.symbol}" ' \
                 f'AND user_id = "{userId}" '
        money = dbName.dictCursor(sqlStr)
        if len(money) == 0 or money[0]['money'] is None:
            money = 0
        else:
            money = money[0]['money']
        return money