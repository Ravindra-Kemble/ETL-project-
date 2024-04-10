import requests
import re

def get_all_plaza_ids():
    cookies = {
        'ASP.NET_SessionId': '5pj4cqjn33ufmhka3lzbpwhk',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        # 'Cookie': 'ASP.NET_SessionId=5pj4cqjn33ufmhka3lzbpwhk',
        'Origin': 'https://tis.nhai.gov.in',
        'Referer': 'https://tis.nhai.gov.in/tollplazasataglance.aspx?language=en',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = "{'TollName':''}"

    response = requests.post(
        'https://tis.nhai.gov.in/TollPlazaService.asmx/GetTollPlazaInfoGrid',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    l = re.findall('javascript:TollPlazaPopup\(\d+\)', response.text)
    ids = [int(re.findall('\d+', str_)[0]) for str_ in l]
    
    return ids


if __name__ == '__main__':
    print(get_all_plaza_ids())