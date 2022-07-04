import argparse
from pythonosc import dispatcher, udp_client, osc_server
from threading import Thread
from time import sleep



class ServerOSC():   
    def __init__(self):
        parser_server = argparse.ArgumentParser()
        parser_server.add_argument("--ip",
            default="127.0.0.1", help="The ip to listen on")
        parser_server.add_argument("--port",
            type=int, default=9999, help="The port to listen on")
        args_server = parser_server.parse_args()
        router = dispatcher.Dispatcher()
        router.set_default_handler(self.default_handler)
        self.server = osc_server.ThreadingOSCUDPServer((args_server.ip, args_server.port), router)
        self.message_buffer = []
     
        self.flag = True


        parser_client = argparse.ArgumentParser()
        parser_client.add_argument("--ip", default="127.0.0.1",help="The ip of the OSC server")
        parser_client.add_argument("--port", type=int, default=8888,help="The port the OSC server is listening on")
        args_client = parser_client.parse_args()
        self.client = udp_client.SimpleUDPClient(args_client.ip, args_client.port)


    def default_handler(self, address, *args):
            self.message_buffer.append([address, args])
            # print('default_hnadler')
            # print(f"{address}: {args}")

    def read_message_buffer(self):
            _buff = self.message_buffer
            self.message_buffer = []
            return _buff

    def send_msg(self, msg):
        self.client.send_message(msg[0], msg[1])
        


    def start_server(self):
        self.thread_server = Thread(target=self.server.serve_forever)
        self.thread_server.start()

    def stop_server(self):
        self.server.shutdown()



if __name__ == "__main__":
    serverosc = ServerOSC()
    serverosc.start_server()
    try:
        for i in range(100):
            sleep(0.5)
            msg = ['/test/track1', i]
            serverosc.send_msg(msg)
            print(msg)
        serverosc.stop_server()
    except KeyboardInterrupt:
        serverosc.stop_server()

            




