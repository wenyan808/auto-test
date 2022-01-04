#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//17 初始化
用例标题
    检查用户已开户，有资金无持仓，个人初始化   
前置条件
    用户已开户，有资金无持仓
步骤/文本
    1、进入redis， 删除用户APO数据，命令    del RsT:APO:user_id#BCH   
    2、进入通用MQ，进入：exchanges  SM:productTradeStatus
    3、手动在MQ中发送品种初始化，{"BCH":{"BCH":1}}
    4、等待初始化完成后,判断品种初始化完成,查询品种表中 init_status=1（交易中，10为初始化中），select init_status from t_product where product_id='BCH' 
预期结果
    1、发送初始化命令后，查看redis中APO数据，存在该用户APO数据（注意:user_id需要实际替换成用户的ID）
        命令     hgetall RsT:APO:user_id#BCH    
    2、检查APO中数据，存在持仓、资金key  
        Position:#BCH#BCH211231#1              （交割有几个合约就要查几个合约，当周/次周/当季/次季）
        orderPositionFrozen:BCH211231#1        （交割有几个合约就要查几个合约，当周/次周/当季/次季）
        clearUnPositionFrozen:BCH211231#1      （交割有几个合约就要查几个合约，当周/次周/当季/次季）  
        Account:#BCH 
        orderFrozenMargin
        clearUnFrozenMargin
     
优先级
    p0
"""

import allure
import pytest
import time
from common.ContractServiceAPI import t as contract_api
from common.mysqlComm import mysqlComm
from common.redisComm import redisConf
from common.SwapMqComm import mqComm
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('初始化')  # 这里填功能
@allure.story('个人初始化')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 曾超群')
@pytest.mark.unstable
class TestUserInit_contract_015:

    @allure.step('前置条件:')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        print("前置条件")

    @allure.title(' 检查用户已开户，有资金无持仓，个人初始化')
    @allure.step('测试执行')
    def test_execute(self, symbol_period, symbol):

        redis_client = redisConf('redis6380').instance()
        with allure.step('操作：查看用户是否有仓位'):
            # 获取合约信息
            contract_type = 'this_week'
            contract_info = contract_api.contract_contract_info(
                symbol=symbol, contract_type=contract_type)
            print(contract_info)
            contract_code = contract_info["data"][0]["contract_code"]
            current_price = ATP.get_current_price(contract_code=symbol_period)

            name = f'RsT:APO:11538447#{symbol}'
            key = f'Position:#{symbol}#{contract_code}#'

            position_info_1 = int(
                float(str(redis_client.hmget(name=name, keys=key + '1')).split(',')[5]))
            position_info_2 = int(
                float(str(redis_client.hmget(name=name, keys=key + '2')).split(',')[5]))
            pass
        with allure.step('操作：有仓位进行平仓(无则跳过)'):
            if position_info_1 > 0:
                print(f'当前用户持有多仓数量{position_info_1},开始进行平仓……')
                contract_api.contract_order(contract_code=contract_code, price=current_price,
                                            volume=position_info_1, offset='close', direction='sell')
            if position_info_2 > 0:
                print(f'当前用户持有空数量{position_info_1},开始进行平仓……')
                contract_api.contract_order(contract_code=contract_code, price=current_price,
                                            volume=position_info_2,
                                            offset='close', direction='buy')
        with allure.step(f'操作：删除Redis Key={name}'):
            redis_client.delete(name)
            print('DEL Redis name {}'.format(name))
        with allure.step('操作：发送MQ信息'):
            mq_result = mqComm.productTradeStatus(symbol=symbol)
            if mq_result and mq_result['routed']:
                print('MQ信息发送成功……')
            else:
                assert False, 'MQ发送失败……'
            time.sleep(1)
        with allure.step(f'验证：Redis Key={name}初始化成功'):
            keys = [
                f'Account:#{symbol}',
                'orderFrozenMargin',
                'clearUnFrozenMargin',
            ]
            for key in keys:
                result = redis_client.hmget(name=name, keys=key)
                print(result[0])
                assert result[0] is not None, key + '校验失败'

        with allure.step('验证：t_product 中品种={}初始化成功'.format(symbol)):
            sqlStr = 'select init_status from t_product where product_id="{}"'.format(
                symbol)
            rec_dict_tuples = mysqlComm().selectdb_execute(
                dbSchema='contract_trade', sqlStr=sqlStr)
            if len(rec_dict_tuples) > 0:
                assert rec_dict_tuples[0]['init_status'] == 1
