import json

import requests

from config import conf


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
    def clean_market(cls, contract_code, direction=None):
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


if __name__ == '__main__':
    print(ATP.get_api_test_data("test_linear_account_info"))
    print(ATP.get_api_test_data("test_linear_account_info", priority_list=["P0", "P1"]))

    # 清除盘口所有卖单
    print(ATP.clean_market(contract_code='ETH-USDT', direction='sell'))
    # 清除盘口所有买单
    print(ATP.clean_market(contract_code='BSV-USD', direction='buy'))
    # 清除盘口所有买卖挂单
    print(ATP.clean_market(contract_code='ETH211231'))
