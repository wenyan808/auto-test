#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import pytest, allure, random, time
from common.CommonUtils import currentPrice
from common.mysqlComm import mysqlComm
from common.SwapServiceAPI import user01,user02
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[5]['feature'])
@allure.story(features[5]['story'][3])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_070:
    ids = ["TestSwapEx_072",
           "TestSwapEx_076",
           "TestSwapEx_080"]
    params = [
        {
            "case_name": "卖出平仓 挂单 撤销",
            "ratio": 1.5,
            "volume":2
        },{
            "case_name": "卖出平仓 全部成交 撤销",
            "ratio": 1.0,
            "volume":2
        },{
            "case_name": "卖出平仓 部分成交 撤销",
            "ratio": 1.0,
            "volume":4
        }

    ]

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.latest_price = currentPrice()
            pass
        with allure.step('*->挂盘'):
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='buy',
                              volume=8)
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.latest_price, 2), direction='sell',
                              volume=4)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            user02.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params,DB_orderSeq):
        allure.dynamic.title(params['case_name'])
        allure.dynamic.description("先挂买单4张："
                                   "\n下单价格为当前价的1.5倍，无法成交；"
                                   "\n以当前价下单，数量为2，则全部成交;"
                                   "\n以当前价下单，数量为4；当前买盘只有2张，所以会部分成交；"
                                   "\n最后撤单所有限价单")

        with allure.step('操作：下单'):
            orderInfo = user01.swap_order(contract_code=self.contract_code, price=round(self.latest_price * params['ratio'], 2),
                                          volume=params['volume'], direction='sell',offset='close')
            pass
        with allure.step('验证：订单存在撮合表'):
            orderId = orderInfo['data']['order_id_str']
            sqlStr = f'select count(1) as count from t_exchange_match_result ' \
                     f'WHERE f_id = (select f_id from t_order_sequence where f_order_id= {orderId})'
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(3):
                isMatch = DB_orderSeq.dictCursor(sqlStr)[0]['count']
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i+1))
            assert flag
            pass

if __name__ == '__main__':
    pytest.main()
