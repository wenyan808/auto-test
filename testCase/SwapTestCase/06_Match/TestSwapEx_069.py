#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211018
# @Author : HuiQing Yu

import pytest, allure, random, time
from common.CommonUtils import currentPrice
from common.mysqlComm import mysqlComm
from common.SwapServiceAPI import user01
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('撤单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapEx_069:
    ids = ["TestSwapEx_069",
           "TestSwapEx_073",
           "TestSwapEx_077"]
    params = [
        {
            "case_name": "买入开仓 挂单 撤销",
            "ratio": 0.5,
            "volume":2
        },{
            "case_name": "买入开仓 全部成交 撤销",
            "ratio": 1.0,
            "volume":2
        },{
            "case_name": "买入开仓 部分成交 撤销",
            "ratio": 1.0,
            "volume":4
        }

    ]
    contract_code = DEFAULT_CONTRACT_CODE
    DB_orderSeq = mysqlComm('order_seq')

    @classmethod
    def setup_class(cls):
        with allure.step('*->挂盘'):
            cls.currentPrice = currentPrice()  # 最新价
            user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell',
                              volume=4)
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('*->恢复环境:取消挂单'):
            user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        allure.dynamic.description("先挂卖单4张："
                                   "\n下单价格为当前价的一半，无法成交；"
                                   "\n以当前价下单，数量为2，则全部成交;"
                                   "\n以当前价下单，数量为4；当前买盘只有2张，所以会部分成交；"
                                   "\n最后撤单所有限价单")

        with allure.step('操作：开多下单'):
            orderInfo = user01.swap_order(contract_code=self.contract_code, price=round(self.currentPrice * params['ratio'], 2),
                                          volume=params['volume'], direction='buy')
            pass
        with allure.step('验证：订单存在撮合结果表'):
            sqlStr = "select count(1) from t_exchange_match_result WHERE f_id = " \
                     "(select f_id from t_order_sequence where f_order_id= '%s')" % (orderInfo['data']['order_id'])
            flag = False
            # 给撮合时间，5秒内还未撮合完成则为失败
            for i in range(5):
                isMatch = self.DB_orderSeq.execute(sqlStr)[0][0]
                if 1 == isMatch:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag



if __name__ == '__main__':
    pytest.main()
