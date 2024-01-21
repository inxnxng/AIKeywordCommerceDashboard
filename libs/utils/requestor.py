import logging
from typing import Any, Dict

import requests

from libs.utils.singleton import Singleton


class Requestor(metaclass=Singleton):
    def __init__(self, source: str = None):
        self._source = source

    @property
    def headers(custom_headers=None):
        if custom_headers is None:
            headers = {}
        headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.149 Safari/537.36"
        )
        return headers

    def __return_response_json(self, response: requests.Response) -> Dict[str, Any]:
        res = response.json()
        logging.info(f"Response: {res}")
        return res

    def __check_response(self, response: requests.Response) -> Dict[str, Any]:
        if not response.ok:
            raise Exception(f"Request failed with status code {response.status_code} and message {response.text}")

    def __response_handler(self, response: requests.Response) -> Dict[str, Any]:
        self.__check_response(response)
        return self.__return_response_json(response)

    def get(self, url, params=None, headers=None, timeout=10):
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        return self.__response_handler(response)

    def post(self, url, data=None, json=None, headers=None, timeout=10):
        response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout)
        return self.__response_handler(response)
