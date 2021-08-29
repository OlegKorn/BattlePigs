import sys
from PIL import Image, ImageDraw
import os
import random


class Pig:
    '''
    Creates pics with wuotation marks
    '''

    def __init__(self):
        # define the path where your file is
        self.path = os.path.abspath(os.path.dirname(sys.argv[0])).replace('\\', '/')

        # starting points of flag
        self.start_point_x = 0
        self.start_point_y = 0

        # define colors
        self.WHITE = '#FFFFFF'
        self.BLUE_RU = '#0033A0'
        self.RED = '#DA291C'

        self.BLUE_UKR = '#005BBB'
        self.YELLOW = '#FFD500'

        self.QUOTATION_COLOR = '#ddd'


    def draw_quotation_mark(self, draw_obj, w, h):
        start_point_x = int(w * 0.7)
        start_point_y = int(h / 2)

        x2 = start_point_x + int(w * 0.055)
        y2 = start_point_y - int(h * 0.015)

        x3 = w
        y3 = 0

        x4 = w
        y4 = h

        x5 = start_point_x + int(w * 0.055)
        y5 = start_point_y + int(h * 0.03)
                    
        xy = [
            (start_point_x, start_point_y), 
            (x2, y2), 
            (x3, y3), 
            (x4, y4),
            (x5, y5)
        ]

        draw_obj.polygon(xy, fill=self.QUOTATION_COLOR)


    def draw_russian_banner(self, draw_obj, w, h):
        '''
        ImageDraw.polygon(xy, fill=None, outline=None)

        Draws a RUS banner in the upper left corner
        Params:
          -- xy – Sequence of either 2-tuples like [(x, y), (x, y), ...] or numeric values like [x, y, x, y, ...].
          -- outline – Color to use for the outline
          -- fill – Color to use for the point
        '''

        # flag stripes params
        stripe_w = int(w * 0.35)

        if w > h:
            stripe_h = int(h * 0.1)
        if h > w:
            stripe_h = int(w * 0.1)

        stripe_1 = [(self.start_point_x, self.start_point_y), (stripe_w, stripe_h)]
        stripe_2 = [(self.start_point_x, stripe_h), (stripe_w, stripe_h * 2)]
        stripe_3 = [(self.start_point_x, stripe_h * 2), (stripe_w, stripe_h * 3)]

        draw_obj.rectangle(stripe_1, self.WHITE)
        draw_obj.rectangle(stripe_2, self.RED)
        draw_obj.rectangle(stripe_3, self.BLUE_RU)


    def draw_ukrainian_banner(self, draw_obj, w, h):
        '''
        ImageDraw.polygon(xy, fill=None, outline=None)

        Draws a UKR banner in the upper left corner
        Params:
          -- xy – Sequence of either 2-tuples like [(x, y), (x, y), ...] or numeric values like [x, y, x, y, ...].
          -- outline – Color to use for the outline
          -- fill – Color to use for the point
        '''

        # flag stripes params
        stripe_w = int(w * 0.35)
        
        if w > h:
            stripe_h = int(h * 0.15)
        if h > w:
            stripe_h = int(w * 0.15)

        stripe_1 = [(self.start_point_x, self.start_point_y), (stripe_w, stripe_h)]
        stripe_2 = [(self.start_point_x, stripe_h), (stripe_w, stripe_h * 2)]

        draw_obj.rectangle(stripe_1, self.BLUE_UKR)
        draw_obj.rectangle(stripe_2, self.YELLOW)


    def insert_flag(self, im=None, path=None, w=None, h=None):
        # flag files
        flags = os.listdir(f'{self.path}/banners')
        flag = random.choice(flags)
        print(flag)
        
        im_to_paste = Image.open(f'{self.path}/banners/{flag}')

        resized_flag = im_to_paste.resize((110, 55))

        if (w != 0 and h):
            resized_flag = im_to_paste.resize((int(w), int(h*0.3)))

        if (w == 0 and h):
            resized_flag = im_to_paste.resize((0, int(h * 0.3)))    
        
        im.paste(resized_flag)
        im.save(f'{self.path}/FLAG.jpg')
        

    def main(self):
        for pic in os.listdir(self.path)[0:10]:
            number_of_files = len(os.listdir(self.path))

            if (not pic.endswith('.py')) and (not pic.endswith('.log')):
                title = (pic.split('.')[0] + '_done').strip()

                with Image.open(pic) as im:
                    draw = ImageDraw.Draw(im)
                    print()
                    print(im.width, im.height)

                    '''
                    self.draw_quotation_mark(draw, im.width, im.height)
                    self.draw_ukrainian_banner(draw, im.width, im.height)
                    im.save(f'UKR_{title}.jpeg')                    
                    print(f'Created: UKR_{title}.jpeg')
                    
                    '''
                    self.draw_quotation_mark(draw, im.width, im.height)
                    self.draw_russian_banner(draw, im.width, im.height)
                    im.save(f'RUS_{title}.jpeg')
                    print(f'Created: RUS_{title}.jpeg')
                    
                    # insert flag
                    self.insert_flag(im, self.path, im.height)



p = Pig()
p.main()
