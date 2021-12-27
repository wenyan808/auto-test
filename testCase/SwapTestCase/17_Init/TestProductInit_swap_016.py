#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/6 9:57 上午
# @Author  : HuiQing Yu

import time

import allure
import pytest

from common.SwapMqComm import mqComm
from common.SwapServiceAPI import user01, user02
from common.mysqlComm import mysqlComm
from common.redisComm import redisConf
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[16]['feature'])
@allure.story(features[16]['story'][0])
@allure.tag('Script owner : 余辉青', 'Case owner : 曾超群')
@pytest.mark.stable
class TestProductInit_swap_016:
    ids = ['TestProductInit_swap_016']
    params = [{'case_name': '检查用户已开户，有资金有多方向持仓，品种初始化'}]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.redisClient = redisConf('redis6380').instance()
            cls.symbol = DEFAULT_SYMBOL
            cls.mysqlClient= mysqlComm()
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = SwapTool.currentPrice()
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：查看用户是否有仓位'):
            name = f'RsT:APO:11538485#{self.symbol}'
            key = f'Position:#{self.symbol}#{self.contract_code}#'
            position_info_1 = int(float(str(self.redisClient.hmget(name=name, keys=key + '1')).split(',')[5]))
            position_info_2 = int(float(str(self.redisClient.hmget(name=name, keys=key + '2')).split(',')[5]))
            pass
        with allure.step('操作：仓位调整(有多仓则跳过,无则持多仓；有空仓则清仓，无则跳过)'):
            if position_info_1 == 0:
                print(f'当前用户未持多仓,数量{position_info_1},开始进行持多仓……')
                user01.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=1,
                                  offset='open', direction='buy')
                user02.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=1,
                                  offset='open', direction='sell')
            elif position_info_2 > 0:
                print(f'当前用户持有空数量{position_info_1},开始进行清仓……')
                user01.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=position_info_2,
                                  offset='close', direction='buy')
                user02.swap_order(contract_code=self.contract_code, price=self.latest_price,
                                  volume=position_info_2,
                                  offset='open', direction='sell')

            pass
        with allure.step(f'操作：删除Redis Key={name}'):
            time.sleep(1)  # 等待清仓完成
            self.redisClient.delete(name)
            pass
        with allure.step('操作：发送MQ信息'):
            mq_result = mqComm.productTradeStatus(symbol=self.symbol)
            if mq_result and mq_result['routed']:
                print('MQ信息发送成功……')
            else:
                assert False, 'MQ发送失败……'
            pass
        with allure.step(f'验证：Redis Key={name}初始化成功'):
            time.sleep(1)  # 等待初始化完成
            keys = [f'Position:#{self.symbol}#{self.contract_code}#1',  # 多仓key
                    f'Position:#{self.symbol}#{self.contract_code}#2',  # 空仓key
                    f'orderPositionFrozen:{self.contract_code}#1',
                    f'orderPositionFrozen:{self.contract_code}#2',
                    f'clearUnPositionFrozen:{self.contract_code}#1',
                    f'clearUnPositionFrozen:{self.contract_code}#2',
                    f'Account:#{self.symbol}',
                    'orderFrozenMargin',
                    'clearUnFrozenMargin',
                    ]
            for key in keys:
                result = self.redisClient.hmget(name=name, keys=key)
                assert result[0] is not None, key + '校验失败'
            pass
        with allure.step(f'验证：t_product 中品种={self.symbol}初始化成功'):
            sqlStr = f'select init_status from t_product where product_id="{self.symbol}"'
            flag = False
            for i in range(3):
                db_info = self.mysqlClient.selectdb_execute(dbSchema='contract_trade',sqlStr=sqlStr)
                if len(db_info) and db_info[0]['init_status'] == 1:
                    flag = True
                    break
                else:
                    print(f'初始化未完成，第{i + 1}重试查询……')
                    time.sleep(1)
            assert flag, '多次重试验证DB初始化状态校验失败'
