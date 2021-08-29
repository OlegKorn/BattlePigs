import requests
from bs4 import BeautifulSoup as bs
import re, os, sys, time
import logging
from wget import download
from selenium import webdriver as wd


FORMAT = '%(message)s'

js = '''
let p = document.querySelectorAll('.img-responsive')
arr_ = []

for (let i=0; i<p.length; i++) {
    let pig = p[i]['src']
    let title = p[i]['alt']
    s = pig + ':' + title 
    arr_.push(s)
}

return arr_   
'''

path = os.path.abspath(os.path.dirname(sys.argv[0])).replace('\\', '/')
url = 'https://all-free-download.com/free-photos/pig-photos.html'


class PigDownloader:

    def get_soup(self, url):
        session = requests.Session()
        r = session.get(url)
        soup = bs(r.content, 'html.parser')

        return soup
    

    def download_images(self):
       
        f = open(f'{path}/pigs.log', 'r').readlines()

        num_of_lines = sum(1 for _ in f)
        n = 0

        forbidden_symbols = ('*,<>:\'\\"/\|?=')

        try: 
            for _ in f:
                _ = _.strip()
        
                session = requests.Session()
                try:
                    img_r_ = session.get(_)
                except Exception as e:
                    print(e)
                    continue 

                con = img_r_.content

                file_name = f'{path}/{artist_name}/{title}_{n}.jpg'
                
                outf = open(file_name, "wb")
                outf.write(con)
                outf.close()

                print(f'{img_to_print}  :  {title}  ->  {n} from {num_of_lines}') 
                
                n += 1                
                

        except Exception as e:
            raise(e)
            pass 


    def execute_js_to_get_pigs(self):
        try:
            self.driver = wd.Chrome()
            self.driver.get(url)
            time.sleep(7)

            pigs = self.driver.execute_script(js)
            self.driver.close()
            print(pigs)

            return pigs
        
        except Exception as e:
            print(e)
            self.driver.close()


    def write_pigs_to_log(self):
        logging.basicConfig(filename='pigs.log', level=logging.INFO, format=FORMAT)
        
        try:
            pigs = self.execute_js_to_get_pigs()

            for pig in pigs:
                print(pig)
                logging.info(pig)        
        
        except Exception as e:
            print(e)            



p = PigDownloader()
# p.download_images()
p.write_pigs_to_log()


