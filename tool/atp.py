import json

import requests

from common.util import api_key_post
from config import conf
from pprint import pprint


class ATP:
    ATPHost = 'http://172.18.6.52:8000'
    # ATPHost = 'http://0.0.0.0:8000'
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    @classmethod
    def get_api_test_data(cls, script_path, priority_list=[], tags=[]):
        data_keys, variables_values_list = cls.get_api_test_data_old(script_path,
                                                                     priority_list=priority_list,
                                                                     tags=tags)
        api_test_data_list = [dict(zip(data_keys, variables_values)) for variables_values in variables_values_list]
        return api_test_data_list

    @classmethod
    def get_api_test_data_old(cls, script_path, priority_list=[], tags=[]):
        atp_url = cls.ATPHost + "/api_case/get_pytest_api_test_data_by_script_path"
        body = {"script_path": script_path,
                "priority_list": priority_list,
                "tags": tags}
        response = requests.post(atp_url, headers=cls.header, json=body)
        data_keys = response.json()['variables_keys_str'].split(",")
        variables_values_list = response.json()['variables_values_list']
        return data_keys, variables_values_list

    @classmethod
    def clean_market(cls, contract_code=None, direction=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        atp_url = cls.ATPHost + "/jobs/market_control"
        body = {"env": conf.ENV,
                "system_type": conf.SYSTEM_TYPE,
                'contract_code': contract_code,
                'job_name': 'CleanMarket'
                }
        if direction == 'sell':
            body['job_name'] = 'CleanSell'
        if direction == 'buy':
            body['job_name'] = 'CleanBuy'
        response = requests.post(atp_url, headers=cls.header, json=body)
        return response.json()

    @classmethod
    def cancel_all_order(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {}
        if conf.SYSTEM_TYPE == 'Delivery':
            if '_' in contract_code:
                json_body['symbol'] = contract_code.split('_')[0]
            else:
                json_body['symbol'] = contract_code[:-6]
        else:
            json_body['contract_code'] = contract_code

        response = api_key_post(conf.URL, conf.CANCEL_ALL_ORDER_URL, json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = api_key_post(conf.URL,
                                          conf.CANCEL_ALL_ORDER_URL.replace('swap_cancelall', 'swap_cross_cancelall'),
                                          json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有限价挂单')
        pprint(response)
        return response

    @classmethod
    def switch_level(cls, contract_code=None, lever_rate=5):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {'lever_rate': lever_rate}
        if conf.SYSTEM_TYPE == 'Delivery':
            if '_' in contract_code:
                json_body['symbol'] = contract_code.split('_')[0]
            else:
                json_body['symbol'] = contract_code[:-6]
        else:
            json_body['contract_code'] = contract_code

        response = api_key_post(conf.URL, conf.SWITCH_LEVER_URL, json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = api_key_post(conf.URL,
                                          conf.SWITCH_LEVER_URL.replace('swap_switch_lever_rate',
                                                                        'swap_cross_switch_lever_rate'),
                                          json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        pprint('修改当前品种杠杆 默认5倍')
        pprint(response)
        return response

    @classmethod
    def cancel_all_trigger_order(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {}
        if conf.SYSTEM_TYPE == 'Delivery':
            if '_' in contract_code:
                json_body['symbol'] = contract_code.split('_')[0]
            else:
                json_body['symbol'] = contract_code[:-6]
        else:
            json_body['contract_code'] = contract_code

        response = api_key_post(conf.URL, conf.CANCEL_ALL_TRIGGER_ORDER_URL, json_body, conf.ACCESS_KEY,
                                conf.SECRET_KEY)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = api_key_post(conf.URL,
                                          conf.CANCEL_ALL_TRIGGER_ORDER_URL.replace('swap_trigger_cancelall',
                                                                                    'swap_cross_trigger_cancelall'),
                                          json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有计划委托挂单')
        pprint(response)
        return response

    @classmethod
    def cancel_all_tpsl_order(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {}
        if conf.SYSTEM_TYPE == 'Delivery':
            if '_' in contract_code:
                json_body['symbol'] = contract_code.split('_')[0]
            else:
                json_body['symbol'] = contract_code[:-6]
        else:
            json_body['contract_code'] = contract_code

        response = api_key_post(conf.URL, conf.CANCEL_ALL_TPSL_ORDER_URL, json_body, conf.ACCESS_KEY,
                                conf.SECRET_KEY)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = api_key_post(conf.URL,
                                          conf.CANCEL_ALL_TPSL_ORDER_URL.replace('swap_tpsl_cancelall',
                                                                                 'swap_cross_tpsl_cancelall'),
                                          json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有止盈止损委托挂单')
        pprint(response)
        return response

    @classmethod
    def cancel_all_track_order(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {}
        if conf.SYSTEM_TYPE == 'Delivery':
            if '_' in contract_code:
                json_body['symbol'] = contract_code.split('_')[0]
            else:
                json_body['symbol'] = contract_code[:-6]
        else:
            json_body['contract_code'] = contract_code

        response = api_key_post(conf.URL, conf.CANCEL_ALL_TRACK_ORDER_URL, json_body, conf.ACCESS_KEY,
                                conf.SECRET_KEY)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = api_key_post(conf.URL,
                                          conf.CANCEL_ALL_TRACK_ORDER_URL.replace('swap_track_cancelall',
                                                                                  'swap_cross_track_cancelall'),
                                          json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有跟踪委托挂单')
        pprint(response)
        return response


if __name__ == '__main__':
    print(ATP.get_api_test_data("test_linear_account_info"))
    print(ATP.get_api_test_data("test_linear_account_info", priority_list=["P0", "P1"]))

    # 清除盘口所有卖单
    print(ATP.clean_market(contract_code='ETH-USDT', direction='sell'))
    # 清除盘口所有买单
    print(ATP.clean_market(contract_code='BSV-USD', direction='buy'))
    # 清除盘口所有买卖挂单
    print(ATP.clean_market(contract_code='ETH211231'))

    # 撤销当前用户 某个品种所有限价挂单
    print(ATP.cancel_all_order(contract_code='ETH211001'))
    # 修改当前品种杠杆 默认5倍
    print(ATP.switch_level(contract_code='ETH_CW'))
