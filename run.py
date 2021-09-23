#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


import os, sys
from string import Template

from config.conf import set_run_env_and_system_type
from tool.DingDingMsg import DingDingMsg

"""
pytest 命令中加入 '-n 数字'可实现分布式执行测试用例，数字表示执行用例的机器数，但是由于速度过快被api接口限频，如果需要可考虑调大测试环境限频
pytest 命令中加入 --html=./report/html/TestReoprt%s.html  --self-contained-html  可生成htlm测试报告
pytest  -m "not xxx" 表示不执行有@pytest.mark.xxx标记的用例 

要使用allure生成测试报告需要经过两步

1 生成测试结果的json文件
使用pytest运行测试脚本时，添加参数pytest --alluredir=json文件生成路径
可以将参数直接写道配置文件中addopts = -s --alluredir=./report
有几个测试用例就会生成几个测试结果的json文件，这些文件在其他语言中也是通用的
多次运行，之前保存的json会保留下来，而且可以在报告中查看之前的测试结果

2 将json数据文件生成HTML测试报告
使用allure generate json文件路径可以生成测试报告，默认生成文件夹为allure-report，指定文件夹可以使用-o参数allure generate json文件路径 -o HTML报告路径
如果JSON文件路径错误，也可以生成测试报告不会报错，但是打开HTML文件是空的
当生成过测试报告，如果已经存在报告路径文件夹时，再次使用会提示添加--clean参数来重写
allure generate ./report --clean
allure generate ./report -o ./html_report --clean
不生成HTML文件，直接在浏览器打开allure serve json文件路径。运行后生成临时文件夹存放HTML报告，在浏览器打开
使用命令打开HTML报告：allure open html报告路径，也可以直接打开index.html。
参考文档：https://www.codenong.com/cs107116946/
        https://blog.csdn.net/liuchunming033/article/details/79624474
        https://www.cnblogs.com/poloyy/category/1690628.html
#将xml报告转换成html,启动allure服务，在浏览器中展示报告
# os.system('allure generate report/allure -o report/html --clean')
# os.system('allure open report/html')
"""


def run(system_type=None, run_env='Test5', test_type=''):
    """
    新执行脚本由jenkins中的shell传入执行模块，执行方式为
    python3 run.py 模块名
    exit 0
    """
    system_types = {
        'Contract': 'Delivery',
        'Swap': 'Swap',
        'Linear': 'LinearSwap',
        'Option': 'Option',
        'Schema': 'Schema'
    }
    if system_type == 'ALL':
        set_run_env_and_system_type(run_env)
        if test_type:
            os.system(f'pytest --alluredir report/allure testCase/ -m "{test_type}"')
        else:
            os.system('pytest --alluredir report/allure testCase/')
    elif type(system_type) == str:
        if system_type.capitalize() in ['Contract', 'Swap', 'Linear', 'Option', 'Schema']:
            set_run_env_and_system_type(run_env, system_types[system_type.capitalize()])
            if test_type:
                os.system('pytest --alluredir report/allure testCase/{}TestCase -m "{}"'.format(system_type.capitalize(),
                                                                                              test_type))
            else:
                os.system(
                    'pytest --alluredir report/allure testCase/{}TestCase'.format(system_type.capitalize()))
        else:
            print('输入错误')
    else:
        print('输入错误')


if __name__ == '__main__':
    system_type = sys.argv[1]
    build_num = sys.argv[2]
    test_type = sys.argv[3]

    # for debug
    # system_type = 'Linear'
    # build_num = 10
    # test_type = 'stable'

    DingDingMsg.init_result(env='Test5', system_type=system_type, test_type=test_type)
    run(system_type, test_type=test_type)
    DingDingMsg.update_json_file(build_num)


