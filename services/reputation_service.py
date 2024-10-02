from abc import ABC, abstractmethod

import requests


# region generic reputation service
class GenericReputationService(ABC):
    _instance = None

    # singleton class
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GenericReputationService, cls).__new__(cls)
        return cls._instance

    @abstractmethod
    def get_ip_address_reputation(self, ip: str, max_retries: int):
        pass


# endregion

# region IPInfo adapter
class IPInfoAdapter(GenericReputationService):
    __api_url = "https://ipinfo.io/{0}?token=126401736d626c"

    def get_ip_address_reputation(self, ip: str, max_retries: int):
        retry_counter = 0

        while retry_counter <= max_retries:
            try:
                reputation_result = self.__get_ip_reputation_info(ip)
                result = {
                    'ip': ip,
                    'api-name': 'IPInfo',
                    'api-result': reputation_result,
                }
                return True, result
            except Exception as ex:
                retry_counter += 1
                if retry_counter > max_retries:
                    return False, str(ex)

        return False, "Max retries exceeded"

    def __get_ip_reputation_info(self, ip: str):
        reputation_result = {}
        headers = {
            "accept": "application/json",
        }
        api_url = self.__api_url.format(ip)
        response = requests.get(api_url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            reputation_result = response.json()

        return reputation_result
# endregion
