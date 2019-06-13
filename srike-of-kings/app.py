#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   app.py
@Time    :   2019/06/11 20:26:04
@Author  :   Jason.Li
@Version :   1.0
@Contact :   initiallht@163.com
@Desc    :   爬取游戏王者农药 - 现存的英雄头像及皮肤
@Notice  :   代码千万行 · 注释第一行 · 代码不规范 · 同事两行泪
'''

# here put the import lib
import requests
import os

'''
爬取前通过页面观察分析，保存重要的url
https://pvp.qq.com/
https://pvp.qq.com/web201605/herolist.shtml
/web201605/js/herolist.json
http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/506/506-bigskin-1.jpg
http://game.gtimg.cn/images/yxzj/img201606/heroimg/506/506.jpg
'''

# 下载并存储图片
def save_url_img(url_link, file_path, file_name):
    request_result = requests.get(url_link)
    if request_result.status_code == 200:
        # 将图片保存下来，并以"英雄名称_皮肤序号"方式命名
        with open(file_path + file_name, 'wb') as f:
            f.write(request_result.content)
        print('save file success: {}{}'.format(file_path, file_name))
        return True
    else:
        print('save file failed, img is not exist: {}'.format(url_link))
        return False


def download_hero_img():

    # 包含英雄名称信息的URL
    url = 'http://pvp.qq.com/web201605/js/herolist.json'
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
    response = requests.get(url, headers=head)
    hero_list = response.json()
    # 提取英雄名字及对数字
    hero_name = list(map(lambda x:x['cname'], hero_list)) 
    hero_number = list(map(lambda x:x['ename'], hero_list))
    
    num = 0
    # 逐一遍历英雄
    for i in hero_number:
        # 英雄头像的URL链接
        hero_head_link = 'http://game.gtimg.cn/images/yxzj/img201606/heroimg/'+str(i)+'/'+str(i)+'.jpg'
        save_url_img(hero_head_link, 'hero_head/', hero_name[num] + '.jpg')

        # 遍历皮肤，上限为20
        for sk_num in range(20):
            if sk_num == 0:
                continue
            # 英雄皮肤的URL链接
            hero_skin_link = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(i)+'/'+str(i)+'-bigskin-'+str(sk_num)+'.jpg'
            result = save_url_img(hero_skin_link, 'hero_skin/', hero_name[num] + str(sk_num) + '.jpg')
            # 返回错误则表示皮肤不存在，不继续进行遍历
            if result == False:
                break

        num = num + 1

    print('down load all hero img !')

# 检查文件夹是否存在，如不存在则创建文件夹
def check_path(path):

    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 

        print('create file [{}] success.'.format(path))
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print('file [{}] exists.'.format(path))
        return False

if __name__ == '__main__':

    check_path('hero_head')
    check_path('hero_skin')
    download_hero_img()