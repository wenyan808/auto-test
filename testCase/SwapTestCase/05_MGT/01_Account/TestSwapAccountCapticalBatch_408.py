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
class TestSwapAccountCapticalBatch_408:
    ids = [
        'TestSwapAccountCapticalBatch_408',
        'TestSwapAccountCapticalBatch_409',
        'TestSwapAccountCapticalBatch_410',
        'TestSwapAccountCapticalBatch_411',
        'TestSwapAccountCapticalBatch_412',
        'TestSwapAccountCapticalBatch_413',
        'TestSwapAccountCapticalBatch_414',
        'TestSwapAccountCapticalBatch_417',
        'TestSwapAccountCapticalBatch_418',
        'TestSwapAccountCapticalBatch_419',
        'TestSwapAccountCapticalBatch_420',
        'TestSwapAccountCapticalBatch_421',
        'TestSwapAccountCapticalBatch_422',
        'TestSwapAccountCapticalBatch_423',
        'TestSwapAccountCapticalBatch_424',
        'TestSwapAccountCapticalBatch_425',
        'TestSwapAccountCapticalBatch_426',
        'TestSwapAccountCapticalBatch_427',
        'TestSwapAccountCapticalBatch_428',
        'TestSwapAccountCapticalBatch_429',
        'TestSwapAccountCapticalBatch_430',
        'TestSwapAccountCapticalBatch_431',
    ]
    params = [
                {'title':'TestSwapAccountCapticalBatch_408','case_name': '平台流水表-结算对账-【从币币转入】横向对账','colName':'moneyIn'},
                {'title':'TestSwapAccountCapticalBatch_409','case_name': '平台流水表-结算对账-【转出至币币】横向对账','colName':'moneyOut'},
                {'title':'TestSwapAccountCapticalBatch_410','case_name': '平台流水表-结算对账-【借贷转运营】横向对账','colName':'borrowToOperate'},
                {'title':'TestSwapAccountCapticalBatch_411','case_name': '平台流水表-结算对账-【运营转借贷】横向对账','colName':'operateToBorrow'},
                {'title':'TestSwapAccountCapticalBatch_412','case_name': '平台流水表-结算对账-【注入到爆仓】横向对账','colName':'toBurst'},
                {'title':'TestSwapAccountCapticalBatch_413','case_name': '平台流水表-结算对账-【从爆仓提取】横向对账','colName':'fromBurst'},
                {'title':'TestSwapAccountCapticalBatch_414','case_name': '平台流水表-结算对账-【给用户赠币赔偿】横向对账','colName':'compensate'},
                {'title':'TestSwapAccountCapticalBatch_417','case_name': '平台流水表-结算对账-【扣减用户资产惩戒】横向对账','colName':'discipline'},
                {'title':'TestSwapAccountCapticalBatch_418','case_name': '平台流水表-结算对账-【手续费转运营】横向对账','colName':'feeToOperate'},
                {'title':'TestSwapAccountCapticalBatch_419','case_name': '平台流水表-结算对账-【活动奖励】横向对账','colName':'actionReward'},
                {'title':'TestSwapAccountCapticalBatch_420','case_name': '平台流水表-结算对账-【返利】横向对账','colName':'dividend'},
                {'title':'TestSwapAccountCapticalBatch_421','case_name': '平台流水表-结算对账-【开仓手续费挂单】横向对账','colName':'openFeeMaker'},
                {'title':'TestSwapAccountCapticalBatch_422','case_name': '平台流水表-结算对账-【开仓手续费吃单】横向对账','colName':'openFeeTaker'},
                {'title':'TestSwapAccountCapticalBatch_423','case_name': '平台流水表-结算对账-【平仓手续费挂单】横向对账','colName':'closeFeeMaker'},
                {'title':'TestSwapAccountCapticalBatch_424','case_name': '平台流水表-结算对账-【平仓手续费吃单】横向对账','colName':'closeFeeTaker'},
                {'title':'TestSwapAccountCapticalBatch_425','case_name': '平台流水表-结算对账-【交割手续费】横向对账','colName':'deliveFee'},
                {'title':'TestSwapAccountCapticalBatch_426','case_name': '平台流水表-结算对账-【资金费-收入】横向对账','colName':'capitalFeeIn'},
                {'title':'TestSwapAccountCapticalBatch_427','case_name': '平台流水表-结算对账-【资金费-支出】横向对账','colName':'capitalFeeOut'},
                {'title':'TestSwapAccountCapticalBatch_428','case_name': '平台流水表-结算对账-【资金费转运营】横向对账','colName':'capitalFeeToOperate'},
                {'title':'TestSwapAccountCapticalBatch_429','case_name': '平台流水表-结算对账-【运营转资金费】横向对账','colName':'operateToCapitalFee'},
                {'title':'TestSwapAccountCapticalBatch_430','case_name': '平台流水表-结算对账-【平账】横向对账','colName':'flatMoney'},
                {'title':'TestSwapAccountCapticalBatch_431','case_name': '平台流水表-结算对账-【当期流水】横向对账','colName':'currInterest'},
              ]
    DB_btc = mysqlComm('btc')

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
            pass
        with allure.step('操作：执行查询'):
            sqlStr = 'SELECT end_time,id ' \
                     'FROM t_settle_log t ' \
                     'where progress_code=13 ' \
                     f'and product_id= "{cls.symbol}" ' \
                     'order by end_time desc limit 2 '
            db_info = cls.DB_btc.dictCursor(sqlStr=sqlStr)
            cls.endDateTime = db_info[0]['end_time']
            cls.beginDateTime = db_info[1]['end_time']
            request_params = [
                cls.symbol,
                2,
                {
                    "productId": cls.symbol,
                    "type": 2,
                    "endDateTime": cls.endDateTime,
                    "beginDateTime": cls.beginDateTime,
                    # "endDailyDateTime": "2021/12/13",
                    # "beginDailyDateTime": "2021/12/12",
                    # "date": 19,
                    "originSettleId": db_info[1]['id'],
                    "finalSettleId": db_info[0]['id'],
                    "reOpen": False,
                    "originTime": cls.beginDateTime,
                    "finalTime": cls.endDateTime
                }
            ]
            result = SwapServiceMGT.findPaltformFlow(params=request_params)
            # '用户类型 1普通用户，2爆仓用户，3应付外债，4交易手续费，5交割手续费，9运营活动，11是平台资产 12是应付用户 13是平账账户',
            cls.daily = json.loads(result['data'])
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('param', params, ids=ids)
    def test_execute(self, param, DB_btc):
        allure.dynamic.title(param['title'])
        with allure.step('操作:从接口返回中取出-各用户类型-数据'):
            for data in self.daily['daily']:
                if data['userType'] == 11: #平台资产
                    plat_form = data
                elif data['userType'] == 12: #应付用户
                    pay_user = data
                elif data['userType'] == 3: #应付外债
                    pay_debt = data
                elif data['userType'] == 4: #交易手续费
                    deal_fee = data
                elif data['userType'] == 5: #互换账户
                    hh_user = data
                elif data['userType'] == 9: #运营账户
                    operate_user = data
                elif data['userType'] == 13: #平账账户
                    flat_user = data
                else:
                    hxdz = data    #横向对账
            col_name = param['colName']
        with allure.step(f'验证:{self.fund_flow_type[col_name]}-横向对账'):
            # 横向对账，平账数据是从平账userType返回里面获取；其他都是横向对账数据中获取即接口中userType=None的数据中
            if 'flatMoney' in col_name:
                expectResult = Decimal(flat_user[col_name])
            else:
                expectResult = Decimal(hxdz[col_name])
            print(f'{self.fund_flow_type[col_name]}:平台资产({plat_form[col_name]})-('
                  f'应付用户({pay_user[col_name]})+'
                  f'应付外债({pay_debt[col_name]})+'
                  f'交易手续费({deal_fee[col_name]})+'
                  f'互换账户({hh_user[col_name]})+'
                  f'运营账户({operate_user[col_name]}))) == 横向对账({expectResult})')
            assert Decimal(plat_form[col_name]) -\
                   ( Decimal(pay_user[col_name]) +
                     Decimal(pay_debt[col_name]) +
                     Decimal(deal_fee[col_name]) +
                     Decimal(hh_user[col_name]) +
                     Decimal(operate_user[col_name])
                     ) - expectResult <=0.00000001,\
                f'{self.fund_flow_type[col_name]}-横向对账 校验失败'