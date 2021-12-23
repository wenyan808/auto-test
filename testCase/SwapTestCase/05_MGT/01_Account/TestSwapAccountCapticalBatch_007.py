#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/7 2:35 下午
# @Author  : HuiQing Yu

import json
from datetime import date, timedelta
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
class TestSwapAccountCapticalBatch_007:
    ids = ['TestSwapAccountCapticalBatch_007']
    params = [{'title':'TestSwapAccountCapticalBatch_007','case_name': '平台流水表-每日跑批-平账', 'userType': 13,'type':1}]

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
                "currInterest": "当期流水"
            }
            cls.money_type = {
                'openFeeTaker': 5,
                'openFeeMaker': 6,
                'closeFeeTaker': 7,
                'closeFeeMaker': 8,
                'deliveFee': 11,
                'moneyIn': 14,
                'moneyOut': 15,
                'flatMoney': 20,
                'borrowToOperate': 21,
                'operateToBorrow': 22,
                'feeToOperate': 23,
                'toBurst': 24,
                'fromBurst': 25,
                'compensate': 26,
                'discipline': 27,
                'actionReward': 28,
                'dividend': 29,
                'capitalFeeIn': 30,
                'capitalFeeOut': 31,
                'capitalFeeToOperate': 32,
                'operateToCapitalFee': 33,
            }
            cls.endDateTime = (date.today() + timedelta(days=-1)).strftime("%Y/%m/%d")
            cls.beginDateTime = (date.today() + timedelta(days=-8)).strftime("%Y/%m/%d")
            cls.s_batch_date = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
            cls.e_batch_date = (date.today() + timedelta(days=-8)).strftime("%Y%m%d")
            sqlStr = 'select flow_end_time from t_daily_log t ' \
                     f'where product_id="{cls.symbol}" ' \
                     f'AND batch_date in ("{cls.s_batch_date}","{cls.e_batch_date}") ' \
                     'order by flow_end_time desc'
            db_info = cls.mysqlClient.selectdb_execute(dbSchema='contract_trade',sqlStr=sqlStr)
            cls.s_batch_date = db_info[1]['flow_end_time']
            cls.e_batch_date = db_info[0]['flow_end_time']
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param):
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
            self.daily = json.loads(result['data'])
            pass
        with allure.step('操作:从接口返回中取出-平账-数据'):
            pay_money = None
            for data in self.daily['daily']:
                if data['userType'] == param['userType']:
                    pay_money = data
                    break
            assert pay_money, '返回数据中未找到-平账-数据，校验失败'
#################################################  【平账账户】当期流水	##################################################
        with allure.step(f'操作:从DB获取-平台资产(平账)-数据'):
            sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_flat_money_record ' \
                     f'WHERE flat_time > "{self.s_batch_date}" ' \
                     f'and flat_time<= "{self.e_batch_date}" ' \
                     'and flat_account=11 ' \
                     f'and product_id = "{self.symbol}"'
            flatMoney = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            if len(flatMoney) == 0 or flatMoney[0]['money'] is None:
                flatMoney = 0
            else:
                flatMoney = flatMoney[0]['money']
        with allure.step(f'操作:从DB获取-应付用户(平账)-数据'):
            sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                     f'WHERE create_time > "{self.s_batch_date}" ' \
                     f'and create_time<= "{self.e_batch_date}" ' \
                     f'AND money_type =  20 ' \
                     f'AND product_id = "{self.symbol}" ' \
                     'AND user_id not in (11186266, 1389607, 1389608, 1389609, 1389766) '
            payUserMoney = self.mysqlClient.selectdb_execute(dbSchema='btc',sqlStr=sqlStr)
            if len(payUserMoney) == 0 or payUserMoney[0]['money'] is None:
                payUserMoney = 0
            else:
                payUserMoney = payUserMoney[0]['money']
        with allure.step(f'操作:从DB获取-应付外债(平账)-数据'):
            payDebt = self.__dbResult(userId='11186266',dbName='btc')
        with allure.step(f'操作:从DB获取-交易手续费(平账)-数据'):
            dealFee = self.__dbResult(userId='1389607', dbName='btc')
        with allure.step(f'操作:从DB获取-互换账户(平账)-数据'):
            hhAccount = self.__dbResult(userId='1389608', dbName='btc')
        with allure.step(f'操作:从DB获取-运营账户(平账)-数据'):
            operateAccount = self.__dbResult(userId='1389609', dbName='btc')
        with allure.step(f'验证:流水类型-{self.fund_flow_type["flatMoney"]}'):
            assert Decimal(pay_money['flatMoney']) == flatMoney - ( payUserMoney+\
                   payDebt +\
                   dealFee+\
                   hhAccount+operateAccount)\
                , f'{self.fund_flow_type["flatMoney"]}-校验失败'

    def __dbResult(self,userId,dbName):
        sqlStr = 'SELECT TRUNCATE(sum(money),8) as money FROM t_account_action ' \
                 f'WHERE create_time > "{self.s_batch_date}" ' \
                 f'and create_time<= "{self.e_batch_date}" ' \
                 f'AND money_type =  20 ' \
                 f'AND product_id = "{self.symbol}" ' \
                 f'AND user_id = "{userId}" '
        money = self.mysqlClient.selectdb_execute(dbSchema=dbName,sqlStr=sqlStr)
        if len(money) == 0 or money[0]['money'] is None:
            money = 0
        else:
            money = money[0]['money']
        return money