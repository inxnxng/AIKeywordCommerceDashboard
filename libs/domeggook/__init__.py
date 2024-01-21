import json
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

from libs.utils.prettier import interger_prettier
from libs.utils.requestor import Requestor


class Domeggok(Requestor):
    def __init__(self):
        self._name = "Domeggok"
        self._description = "Domeggok is a library for creating and managing Discord bots."
        self._url = "https://openapi.domeggook.com/main/reference/lst_open"
        self._version = "4.0"
        self._author = "Domeggook"

        self.api_url = "https://domeggook.com/ssl/api/"
        self.aid: str = st.secrets.domeggook.api_key

    def default_params(self, version: str = None):
        if version is None:
            version = self._version
        return {
            "ver": version,
            "aid": self.aid,
            "om": "json",
        }

    def __get_product_from_list_handler(self, results: List[Dict[str, Any]]):
        return [
            {
                "no": result["no"],
                "title": result["title"],
                "thumb": result["thumb"],
                "idxCOM": result["idxCOM"],
                "id": result["id"],
                "price": interger_prettier(result["price"]),
                "unitQty": interger_prettier(result["unitQty"]),
                "comOnly": result["comOnly"],
                "adultOnly": result["adultOnly"],
                "lwp": result["lwp"],
                "url": result["url"],
            }
            for result in results.copy()
        ]

    def __get_item_list_handler(self, result: dict):
        return {
            "numberOfItems": result["domeggook"]["header"]["numberOfItems"],
            "currentPage": result["domeggook"]["header"]["currentPage"],
            "numberOfPages": result["domeggook"]["header"]["numberOfPages"],
            "list": self.__get_product_from_list_handler(result["domeggook"]["list"]["item"]),
        }

    def getItemList(self, ev: str, ca: str, kw: str, pg: int = 1, sz: int = 20, version: str = "4.1", **kwargs):
        """
        @latest version: 4.1
        https://openapi.domeggook.com/main/reference/detail?api_no=68&scope_code=SCP_OPEN
        """
        mode = "getItemList"
        response = self.get(
            url=f"{self.api_url}",
            params={
                # required
                "mode": mode,
                **self.default_params(version=version),
                # search option
                "market": "dome",
                "ev": ev,
                "ca": ca,
                "kw": kw,
                # result option
                "so": "se",
                "pg": pg,
                "sz": sz,
                # etcq
                **kwargs,
            },
        )
        return self.__get_item_list_handler(response)

    def __category_handler(self, categories: dict):
        return [
            {
                "name": category["name"],
                "code": category["code"],
            }
            for category in categories["parents"]["elem"] + [categories["current"]]
        ]

    def __option_handler(self, options: dict):
        options = json.loads(options)
        return [{"name": option["name"], "domPrice": option["domPrice"]} for option in options["data"].values()]

    def get_item_detail_handler(self, result: dict):
        res = result["domeggook"]
        return {
            "status": res["basis"]["status"],
            "title": res["basis"]["title"],
            "keywords": res["basis"]["keywords"]["kw"],
            "price": res["price"]["dome"],
            "images": [res["thumb"][key] for key in res["thumb"].keys() if res["thumb"][key].startswith("https://")],
            "image_use": res["desc"]["license"]["usable"] == "true",
            "description": res["desc"]["contents"]["item"],
            "options": self.__option_handler(res["selectOpt"]),
            "detail": res["detail"],
            "category": self.__category_handler(res["category"]),
            "return": res["return"],
        }

    @st.cache_data()
    def getItemDetail(_self, no: int, version: str = "4.4", **kwargs):
        """
        @latest version: 4.4
        https://openapi.domeggook.com/main/reference/detail?api_no=73&scope_code=SCP_OPEN
        """
        mode = "getItemView"
        print(f"api {no} ----------------------------")

        response = _self.get(
            url=f"{_self.api_url}",
            params={
                "mode": mode,
                **_self.default_params(version=version),
                #
                "no": no,
                #
                **kwargs,
            },
        )
        print(response)
        return response

    def getImageAllowItems(self, moq: str = "true", version: str = "1.1", **kwargs):
        """
        @latest version: 1.1
        https://openapi.domeggook.com/main/reference/detail?api_no=310&scope_code=SCP_OPEN
        """
        mode = "getImageAllowItems"
        return self.get(
            url=f"{self.api_url}",
            params={
                "mode": mode,
                **self.default_params(version=version),
                #
                "page": 0,
                "moq": moq,  # 최소주문수량이 1인 상품만 가져옴
                **kwargs,
            },
        )

    def change_D_to_Naver(self, sale_price, input_product_info):
        data = input_product_info["domeggook"]

        title = data["basis"]["title"]

        sale_start_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        sale_end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S").replace("datetime.now().year", "2039")

        stock_quantity = 9999

        category_id = data["category"]["current"]["code"]
        detail_content = data["desc"]["contents"]["item"]
        images = data["thumb"]

        detail = data["desc"]["content"]["item"]
        manufacturer = detail.get("manufacturer", "")

        return {
            "originProduct": {
                "statusType": "WAIT",  # WAIT SALE OUTOFSTOCK UNADMISSION REJECTION SUSPENSION CLOSE PROHIBITION DELETE
                "saleType": "NEW",  # NEW OLD
                "leafCategoryId": category_id,
                "name": title,
                "detailContent": detail_content,
                "images": {
                    "representativeImage": {"url": images.pop("original")},
                    "optionalImages": [{"url": img} for img in images.values()],
                },
                "saleStartDate": sale_start_date,
                "saleEndDate": sale_end_date,
                "salePrice": sale_price,
                #######################################
                "stockQuantity": stock_quantity,
                "deliveryInfo": {
                    "deliveryType": "DELIVERY",
                    "deliveryAttributeType": "NORMAL",
                    "deliveryCompany": "HANJIN",
                    "deliveryFee": {},
                },
            },
        }
