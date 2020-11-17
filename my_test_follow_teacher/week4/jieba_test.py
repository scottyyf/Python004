#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: jieba_test.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import jieba
import time
import threading


def test():
    jieba.load_userdict('jieba.txt')
    jieba.add_word('百度地图')
    strings = ['我来自即可大学', 'i am a student, bitch',
               '百度地图导航到了武汉大学食堂1', '莫西莫西你的大大的快点八嘎牙路']

    for i in strings:
        result = jieba.cut(i)
        print('/'.join(list(result)))

    for i in strings:
        result = jieba.cut(i, cut_all=True)
        print('/'.join(list(result)))

    result = jieba.cut('新冠百度地图导航到了武汉大学食堂1')
    print('/'.join(list(result)))

    print(jieba.lcut('丰田太省了'))
    print(jieba.lcut('我们中出了一个叛徒', HMM=False))


import jieba.analyse
from pprint import pprint


def test1():
    jieba.add_word('猎狐行动')
    jieba.load_userdict('jieba.txt')
    text = '''
    当地时间28日，美国司法部和联邦调查局（FBI）宣布对8名在美国参与“猎狐行动”的人员提起诉讼，其中5人当天上午被捕，另外3
    人据信在中国。华盛顿声称，北京“非法代理人”在美国境内执法，监视、骚扰、威胁美国公民及永久居民。


新闻发布会截图

“中国执法机关严格根据国际法开展对外执法合作，充分尊重外国法律和司法主权，依法保障犯罪嫌疑人合法权益，有关行动无可非议。”中国外交部发言人汪文斌在29
日的例行记者会上批驳美方无视基本事实，对中方追逃追赃工作进行污蔑。根据FBI
局长克里斯托弗·雷的说法，这是美方首次针对参与中国“猎狐”行动的人员提起诉讼，《华尔街日报》将其美化成华盛顿为打击中方“不当执法行动”开辟了一条“新战线”。但在29日接受《环球时报》记者采访的中国学者看来，为了打“政治牌”而包庇这些犯罪嫌疑人，美国的做法不仅会损害自身的法律体系，同时也将与中国的司法合作引向毒化的方向。

被指控是“非法代理人”

据美国《华尔街日报》29日报道，5人被捕的地点分别是纽约州、新泽西州和加利福尼亚州。香港《南华早报》称，被捕者中有2
人是美国公民（包括一名归化入籍者），其中一人为私家侦探，另外3人是拥有美国永居权的中国公民。美国共起诉8
人，他们被控作为“中国非法代理人”在美国行动，或将面临最高5年监禁的刑期，其中6人还面临共谋跨州和国际跟踪相关指控。在28
日举行的网络新闻发布会上，美国司法部负责国家安全事务的助理部长德默斯自夸说，通过这次指控，美方“把‘猎狐行动’反转了过来，猎手变成猎物，追捕者变成被追捕者”。


▲“猎狐行动”是中央反腐败协调小组部署的“天网行动”的重要组成部分。截至10月20日，共从67个国家和地区成功劝返各类境外逃犯634
名。其中，配合缉捕“百名红通”逃犯16名，协助有关部门缉捕职务犯罪外逃人员50名，缉捕海关走私犯罪境外逃犯31名。

《华尔街日报》报道说，纽约东区联邦地区法院28日公布了长达43页的刑事起诉书，里面描述了上述被告在2016年至2019
年试图采取“发恐吓信”“网络骚扰”等手段向一名住在新泽西州的中国公民施压、要求他返回中国的细节。《纽约时报》称，司法部官员并未透露“猎狐行动”目标的具体身份，只是说他们“需要保护”。《华盛顿邮报》说，中国“猎狐行动”的对象据信多是中国政府前官员，他们可能在出国前从自己的职位中获得可观的利益。

“猎狐行动”是中国公安机关缉捕在逃境外经济犯罪嫌疑人专项行动代号。公开资料显示，自2014年行动启动以来，中方从120
多个国家和地区抓获外逃经济犯罪嫌疑人6000余名，其中缉捕“百名红通”外逃犯罪嫌疑人60
名。“我国的追逃行动都是公开的，而且对藏匿在没有引渡条约的国家的犯罪嫌疑人，我们采取的主要方式是劝服。”中国社科院美国问题专家吕祥29
日对《环球时报》记者说，这是一种非常温和的方式，我国的追逃行动不会有触犯当地法律的情况出现。

环球时报驻美国特约记者 郑 可 环球时报记者 范凌志 白云怡 陈青青 任 重
    '''
    jieba.analyse.set_stop_words('stopwords.txt')
    tfidf = jieba.analyse.extract_tags(text, topK=15, withWeight=True)
    pprint(tfidf)

    # textRank = jieba.analyse.textrank(text, topK=5, withWeight=True)
    # pprint(textRank)


test1()
