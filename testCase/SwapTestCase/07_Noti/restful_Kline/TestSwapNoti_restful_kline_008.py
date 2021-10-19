#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211015
# @Author : 
    用例标题
        restful请求K线1min size>2000
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        3
    用例别名
        TestSwapNoti_restful_kline_008
"""

from common.SwapServiceAPI import t as swap_api
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('restful请求K线')  # 这里填功能
@allure.story('restful请求K线1min 选填参数验证：size>2000')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_kline_008:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送restful请求kline的请求,类型=1min；"
              "\n*、选填参数是否传参：size>2000"
              "\n*、验证Kline返回结果：报错并提示错误原因，size=[1,2000]")

    @allure.title('restful请求K线1min size>2000')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            period = '1min'
            size = 2001
            toTime = int(time.time())
            fromTime = toTime - 60 * 60 * 24 * 30
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=period, size=size, to=toTime,
                                            From=fromTime)
            assert 'invalid size, valid range: [1,2000]' in kLineInfo['err-msg']
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
