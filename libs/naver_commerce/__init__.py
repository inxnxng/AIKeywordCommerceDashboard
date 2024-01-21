import time
from datetime import datetime
from typing import Any, Dict

import bcrypt
import pybase64
import streamlit as st

from libs.utils.requestor import Requestor


class NaverCommerce(Requestor):
    def __init__(self):
        self._name = "NaverCommerce"
        self._description = "NaverCommerce is a library for creating and managing Discord bots."
        self._url = "https://apicenter.commerce.naver.com/ko/basic/commerce-api"
        self._version = "1.0"
        self._author = "NaverCommerce"

        self.api_url = "https://api.commerce.naver.com"
        self.client_id: str = st.secrets.naver_commerce.client_id
        self.client_secret: str = st.secrets.naver_commerce.client_secret

    def __get_auth(self):
        clientId = st.secrets.naver_commerce.client_id
        clientSecret = st.secrets.naver_commerce.client_secret
        timestamp = int(time.time() * 1000)
        password = clientId + "_" + str(timestamp)

        hashed = bcrypt.hashpw(password.encode("utf-8"), clientSecret.encode("utf-8"))
        return pybase64.standard_b64encode(hashed).decode("utf-8")

    def upload(self, data: Dict[str, Any]):
        """
        https://apicenter.commerce.naver.com/ko/basic/commerce-api#tag/%EC%83%81%ED%92%88/operation/createProduct_1.product
        """
        path = "/external/v2/products"
        headers = {
            "Authorization": f"Bearer {self.__get_auth()}",
            "content-type": "application/json",
        }

        response = self.post(f"{self.api_url}/{path}", headers=headers, data=data)
        return response
