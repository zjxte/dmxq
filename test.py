import time
import re
import requests
import threading
import concurrent.futures

# 超能计划  https://www.dmxq.fun/vodplay/8062-1-1.html



def get_m3u8_list(url):
    urls = []

    headers = {
        'Origin': 'dmplayer.suoyou.live',
        'Host': 'm3u8.zhisongip.com:38741',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    r = requests.get(url=url, headers=headers).text
    m3u8_data = re.sub('#E.*', '', r).split()
    return m3u8_data

def download_videos(m3u8_url):
    # 下载单条视频
    movie = requests.get(url=m3u8_url).content
    with open('movie.mp4', 'ab') as f:
        f.write(movie)

if __name__ == '__main__':

    url = 'https://m3u8.zhisongip.com:38741/video/1ef9bb59428975cff6657c5fca7ecc26.m3u8'
    # x = get_m3u8_list(url)
    # print(x)

    t1 = time.time()

    movie_list = get_m3u8_list(url)
    # print(len(movie_list))
    for i in range(1, len(movie_list)):
        t = threading.Thread(target=download_videos, args=(movie_list[i],))
        t.start()
        print(f'{i} of {len(movie_list)} downloaded')


    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(download_videos, movie_list)

    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
    t.join()