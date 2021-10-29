#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20210929
# @Author : YuHuiQing

from common.LinearServiceAPI import user01
import pytest, allure, random, time
from tool.atp import ATP

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('平仓')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
class TestLinearTriggerCloseBuy_004:

    ids=['TestLinearTriggerCloseBuy_005',
         'TestLinearTriggerCloseBuy_006',
         'TestLinearTriggerCloseBuy_004',
         'TestLinearTriggerCloseSell_005',
         'TestLinearTriggerCloseSell_006',
         'TestLinearTriggerCloseSell_004']
    params = [{'titleName': '平空-触发价低于最新价', 'direction':'buy', 'trgRatio':0.99, 'ordRatio':0.98},
            {'titleName': '平空-触发价等于最新价', 'direction':'buy', 'trgRatio':1.00, 'ordRatio':0.98},
            {'titleName': '平空-触发价高于最新价', 'direction':'buy', 'trgRatio':1.01, 'ordRatio':0.98},
            {'titleName': '平多-触发价低于最新价', 'direction':'sell', 'trgRatio':0.99, 'ordRatio':0.98},
            {'titleName': '平多-触发价等于最新价', 'direction':'sell', 'trgRatio':1.00, 'ordRatio':0.98},
            {'titleName': '平多-触发价高于最新价', 'direction':'sell', 'trgRatio':1.01, 'ordRatio':0.98}]

    @allure.step('测试执行')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,contract_code,params):
        with allure.step('1、行情-最新价更新为49800'):
            allure.dynamic.title(params['titleName'])
            allure.dynamic.description('\n测试标题：'+params['titleName']+'场景，验证计划委托-委托触发'
                                      '\n*、先清盘避免盘口数据干扰;'
                                      '\n*、以'+params['titleName']+'下单计划委托单；'
                                      '\n*、触发计划委托订单；'
                                      '\n*、验证计划委托订单触发否')
            print("清盘》》》》", ATP.clean_market())
            currentPrice = ATP.get_current_price()  # 最新价
            trigger_price = round(params['trgRatio']*currentPrice,2) #触发价
            order_price = round(params['ordRatio']*currentPrice,2) #买入价
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if trigger_price >= currentPrice:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'
            pass
        with allure.step('2、计划委托下单，触发价为50000；买入价为49800；'):
            orderResult = user01.linear_trigger_order(contract_code=contract_code,
                                                      trigger_type=trigger_type,
                                                      trigger_price=trigger_price,
                                                      offset='close',
                                                      order_price=order_price,direction=params['direction'])
            # 下单失败则断言失败
            if 'err_msg' in orderResult:
                print(orderResult)
                assert False
            else:
                triggerOrderId = orderResult['data']['order_id']
                print('计划委托单号 = ', triggerOrderId)
            pass
        with allure.step('3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单'):
            # 等待成交刷新最新价
            time.sleep(0.5)
            user01.linear_order(contract_code=contract_code, price=trigger_price, direction='buy')
            user01.linear_order(contract_code=contract_code, price=trigger_price, direction='sell')
            time.sleep(0.5)
            pass
        with allure.step('4、验证计划委托单被触发'):
            triggerOrderHistoryOrders = user01.linear_trigger_hisorders(contract_code=contract_code,status=4)
            # print('计划委托7天内买入平空单历史 =',triggerOrderHistoryOrder)
            historySize = triggerOrderHistoryOrders['data']['total_size']
            # 单页只显示10条数据
            if historySize > 10:
                historySize = 10
            elif historySize == 0:  # 未触发
                assert False

            flag =False
            for i in range(int(historySize)):
                triggerOrderHistoryOrder = triggerOrderHistoryOrders['data']['orders'][i]['order_id']
                # 循环历史计划委托单，获取测试的计划委托单
                if triggerOrderHistoryOrder == triggerOrderId:
                    # 在历史记录中找到了该计划委托订单则跳出循环，不再查找
                    flag = True
                    break

            assert flag
            pass

if __name__ == '__main__':
    pytest.main()
