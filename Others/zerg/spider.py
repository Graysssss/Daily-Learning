'''
This is a simple zerg
没有什么面向对象的思想
复用性为0
'''
import re
from urllib import request


class Spider():
    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        '''
        定位符：唯一标示性标签 接近于提取数据的标签
        '''
        root_html = re.findall(Spider.root_pattern, htmls)

        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)

        return anchors

    def __refine(self, anchors):
        '''
        数据精炼
        '''
        l = lambda anchor: {'name': anchor['name'][0].strip(), 'number': anchor['number'][0]}
        return map(l, anchors)

    def __sort(self, anchors):
        '''
        排序
        '''
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        '''
        种子函数 提取数字
        '''
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        '''
        加入排名的显示函数
        '''
        for rank in range(0, len(anchors)):
            print('rank ' + str(rank + 1) + ' : ' + anchors[rank]['name'] +
                  '     ' + anchors[rank]['number'])

    def go(self):
        '''
        入口主方法
        '''
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
