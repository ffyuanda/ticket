import json


url = 'https://www.cmskchp.com/sailingsJson'

cookies = {
    '__jsluid_s': 'a6134e735a9850a826823be85f9fa053',
    'cloudwise_client_id': 'cb2dfc97-d464-a159-985b-f2bcdbeb31a5',
    'SESSION': 'bc9538018e4e2f61a4bcf9799c673dde62dc6bb7',
    'PLAY_SESSION': '"e5b80c4829d19f2efd0a6331c5fea5b12e4e54e8-login_user_id=90ff0b18d2ed1131c88f394d8a8cfd76&login_user_type=member"',
    'session_graphic_code_order': 'a5ccd8f36cb1931efba3839cd69856b8a58d668b1f51f1a5f99e78546f0a5df42142ff548c8d3c3f64995605585e833c',
    'redirect_path': '%2ForderDetail%3ForderNo%3D1237998926',
    'siteResJson': '%7B%22userType%22%3A%22LTP001%22%2C%22sailingType%22%3A%220%22%2C%22toDate%22%3A%222022-05-28%22%2C%22startSiteName%22%3A%22%E6%B7%B1%E5%9C%B3%E8%9B%87%E5%8F%A3%22%2C%22endSiteName%22%3A%22%E9%A6%99%E6%B8%AF%E6%9C%BA%E5%9C%BA%22%2C%22backDate%22%3A%22%22%2C%22lineId%22%3A%22SK-HKA%22%2C%22startSite%22%3A%22SK%22%2C%22endSite%22%3A%22HKA%22%2C%22flightId%22%3A%224%22%2C%22flightName%22%3A%22%E5%8A%A0%E6%8B%BF%E5%A4%A7%E8%88%AA%E7%A9%BA%22%2C%22flightNo%22%3A%22AC008%22%2C%22flightDate%22%3A%222022-05-28%22%2C%22flightHours%22%3A%2219%22%2C%22flightMinute%22%3A%2200%22%2C%22code%22%3A%22AC%22%2C%22flightCode%22%3A%22AC%22%7D',
    'CW_Start': '1652196957720',
    'session_graphic_code': '7d63ffc1393c9a8761c0c65651a83d84056bb7db83ecf3c81ee8867860301da22142ff548c8d3c3f64995605585e833c',
    'page_uri': '/sailings',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.cmskchp.com',
    'Referer': 'https://www.cmskchp.com/sailings',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

payload = {
    'siteResJson': '{"startSite":"SK","endSite":"HKA","toDate":"2022-05-28"}',
}

template_payload = json.loads(payload['siteResJson'])
