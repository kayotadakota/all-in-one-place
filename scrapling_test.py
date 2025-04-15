import requests

from scrapling.fetchers import Fetcher

page = Fetcher.get('https://www.cmoa.jp/newrelease/schedule/')
links = page.css('div.h_long_thum_w_4.volume > a')
total_pages = len(page.css('div.es-carousel li'))


def get_titles(payload: dict):
    new_titles = []

    try:
        page = Fetcher.get('https://www.cmoa.jp/newrelease/schedule/', params=payload, timeout=3)
        links = page.css('div.h_long_thum_w_4.volume > a')
        #volumes = page.css('div.vol_num::text').re(r'^1(?:-\d+)?\D.*$')
        #volumes = [vol.parent.attrib['href'] for vol in page.css('div.vol_num') if vol.text.re(r'^1(?:-\d+)?\D.*$')]
        #images = [f'https:{vol.parent.parent.find('img').attrib['src']}' for vol in page.css('div.vol_num') if vol.text.re(r'^1(?:-\d+)?\D.*$')]

        for tag in page.css('div.vol_num'):
            if tag.text.re(r'^1(?:-\d+)?\D.*$'):
                url = tag.parent.parent.find('img').attrib['src']
                title_id = tag.siblings[2].attrib['href'].re_first(r'/title/(\d+)/')
                new_titles.append((url, title_id))
                download_img(url, title_id)
                


        
        #new_titles.extend([f'https://cmoa.jp{vol.parent.attrib['href']}' for vol in volumes])
        # images = page.css('div.h_long_thum_w_4.volume img')

        # for link, vol, img in zip(links, volumes, images):
        #     if re.search(r'^1(?:-\d+)?\D.*$', vol.text):
        #         new_titles.append(f'https://cmoa.jp{link.attrib['href']}')
        #         title_id = re.search(r'/title/(\d+)/', link.attrib['href'])
        #         await download_img(img.attrib['src'], title_id.group(1)) 

    except Exception as ex:
        print(f'Unexpected error has occured: {ex}')

    return new_titles


def download_img(url: str, name: str):
    try:
        with open(f'images/{name}.jpg', 'wb') as img:
            res = requests.get(f'https:{url}', timeout=3)
            for chuck in res.iter_content(100000):
                img.write(res.content)

    except Exception as ex:
        print(f'Unexpected error has occured: {ex}')


def main():
    results = []

    for page in range(1, 10):
        payload = {'page': page}
        results.append(get_titles(payload))

    print(results)

if __name__ == '__main__':
    main()