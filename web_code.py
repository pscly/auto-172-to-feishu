"""
请求相关逻辑 - 优化方案一
"""

import os
import httpx
import requests
import re
import atexit
import json

from addict import Dict
from html import unescape


def match(self, regular, value, default="", group_id=None):
    try:
        obj = re.search(regular, value, re.S | re.I)
        if obj:
            if group_id:
                return obj.group(group_id)
            else:
                return obj.group()
        else:
            return default
    except Exception as e:
        print("正则提取错误", regular, e)
        return ""


class WebClient:
    """
    一个更抽象和易用的Web客户端。
    它在内部“懒加载”并管理一个httpx客户端实例，以实现高效的连接复用。
    """

    def __init__(self, headers: dict | None = None) -> None:
        self._client: httpx.Client | None = None

        # 如果没有提供 headers，则使用默认的
        if headers is None:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0 73362",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            }
        else:
            self.headers = headers

        # 注册一个在程序退出时自动调用的函数，确保客户端被关闭
        atexit.register(self.close)

    def _get_client(self) -> httpx.Client:
        """
        内部方法，用于获取或创建httpx客户端实例（懒加载）。
        如果客户端还未创建或是已经关闭，就创建一个新的。
        """
        if self._client is None or self._client.is_closed:
            print("Initializing new httpx client...")
            self._client = httpx.Client(
                headers=self.headers, follow_redirects=True, timeout=10.0
            )
        return self._client

    def get_html(self, url: str, de=True) -> str | None:
        """
        获取指定URL的HTML内容，并自动解码。

        Args:
            url (str): 目标网页的URL。

        Returns:
            str | None: 解码后的HTML字符串，如果失败则返回None。
        """
        try:
            client = self._get_client()
            response = client.get(url)
            response.raise_for_status()
            if de:
                # 直接在这里解码并返回
                return unescape(response.text)
            else:
                return response.text
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            print(
                f"Error response {e.response.status_code} while requesting {e.request.url!r}."
            )
            return None

    def close(self):
        """
        显式关闭客户端，释放资源。
        """
        if self._client and not self._client.is_closed:
            print("Closing httpx client...")
            self._client.close()


class AllKa:
    def __init__(self, user_id: str = "ad6c8ab0079c1140"):
        # userid 是 每个代理的id这里默认用的是我的
        self.all_ka = []
        self.uid = user_id
        self.zkl = os.getenv("ZKL") or 0.9
        print(f"折扣率是 {self.zkl}")
        self.wb = WebClient()
        self.get_all_ka()

    def get_all_webdata(self):
        # 优先从环境变量读取 API URL，便于在不同环境下替换
        url = os.getenv(
            "PRODUCTS_API_URL",
            "https://172appapi.lot-ml.com/api/Products/NewQuery2?TimeType=0&page=1&OnShop=true&limit=199&IsKuan=0",
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; 2304FPN6DC Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.168 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/35.142857)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            # Authorization 从环境读取，确保敏感信息不写死在代码里
            "Authorization": os.getenv("AUTHORIZATION"),
            "market": os.getenv("MARKET", "xiaomi"),
            "ver": os.getenv("APP_VER", "341"),
            "platform": os.getenv("PLATFORM", "android_app"),
            # 可选：CID 同样从环境读取，以便不同设备/环境复用
            "cid": os.getenv("CID"),
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            print("请求失败")
            print("去检查一下 Cookies 相关吧")
            quit()
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败, 状态码: {response.status_code}")
            quit()


    def get_all_ka(self):
        self.all_ka = []
        all_data = Dict(self.get_all_webdata())

        if not all_data["data"]:
            print("没有获取到数据_001")
            quit("")

        for item in all_data["data"]:
            item_data = Dict()
            item_data["宣传图片"] = item["mainPic"]
            item_data["推广链接"] = (
                f"https://h5.lot-ml.com/h5orderEn/index?pudID={item['sn']}&userid={self.uid}"
            )
            item_data["标题"] = item["productName"]
            item_data["返现类型"] = item["backMoneyType"]

            item_data["运营商"] = item["operator"]

            item_data["返现金额"] = int(item["sPrice"]) * float(self.zkl) // 1
            item_data["返现金额"] = item_data["返现金额"] // 10 * 10
            item_data["归属地"] = item["area"]  # str
            item_data["不发货地区"] = item["disableArea"]  # str

            item_data["规则"] = item["rule"]
            item_data["最小年龄"] = item["age1"]
            item_data["最大年龄"] = item["age2"]

            item_data["通用流量"] = item["tyLiuliangStr"]
            item_data["定向流量"] = item["dxLiuliangStr"]
            item_data["通话时长"] = item["tonghuaStr"]

            item_data["首冲价格"] = item["firstPrice"]

            item_data["更新时间"] = item["publicTime"]

            self.all_ka.append(item_data)

        return self.all_ka


# --- 如何使用 ---
if __name__ == "__main__":
    # # 1. 创建一个实例，可以一直复用
    # web_client = WebClient()

    # # 2. 直接调用方法获取页面，非常简洁
    # print("--- First Request ---")
    # url1 = 'https://h5.lot-ml.com/ProductEn/Index/ad6c8ab0079c1140'
    # html1 = web_client.get_html(url1)

    ka = AllKa()
    print(ka.all_ka)

    # with open('path2.json', 'w', encoding='utf-8') as f:
    #     json.dump(ka.all_ka, f, ensure_ascii=False, indent=4)
