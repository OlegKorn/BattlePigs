import requests
from bs4 import BeautifulSoup as bs
import re, os, sys, time
import logging
from wget import download
from selenium import webdriver as wd


FORMAT = '%(message)s'

js = '''
let banners = document.querySelectorAll('#content img')
arr_ = []

for (let i=0; i<banners.length; i++) {
    let img = banners[i]['src']
    let country = banners[i]['alt']
    data = img + ':' + country 
    arr_.push(data)
}

return arr_   
'''

path = os.path.abspath(os.path.dirname(sys.argv[0])).replace('\\', '/')

url = 'https://www.flagistrany.ru/azbuka'


class BannerDownloader:

    def __init__(self):
        if not os.path.exists(f'{path}/banners'):
            os.mkdir(f'{path}/banners')
            print(f'Created: {path}/banners')


    def get_soup(self, url):
        session = requests.Session()
        r = session.get(url)
        soup = bs(r.content, 'html.parser')

        return soup
    

    def execute_js_to_get_banners(self):
        try:
            self.driver = wd.Chrome()
            self.driver.get(url)
            time.sleep(7)

            banners = self.driver.execute_script(js)
            self.driver.close()
            print(banners)

            return banners
        
        except Exception as e:
            print(e)
            self.driver.close()


    def write_banners_to_log(self):
        logging.basicConfig(filename=f'{path}/banners/banners.log', level=logging.INFO, format=FORMAT)
        
        try:
            banners = self.execute_js_to_get_banners()

            for banner in banners:
                print(banner)
                logging.info(banner)        
        
        except Exception as e:
            print(e)            


    def download_images(self):
        f = open(f'{path}/banners/banners.log', 'r').readlines()

        num_of_lines = sum(1 for _ in f)
        n = 0

        try: 
            for _ in f:
                _ = _.strip()
                
                url = _.split('g:')[0] + 'g'
                title = _.split('g:')[1].replace(' ', '_')

                session = requests.Session()
                try:
                    img_r_ = session.get(url)
                except Exception as e:
                    print(e)
                    continue 

                con = img_r_.content

                file_name = f'{path}/banners/{title}.jpg'
                
                outf = open(file_name, "wb")
                outf.write(con)
                outf.close()

                print(f'{title} - {n} from {num_of_lines}') 
                
                n += 1                
                
        except Exception as e:
            raise(e)
            pass 



bd = BannerDownloader()
# bd.write_banners_to_log()
bd.download_images()


