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
    def get_global_data(cls, env=None, system_type=None):
        atp_url = cls.ATPHost + "/global_data/get_all_global_data_by_env_and_system_type"
        params = {"env": env,
                  "system_type": system_type}
        response = requests.get(atp_url, headers=cls.header, params=params)
        return response.json()

    @classmethod
    def clean_market(cls, system_type, contract_code, direction=None):
        atp_url = cls.ATPHost + "/jobs/market_control"
        body = {"env": conf.ENV,
                "system_type": system_type,
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
    print(ATP.get_global_data())
    print(ATP.get_global_data(env='Test6'))
    print(ATP.get_global_data(env='Test20', system_type='LinearSwap'))
    print(ATP.clean_market(system_type='LinearSwap', contract_code='ETH-USDT', direction='sell'))
    print(ATP.clean_market(system_type='Swap', contract_code='BSV-USD', direction='buy'))
    print(ATP.clean_market(system_type='Delivery', contract_code='ETH211231'))
