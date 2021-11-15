#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import pytest, allure, random, time
from tool.atp import ATP
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('撤单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_070:
    ids = ["TestSwapEx_070",
           "TestSwapEx_074",
           "TestSwapEx_078"]
    params = [
        {
            "case_name": "卖出开仓 挂单 撤销",
            "ratio": 1.5,
            "volume":2
        },{
            "case_name": "卖出开仓 全部成交 撤销",
            "ratio": 1.0,
            "volume":2
        },{
            "case_name": "卖出开仓 部分成交 撤销",
            "ratio": 1.0,
            "volume":4
        }

    ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy',
                              volume=4)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        allure.dynamic.description("先挂买单4张："
                                   "\n下单价格为当前价的1.5倍，无法成交；"
                                   "\n以当前价下单，数量为2，则全部成交;"
                                   "\n以当前价下单，数量为4；当前买盘只有2张，所以会部分成交；"
                                   "\n最后撤单所有限价单")
        with allure.step('下单'):
            orderInfo = user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice * params['ratio'], 2),
                                          volume=params['volume'], direction='sell')
            pass
        with allure.step('校验撮合表'):
            sqlStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            except_result = ((1,),) #预期结果
            result = retryUtil(DB_orderSeq.execute,sqlStr,except_result)
            assert result[0][0] == 1
            pass

if __name__ == '__main__':
    pytest.main()
