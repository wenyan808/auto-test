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
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[4]['feature'])
@allure.story(features[4]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : 程卓')
@pytest.mark.stable
class TestSwapAccountCapticalBatch_005:
    ids = ['TestSwapAccountCapticalBatch_005','TestSwapAccountCapticalBatch_205']
    params = [{'case_name': '平台流水表-每日跑批-互换账户', 'userType': 5, 'userId': '1389608','type': 1},
              {'case_name': '平台流水表-单日0-24-互换账户', 'userType': 5, 'userId': '1389608','type': 3}]
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
            pass


    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    def __dbResult(self,money_type,userId,dbName):
        sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                 f'WHERE create_time > UNIX_TIMESTAMP("{self.daily["beginDateTime"]}")*1000 ' \
                 f'and create_time<=UNIX_TIMESTAMP("{self.daily["endDateTime"]}")*1000 ' \
                 f'AND money_type =  {money_type} ' \
                 f'AND product_id = "{self.symbol}" ' \
                 f'AND user_id = "{userId}" '
        money = dbName.dictCursor(sqlStr)
        if len(money) == 0 or money[0]['money'] is None:
            money = 0
        else:
            money = money[0]['money']
        return money

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param, DB_btc):
        allure.dynamic.title(param['case_name'])
        with allure.step('操作：执行查询'):
            endDateTime = (date.today() + timedelta(days=-1)).strftime("%Y/%m/%d")
            beginDateTime = (date.today() + timedelta(days=-random.randint(2,7))).strftime("%Y/%m/%d")
            request_params = [
                self.symbol,
                param['type'],
                {
                    "productId": self.symbol,
                    "type": param['type'],
                    "endDateTime": endDateTime,
                    "beginDateTime": beginDateTime,
                    "endDailyDateTime": endDateTime,
                    "beginDailyDateTime": beginDateTime
                }
            ]
            result = SwapServiceMGT.findPaltformFlow(params=request_params)
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
            deliveFee = self.__dbResult(money_type=11,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["deliveFee"]}'):
            assert Decimal(pay_money['deliveFee']) == deliveFee, f'{self.fund_flow_type["deliveFee"]}-校验失败'
#################################################  【互换账户】资金费-收入	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["capitalFeeIn"]}-数据'):
            capitalFeeIn = - self.__dbResult(money_type=30,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["capitalFeeIn"]}'):
            assert Decimal(pay_money['capitalFeeIn']) == capitalFeeIn, f'{self.fund_flow_type["capitalFeeIn"]}-校验失败'
#################################################  【互换账户】资金费-支出	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["capitalFeeOut"]}-数据'):
            capitalFeeOut = - self.__dbResult(money_type=31,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["capitalFeeOut"]}'):
            assert Decimal(pay_money['capitalFeeOut']) == capitalFeeOut, f'{self.fund_flow_type["capitalFeeOut"]}-校验失败'
#################################################  【互换账户】资金费转运营	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["capitalFeeToOperate"]}-数据'):
            capitalFeeToOperate = self.__dbResult(money_type=32,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["capitalFeeToOperate"]}'):
            assert Decimal(pay_money['capitalFeeToOperate']) == capitalFeeToOperate, f'{self.fund_flow_type["capitalFeeToOperate"]}-校验失败'
#################################################  【互换账户】运营转资金费	################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["operateToCapitalFee"]}-数据'):
            operateToCapitalFee = self.__dbResult(money_type=33,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["operateToCapitalFee"]}'):
            assert Decimal(pay_money['operateToCapitalFee']) == operateToCapitalFee, \
                f'{self.fund_flow_type["operateToCapitalFee"]}-校验失败'
#################################################  【互换账户】平账	####################################################
        with allure.step(f'操作:从DB获取-{self.fund_flow_type["flatMoney"]}-数据'):
            flatMoney = self.__dbResult(money_type=20,userId=param['userId'],dbName=DB_btc)
        with allure.step(f'验证:流水类型-{self.fund_flow_type["flatMoney"]}'):
            assert Decimal(pay_money['flatMoney']) == flatMoney, f'{self.fund_flow_type["flatMoney"]}-校验失败'
#################################################  【互换账户】当期流水	####################################################
        with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
            assert Decimal(pay_money['currInterest']) == deliveFee + \
                   capitalFeeIn + \
                   capitalFeeToOperate+ \
                   operateToCapitalFee+\
                   capitalFeeOut + flatMoney, \
                f'{self.fund_flow_type["currInterest"]}-校验失败'