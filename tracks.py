# address = 0x3C
from oled import Oled
# _menu_oled = Oled(address)
# from urllib import request
# from server import ServerOSC
from encoders import Encoders
from time import sleep, time
from smbus import SMBus
from led import LED



class Track():
    ##########################

    
    num_tracks = 8 
    num_encoders = 3 # without menu encoder
    num_pages = 2
    track = 1
    page  = 0 

    encoders = Encoders()
    i2cbus_menu = SMBus(1)
    oled_menu  = Oled(i2cbus_menu)
    tracks = []
    led = LED(8)


    def __init__(self, index):
         self.index = index
         Track.tracks.append(self)


    @classmethod
    def init_tracks(cls):
        for track in range(cls.num_tracks):
            Track(track)


    @classmethod
    def encoder_handler(cls):
        msg = cls.encoders.get_msg()
        msg_menu = msg[0]
        msg_fx = msg[1:]

        cls.handle_msg_menu(msg_menu)


    @classmethod
    def handle_msg_menu(cls, msg):
        if msg[0] and msg[1] == None:
            cls.tracks[cls.track].arm()
        elif msg[1] == 1 and msg[0] == None:
            print(msg)
            cls.change_track(msg[1])
            
    def arm(self):
        print(f'arm {self.index}')
    
    @classmethod    
    def change_track(cls, val):
        cls.track = (cls.track + val)%cls.num_tracks
        print(f"changed to {cls.track}")
        data_menu = {'track': cls.track,'name':  'Synth','arm': True,'mute':False,'vol': int(time())%80}
        cls.led.set_pixel(cls.track)
        
        
        cls.oled_menu.menu_render_screen(data_menu)




if __name__ == '__main__':
    Track.encoders.start()
    Track.init_tracks()
    # Track.serverosc.start_server()

    try:
        while True:
            # sleep(0.01)
            Track.encoder_handler()
            # my_buffer = Track.serverosc.read_message_buffer()
            # Track.read_msg_from_buffer(my_buffer)

    except KeyboardInterrupt: # stop encoder loop
        Track.serverosc.stop_server()

