class Assert:
    @staticmethod
    def base_check_response(res, get_field=''):
        assert isinstance(res, dict), f'response is not json type.\r\n response is : \r\n {res}'
        assert res.get('status', 'err') == 'ok', f'response status is not ok.\r\n response is : \r\n {res}'
        if get_field:
            assert res.get(get_field, False), f'"{get_field}" not in response.\r\n response is : \r\n {res}'
            return res.get(get_field)
        return res
