import re
import requests

from bs4 import BeautifulSoup

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'cache-control': 'max-age=0',
    'connection': 'keep-alive',
    'host': 'www.cmoa.jp',
    'referer': 'https://www.cmoa.jp/newrelease/schedule/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-full-version': '"135.0.7049.42"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '',
    'sec-ch-ua-platform': 'Windows',
    'sec-ch-ua-platform-version': '10.0.0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-request': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

zxc = '_ga=GA1.2.103217865.1741776744; _tt_enable_cookie=1; _ttp=01JP4ZQV919AADDXJ5KGZADE5G_.tt.1; \
                    _ebtd=1.11q6buuhh6u.1721553328; FPID=FPID2.2.LxxDmPV10k9JJdi93%2F31IwM%2BFfXGNmD%2F9b9UGh8Dggc%3D.1741776744; \
                    FPAU=1.2.738732563.1741776746; _yjsu_yjad=1741776744.22c9b62a-7b47-4b83-acea-aac0fead4fd9; _cmoa_web_=1; \
                    _gcl_au=1.1.1593953801.1743706354; snexid=5f1f5279-8c7b-4218-982d-82155514bd49; \
                    __lt__cid=4fc2b00e-c7a1-4d85-884f-451fb085a3cd; __lt__cid.c366e723=4fc2b00e-c7a1-4d85-884f-451fb085a3cd; \
                    _im_vid=01JQYFZ1NMPNRSYWJ7Y3WG6DXG; nmid=CiARC2fu2UNl7BbvHaDuAg==; krt.vis=sq8GUcwS05MmwaI; krt.lnd=17; \
                    sess_99673124=member.cmoa.jp_20250403215742325HwdRy; _sol_new_coupon_13282f8=20250226memberregistration; \
                    _cmoa_login_session_token_=2025-04-03T18%3A58%3A07Z7EOMyg; mhuid=b7b3695d89ac1cdd72475d2f3d30e11d; \
                    _gender_=MALE; _items_in_cart_=1; PAGE=0; _binb_ret_url_=https%3A%2F%2Fwww.cmoa.jp%2Fsearch%2Fresult%2F%3Fauthor_id%3D0000003659%26sort%3D14%23ti1101065487; \
                    BIGipServer~I090~Pool_Cmoa_App_On=rd90o00000000000000000000ffffac101041o80; \
                    BIGipServer~I090~Pool_Cmoa_Static_On=rd90o00000000000000000000ffffac101003o80; \
                    FPLC=oOnUl5DxTKhXdF6fHaPhH0PxN8R9stLu%2BERAvMR%2BfbhZXr1jwU6wN3TUzcYTPGOGqM%2BaDVnTpR6qfXzxnzqLFcp5p%2Fj%2FPal1YvIsQeoyREOaaRjtcqK2ySiekLrpNA%3D%3D; \
                    _notice_=3; __lt__sid=96d3cd14-b8cb79bd; __lt__sid.c366e723=96d3cd14-b8cb79bd; \
                    TS017350e1=01f277dc080895a5f02e2e81fd5260373e8f1d51cd6ea5ff9c63b6a0308764fd85809b4c73562c136b0f58b12e31a900b6dd08c30c; \
                    _pte_1h_cook=74; TS016f3b3b=01f277dc080895a5f02e2e81fd5260373e8f1d51cd6ea5ff9c63b6a0308764fd85809b4c73562c136b0f58b12e31a900b6dd08c30c; \
                    community_session=25VlKLZlTNdhXQWt5UiUwtuNxWhO6ROJBR4unu41; \
                    BIGipServer~I090~Pool_Cmoa_Community_Renewal_Reverseproxy_On=rd90o00000000000000000000ffffac101129o80; \
                    COMMUNITY-XSRF-TOKEN=1S2G7MH2zCji3m76rcXElej1TMUxuSlReWaZ0zbe; \
                    _ssid_=dzflugUBxLOYZqXMS%2FpNKRYI4BStqIdkEA7WMVGcywiScnniW%2Fl32ErnDTz0FhnKOISj6Te%2Ba1o8odFd4mniA5mTKZey8XeNJbKEbz8l02saYD2%2BMMSU5M8eRsTVipfTDnhQIzAALSJQGIyRdCdWmRUIkHvHiNYnHHMs4Qo%2BgJxdA1F%2Fj6rnFROJlDUVT9J9DJt3iJjVg4UinyCKOf1C9A%3D%3D; \
                    IDS_CMOA=100003198050001%2C100003194090001%2C100003189380001%2C100003188800001%2C100002882340001%2C111010259190001%2C111010654870001%2C100002679970001%2C100003190500001%2C100003107220001%2C100002957750001%2C100002386950001%2C100002862090001%2C100002862080001%2C111010650700001; \
                    TS01b31523=01f277dc085140d626455aa5af3aee3b57cda0636093578df70dffa33a0bfa762b47808e1f85b455f9aaa63914248f7bdc8b10229b; \
                    _ga_19WGWEVP54=GS1.2.1744201345.9.1.1744202043.0.0.1403296413; ttcsid_C6EQC823RRRB95OGA5GG=1744201345634.1.1744202044348; \
                    FPGSID=1.1744201346.1744202044.G-19WGWEVP54.Z3lfaniGKJxlV8UhmxmVbw; ttcsid=1744201345635.1.1744202047403; \
                    ttcsid_CIAJ9IJC77U9G5MUVAMG=1744201348227.1.1744202047765; ttcsid_CLP7MQBC77UCSDME0QDG=1744201348231.1.1744202047765; \
                    ttcsid_CT7VCBRC77U74JDR0MR0=1744201348233.1.1744202047766'


def gather_new_titles(session, page_number):
    new_titles = []
    payload = {'page': page_number}
    response = session.get('https://www.cmoa.jp/newrelease/schedule/', params=payload)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    volumes = soup.select('div.vol_num')
    links = soup.select('div.h_long_thum_w_4.volume > a')
    imgs = soup.select('div.h_long_thum_w_4.volume img')
    # re.search(r'/1(?:-\d+)?/', link['href']

    for link, vol, img in zip(links, volumes, imgs):
        if re.search(r'^1(?:-\d+)?\D.*$', vol.text):
            new_titles.append(f'https://www.cmoa.jp{link['href']}')
            title_id = re.search(r'/title/(\d+)/', link['href'])
            download_img(session, img['src'], title_id.group(1))

    return new_titles


def download_img(session, url, name):
    try:
        with open(f'images/{name}.jpg', 'wb') as img:
            img.write(requests.get(f'https:{url}', timeout=1).content)
            #img.write(session.get(f'https:{url}', timeout=1).content)
    except Exception as ex:
        print(f'Unexpected error has occured: {ex}')


def make_request():
    results = []
    session = requests.Session()
    session.headers.update(HEADERS)
    response = session.get('https://www.cmoa.jp/newrelease/schedule/', timeout=3, params={'page': '1'})
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = len(soup.select('div.es-carousel li'))

    results.extend(gather_new_titles(session, 1))

    for page_number in range(2, 3):
        new_titles = gather_new_titles(session, page_number)
        results.extend(new_titles)

    for result in results:
        print(result)

    print(len(result))

if __name__ == '__main__':
    make_request()