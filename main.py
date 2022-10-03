import requests
import re
import json
import time
import random
import datetime as dt
import os
import threading

# 真实的播放url https://m3u8.zhisongip.com:38741/video/1ef9bb59428975cff6657c5fca7ecc26.m3u8

def get_html(url):

    '''
    $('#playerMainFrame').attr('src','https://dmplayer.suoyou.live/?url='+player_aaaa.url);
    $('#playerMainFrame').load(() => {
        setTimeout(()=>{
            init();
        },80);
    });
    var config = {
        domain: 'https://www.dmxq.fun'
    };
    var state = {
        id: '2670',
        sid: '1',
        nid: '1',
    };
    var MacPlayer = {};
    var ep_title = "";
    :param url:
    :return:
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    r0 = requests.get(url=url, headers=headers).text
    r = r0.replace('/static/js/play.js','https://www.dmxq.fun/static/js/play.js')

    # print(r.text)
    # t = dt.datetime.now().strftime('%Y-%m-%d')
    with open(f'a.html', 'w', encoding='utf-8') as f:
        f.write(r)
    info = re.findall('var player_aaaa=(.*?)</script>', r)[0]
    # print(info)
    json_data = json.loads(info)
    print(json_data)

    # link = json_data['link']
    title = json_data['vod_data']['vod_name']
    print(title)

    url0 = json_data['url']
    video_url = "https://dmplayer.suoyou.live/?url=" + url0
    print(video_url)

    video_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }


    r2 = requests.get(url=video_url, headers=video_headers)
    with open(f"video.html","w", encoding='utf-8') as f:
        f.write(r2.text)
    # print(r2.text)


def get_m3u8():
    # fall_address = https://www.dmxq.fun/vodplay/63014-1-1.html
    # /video/55081476908ef062023623c39bb8d034.m3u8
    # 超能计划 url0 = 'https://m3u8.zhisongip.com:38741/video/3ccbc06458074f6780f7723b1c99041b.m3u8'

    # /video/e654138768a9e88670fb49c217e8cef9.m3u8

    t = '3ccbc06458074f6780f7723b1c99041b'

    # print(len(t))

    # https://cdn.hls.shenglinyiyang.cn/hls/103C6C88266E1312173B3068C7E6E08F38779B0809F89C5B464F230C0481B8FD984E053482DAA1183D877FF8884A5D71A207E2352ACFCBD3A6D08B58DF9F4DADA0F7C9C139154F7889EA6B07?st=ec89_urgCiBxlMm3iz9Eow&e=1664245904

    try:
        headers = {
            'Origin': 'dmplayer.suoyou.live',
            'Host': 'm3u8.zhisongip.com:38741',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        # m3u8_url = f'https://m3u8.zhisongip.com:38741/video/{t}.m3u8'
        m3u8_url = f'https://m3u8.zhisongip.com:38741/video/{t}.m3u8'
        print(m3u8_url)
        m3u8_data = requests.get(url=m3u8_url, headers=headers).text
        print(m3u8_data)
        m3u8_data = re.sub('#E.*','',m3u8_data).split() # 字符串分割，返回列表

        i = 0
        for ts in m3u8_data:
            ts_content = requests.get(url=ts).content
            with open('超能计划.mp4', mode='ab') as f:
                f.write(ts_content)
                i += 1
                # cls()
                print(f"{i} of {len(m3u8_data)} download successful.")
    except:
        print('some error.')
        pass


    print("Movie download sussessful.")


def get_url():
    headers = {
        'Origin': 'dmplayer.suoyou.live',
        'Host': 'cdn.hls.shenglinyiyang.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    url = 'https://cdn.hls.shenglinyiyang.cn/hls/103C6C88266E1312173B3068C7E6E08F38779B0809F89C5B464F230C0481B8FD984E053482DAA1183D877FF8884A5D71A207E2352ACFCBD3A6D08B58DF9F4DADA0F7C9C139154F7889EA6B07?st=ec89_urgCiBxlMm3iz9Eow&e=1664245904'
    r = requests.get(url=url, headers=headers)
    print(r)


# get_html()
# get_m3u8()



if __name__ == '__main__':
    # url = 'https://www.dmxq.fun/vodplay/63014-2-1.html' # fall
    url = 'https://www.dmxq.fun/vodplay/15500-1-1.html' # 毒枭第一季

    get_html(url)
    # get_m3u8()


    # start_time = time.time()
    # t = threading.Thread(target=get_m3u8)
    # t.start()
    # t.join()
    # print(time.time() - start_time)