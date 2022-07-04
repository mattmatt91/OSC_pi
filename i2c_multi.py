from pickle import TRUE
from stringprep import in_table_c21_c22
import board
import adafruit_tca9548a
from time import sleep, time
import board
import busio
import adafruit_tca9548a
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

num_oleds = 4
width = 127
height =63


border = 5
height_track = 0.5

fontsize = 25

FreeSans12 = ImageFont.truetype('FreeSans.ttf', 12)
FreeSans20 = ImageFont.truetype('FreeSans.ttf', 20)
FreeSans18 = ImageFont.truetype('FreeSans.ttf', 18)

menu_rect_track = (0, 0,width, int(height*height_track))
menu_rect_arm = (int(width*0.7), int(height*height_track), width, int(height*(height_track + (1 - height_track)/2)))
menu_rect_mute = (int(width*0.7), int(height*(height_track + (1 - height_track)/2)), width, height)
menu_rect_vol = (0, int(height*height_track), int(width*0.7), height)

fx_rect_name = (0, 0,width, int(height*height_track))
fx_rect_active = (int(width*0.8), int(height*height_track), width, height)
fx_rect_value = (0, int(height*height_track), int(width*0.8), height)

i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)


class Oled():
    def __init__(self, index):
        self.oled  = adafruit_ssd1306.SSD1306_I2C(128, 64, tca[index])
        self.oled.fill(0)
        self.oled.show()


    def test(self, i):
        image = Image.new('1', (width+1, height+1))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, i%(height), width, i%(width)), outline=i%3, fill=0)
        self.oled.image(image)
        self.oled.show()


    def menu_render_screen(self, data): # track, name, arm, mute, vol

        image = Image.new('1', (width+1, height+1))
        draw = ImageDraw.Draw(image)
        draw.rectangle(menu_rect_track, outline=1, fill=0)
        draw.text((menu_rect_track[0]+5, menu_rect_track[1]+5), f"{data['track']}: {data['name']}", font=FreeSans18, fill=1)


        fill = 1 if data['arm'] else 0
        draw.rectangle(menu_rect_arm, outline=1, fill=fill)
        draw.text((menu_rect_arm[0]+3, menu_rect_arm[1]+3), 'ARM', font=FreeSans12, fill=(1-fill))

        fill = 1 if data['mute'] else 0
        draw.rectangle(menu_rect_mute, outline=1, fill=fill)
        draw.text((menu_rect_mute[0]+3, menu_rect_mute[1]+3), 'MUTE', font=FreeSans12, fill=(1-fill))

        draw.rectangle(menu_rect_vol, outline=1, fill=0)
        draw.text((menu_rect_vol[0]+5, menu_rect_vol[1]+5), f"Vol: {data['vol']}", font=FreeSans20, fill=1)
        self.oled.image(image)
        self.oled.show()


    def fx_render_screen(self, data): # track, name, arm, mute, vol
        image = Image.new('1', (width+1, height+1))
        draw = ImageDraw.Draw(image)
        draw.rectangle(fx_rect_name, outline=1, fill=0)
        draw.text((fx_rect_name[0]+5, fx_rect_name[1]+5), f"{data['name']}", font=FreeSans18, fill=1)


        fill = 1 if data['active'] else 0
        draw.rectangle(fx_rect_active, outline=1, fill=fill)
        # draw.text((fx_rect_active[0]+3, fx_rect_active[1]+3), '', font=FreeSans12, fill=(1-fill))

        draw.rectangle(fx_rect_value, outline=1, fill=0)
        draw.text((fx_rect_value[0]+5, fx_rect_value[1]+5), f"-> {data['value']}", font=FreeSans20, fill=1)
        self.oled.image(image)
        self.oled.show()
        
        



if __name__ == '__main__':
    oleds = []
    for i in range(num_oleds):
        oleds.append(Oled(i))
    for oled in oleds:
        oled.test(1)
    exit

    while True:
        flag = True
        _bool = True if int(time())%2 == 0 else False
        _bool2 = True if int(time())%3 == 0 else False

        data_menu = {'track': 1,'name':  'Synth','arm': _bool,'mute': _bool2,'vol': int(time())%80}
        data_fx = {'name': 'Delay','value': 45, 'active':True}
        for oled in oleds:
            if flag:
                flag = False
                oled.menu_render_screen(data_menu)
            else:
                oled.fx_render_screen(data_fx)
        print("update")
        sleep(0.01)



