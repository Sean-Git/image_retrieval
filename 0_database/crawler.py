# -*- coding: utf-8 -*-
__author__ = 'sean.wang'

from selenium import webdriver
import logging
import os
import shutil
import time
import urllib

class Crawler:

    def __init__(self):
        logging.basicConfig(level = logging.INFO,
                            format = '[%(levelname)s] %(message)s',
                            filename = 'log',
                            filemode = 'w')
        self.search_url_lst = ['http://pic.sogou.com/pics?query=%CA%D6%BB%FA&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421762128&w=05009900&sut=2393&sst0=1421762158069',
                               'http://pic.sogou.com/pics?query=%B5%E7%C4%D4&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421758507&w=05009900&sut=4952&sst0=1421762132276',
                               'http://pic.sogou.com/pics?query=%CB%D1%BA%FC&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421762154&w=05009900&sut=2336&sst0=1421762219604',
                               'http://pic.sogou.com/pics?query=%CA%E9&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421762216&w=05009900&sut=2945&sst0=1421762249580',
                               'http://pic.sogou.com/pics?query=%B1%CA&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421762246&w=05009900&sut=1102&sst0=1421762279868',
                               'http://pic.sogou.com/pics?query=%CB%AE%B1%AD&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421766513&w=05002100&oq=shuibei&ri=0&sourceid=sugg&sut=2923&sst0=1421767037907',
                               'http://pic.sogou.com/pics?query=%C5%E8%BE%B0&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767034&w=05002100&oq=penjing&ri=1&sourceid=sugg&sut=3289&sst0=1421767075547',
                               'http://pic.sogou.com/pics?query=%C6%FB%B3%B5&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767093&w=05009900&sut=1626&sst0=1421767107603',
                               'http://pic.sogou.com/pics?query=%D2%CE%D7%D3&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767133&w=05009900&sut=1871&sst0=1421767143321',
                               'http://pic.sogou.com/pics?query=%BD%A1%BF%B5&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767188&w=05009900&sut=2031&sst0=1421767225770',
                               'http://pic.sogou.com/pics?query=%C3%C0%CA%B3&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767222&w=05009900&sut=3451&sst0=1421767265827',
                               'http://pic.sogou.com/pics?query=%D2%BD%C1%C6&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767262&w=05009900&sut=2720&sst0=1421767284281',
                               'http://pic.sogou.com/pics?query=%C4%B8%D3%A4&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767281&w=05009900&sut=2496&sst0=1421767305432',
                               'http://pic.sogou.com/pics?query=%BD%CC%D3%FD&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767302&w=05009900&sut=2769&sst0=1421767325729',
                               'http://pic.sogou.com/pics?query=%C2%C3%D3%CE&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767322&w=05009900&sut=4961&sst0=1421767351840',
                               'http://pic.sogou.com/pics?query=IT+%BF%C6%BC%BC&p=&dp=&di=2&_asf=pic.sogou.com&_ast=1421767348&w=05009900&sut=2613&sst0=1421767378404']
        self.xpath = '//div[@id="imgid"]/ul/li/a/img'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.img_url_dic = {}

    def release(self):
        del self.search_url_lst
        del self.xpath
        self.driver.close()
        del self.img_url_dic

    def launch(self):
        driver = self.driver
        img_url_dic = self.img_url_dic
        
        c = 0
        for search_url in self.search_url_lst:
            logging.info('crawling url NO.%d - %s' % (c, search_url))
            m = 0
            
            # 判断存放图片的文件夹是否存在
            path = './%s/' % str(c)
            if os.path.exists(path):
                shutil.rmtree(path) # 递归删除非空文件夹
            os.mkdir(path)                
                
            driver.get(search_url)
            # 模拟滚动窗口以浏览更多图片
            pos = 0
            for i in range(10):
                pos += i*400 # 每次下滚500
                js = "document.documentElement.scrollTop=%d" % pos
                driver.execute_script(js)
                time.sleep(1)           
                for element in driver.find_elements_by_xpath(self.xpath):
                    img_url = element.get_attribute('src')
                    #img_desc = element.get_attribute('data-desc')
                    img_desc = ''

                    # 保存图片到指定路径
                    if img_desc != None and img_url != None and not img_url_dic.has_key(img_url):
                        m += 1
                        # 标题描述预处理
                        img_desc = self.filter_filename_str(img_desc)
                        img_url_dic[img_url] = c
                        ext = img_url.split('.')[-1]

                        #保存图片数据
                        data = urllib.urlopen(img_url).read()
                        filename = '%d_%d%s.%s' % (c, m, img_desc, ext) 
                        f = open(path + filename, 'wb')
                        f.write(data)
                        f.close()
                        logging.info('img NO.%d saved: %s - %s' % (m, img_url, img_desc))
            c += 1

    def filter_filename_str(self, s):
        invalid_set = ('\\','/',':','*','?','"','<','>','|',' ')
        for i in invalid_set:
            s = s.replace(i, '_')
        return s
                         
        
    
if __name__ == '__main__':
    crawler = Crawler()
    crawler.launch()
    crawler.release()
