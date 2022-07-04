from lib_oled96 import ssd1306
from smbus import SMBus
from PIL import Image
from time import sleep, time
from PIL import ImageFont


width = 127
height = 63
border = 5
height_track = 0.5
_time = int(time())
fontsize = 25
# img = 'bypass.jpg'
FreeSans12 = ImageFont.truetype('FreeSans.ttf', 12)
FreeSans20 = ImageFont.truetype('FreeSans.ttf', 20)
FreeSans18 = ImageFont.truetype('FreeSans.ttf', 18)
i2cbus = SMBus(1)     
# canvas menu
menu_rect_track = (0, 0,width, int(height*height_track))
menu_rect_arm = (int(width*0.7), int(height*height_track), width, int(height*(height_track + (1 - height_track)/2)))
menu_rect_mute = (int(width*0.7), int(height*(height_track + (1 - height_track)/2)), width, height)
menu_rect_vol = (0, int(height*height_track), int(width*0.7), height)


fx_rect_name = (0, 0,width, int(height*height_track))
fx_rect_active = (int(width*0.8), int(height*height_track), width, height)
fx_rect_value = (0, int(height*height_track), int(width*0.8), height)


   # 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1
class Oled():



    def __init__(self,bus):
        self.oled = ssd1306(bus)
        self.oled.display()
        


    def menu_render_screen(self, data): # track, name, arm, mute, vol

        draw = self.oled.canvas
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


        self.oled.display()
    def fx_render_screen(self, data): # track, name, arm, mute, vol

        draw = self.oled.canvas
        draw.rectangle(fx_rect_name, outline=1, fill=0)
        draw.text((fx_rect_name[0]+5, fx_rect_name[1]+5), f"{data['name']}", font=FreeSans18, fill=1)


        fill = 1 if data['active'] else 0
        draw.rectangle(fx_rect_active, outline=1, fill=fill)
        # draw.text((fx_rect_active[0]+3, fx_rect_active[1]+3), '', font=FreeSans12, fill=(1-fill))

        draw.rectangle(fx_rect_value, outline=1, fill=0)
        draw.text((fx_rect_value[0]+5, fx_rect_value[1]+5), f"-> {data['value']}", font=FreeSans20, fill=1)


        self.oled.display()




if __name__ == '__main__':
    address = 0x3C
    oled = Oled()
    while True:
        sleep(0.1)
        # oled.get_img('Wet Delay',str(int(time())%15),int(time()/2)%2==0)
        # oled.oled.fill_rect(10, 10, 107, 43, 1)
        _bool = True if int(time())%2 == 0 else False
        _bool2 = True if int(time())%3 == 0 else False

        data_menu = {'track': 1,'name':  'Synth','arm': _bool,'mute': _bool2,'vol': int(time())%80}
        data_fx = {'name': 'Delay','value': 45, 'active':True}
        oled.menu_render_screen(data_menu) #track, name, arm, mute, vol
        # oled.fx_render_screen(data_fx) #track, name, arm, mute, vol


