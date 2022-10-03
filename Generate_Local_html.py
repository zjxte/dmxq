import requests
import re
import json
from lxml import etree

def get_allNeflix(page):

    url = f'https://www.dmxq.fun/label/netflix/page/{page}/pjax/YES.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    r = requests.get(url=url, headers=headers)

    html = etree.HTML(r.text)
    score_list = html.xpath('//div[@class="module"]/div[2]/div/a/div/div[2]/text()')

    scores = []
    for score in score_list:
        s = score.replace('豆瓣:','').replace('分','')
        scores.append(float(s))
    titles = html.xpath('//div[@class="module"]/div[2]/div/a/div[2]/div/text()')
    links = []
    short_links = html.xpath('//div[@class="module"]/div[2]/div/a/@href')
    for link in short_links:
        links.append("https://www.dmxq.fun" + link)


    movies = {
        "pages": page,
        "scores": scores,
        "titles": titles,
        "links": links
    }
    print(movies)


def get_html(url):
    # url = f'https://www.dmxq.fun/vodplay/15499-1-{url}.html' # 毒枭第一季
    url = f'https://www.dmxq.fun/vodplay/15499-1-{url}.html' #超感猎杀第一季
    # print(url)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    r = requests.get(url=url, headers=headers)
    aaaa = re.findall('var player_aaaa=(.*?)</script>', r.text)[0]
    json_aaaa = json.loads(aaaa)
    mov_title = json_aaaa['vod_data']['vod_name']
    aaaa_script = '<script type="text/javascript">var player_aaaa=' + aaaa + '</script>'
    ep_title = re.findall('var ep_title = "(.*?)";', r.text)[0]
    title = re.findall('document.title = (.*?);', r.text)[0]
    var_ep_title = f'var ep_title = "{ep_title}";'
    doc_title = f'document.title ={title};'.replace('免费在线观看-大米星球','')
    id = json_aaaa['id'] #
    sid = json_aaaa['sid'] #
    nid = json_aaaa['nid'] # 第几集

    # print(id, sid, nid)

    with open('template.text', 'r') as temp:
        template = temp.read()

        template= template.replace('replace_script', aaaa_script)
        template = template.replace('replace_ep_title', var_ep_title)
        template = template.replace('replace_document_title', doc_title)

        template = template.replace('replace_id', str(id))
        template = template.replace('replace_sid', str(sid))
        template = template.replace('replace_nid', str(nid))

        template = template.replace('replace_title', ep_title)


        # print(template)

    with open(f'{ep_title}.html','w',encoding='utf-8') as f:
        f.write(template)
        print(f'{ep_title} has been downloaded, {url}')

if __name__ == '__main__':
    for i in range(1,11):
        get_html(i)

    # for i in range(1,6):
    #     get_allNeflix(i)
