#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/7 2:35 下午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import json
from datetime import date, timedelta
from decimal import Decimal
import time
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
class TestSwapAccountCapticalBatch_201:

    ids = ['TestSwapAccountCapticalBatch_201']
    params = [{'title':'TestSwapAccountCapticalBatch_201','case_name':'平台流水表-单日0-24流水-平台资产','userType': 11,'type': 3}]


    def __dbResult(self, money_type, dbName):
        sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                 f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                 f'and create_time < unix_timestamp("{self.endDateTime}")*1000 ' \
                 f'AND money_type = {money_type} ' \
                 f'AND product_id = "{self.symbol}" ' \
                 'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) '
        money = mysqlClient.selectdb_execute(dbSchema=dbName,sqlStr=sqlStr)
        if len(money) == 0 or money[0]['money'] is None:
            money = 0
        else:
            money = money[0]['money']
        return money

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

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['title'])
        with allure.step('操作：执行查询'):
            request_params = [
                self.symbol,
                params['type'],
                {
                    "productId": self.symbol,
                    "type": params['type'],
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
        with allure.step('操作:从接口返回中取出-平台资产-数据'):
            platform_money = None
            for data in self.daily['daily']:
                if data['userType'] == 11:
                    platform_money = data
                    break
            assert platform_money,'返回数据中未找到-平台资产，校验失败'
#########################################  【平台资产】从币币转入	########################################################
            with allure.step(f'操作:从DB获取-{self.fund_flow_type["moneyIn"]}-数据'):
                moneyIn = self.__dbResult(money_type=14,dbName='btc')
            with allure.step(f'验证:流水类型-{self.fund_flow_type["moneyIn"]}'):
                assert Decimal(platform_money['moneyIn']) == moneyIn, f'{self.fund_flow_type["moneyIn"]}-校验失败'
#################################################  【平台资产】转出至币币	################################################
            with allure.step(f'操作:从DB获取-{self.fund_flow_type["moneyOut"]}-数据'):
                moneyOut = self.__dbResult(money_type=15,dbName='btc')
            with allure.step(f'验证:流水类型-{self.fund_flow_type["moneyOut"]}'):
                assert Decimal(platform_money['moneyOut']) == moneyOut, f'{self.fund_flow_type["moneyOut"]}-校验失败'
#################################################  【平台资产】平账	####################################################
            with allure.step(f'操作:从DB获取-{self.fund_flow_type["flatMoney"]}-数据'):
                sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_flat_money_record ' \
                         f'WHERE flat_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                         f'and flat_time< UNIX_TIMESTAMP("{self.endDateTime}")*1000   ' \
                         'and flat_account=11 ' \
                         f'and product_id = "{self.symbol}"'
                flatMoney = mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
                if len(flatMoney) == 0 or flatMoney[0]['money'] is None:
                    flatMoney = 0
                else:
                    flatMoney = flatMoney[0]['money']
            with allure.step(f'验证:流水类型-{self.fund_flow_type["flatMoney"]}'):
                assert Decimal(platform_money['flatMoney']) == flatMoney, f'{self.fund_flow_type["flatMoney"]}-校验失败'
#################################################    【平台资产】当期流水    ###############################################
            with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
                # 只有平台资产的平账资金是从t_flat_money_record中获取；其他账户还是在t_account_action中取值
                sqlStr = 'select sum(money) as money from ( ' \
                         'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                         f'WHERE create_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                         f'and create_time < UNIX_TIMESTAMP("{self.endDateTime}")*1000 ' \
                         f'AND money_type in (14,15) ' \
                         f'AND product_id = "{self.symbol}" ' \
                         'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) ' \
                         'union ' \
                         'SELECT TRUNCATE(sum(money), 8) as money ' \
                         'FROM t_flat_money_record ' \
                         f'WHERE flat_time >= UNIX_TIMESTAMP("{self.beginDateTime}")*1000 ' \
                         f'and flat_time< UNIX_TIMESTAMP("{self.endDateTime}")*1000   ' \
                         f'and product_id = "{self.symbol}" and flat_account = 11 ) a'
                currInterest = mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
                if len(currInterest) == 0 or currInterest[0]['money'] is None:
                    currInterest = 0
                else:
                    currInterest = currInterest[0]['money']
            with allure.step(f'验证:流水类型-{self.fund_flow_type["currInterest"]}'):
                assert Decimal(platform_money['currInterest']) == currInterest, \
                    f'{self.fund_flow_type["currInterest"]}-校验失败'

