import sys
import getopt

import Checksum
import BasicSender

from random import randint

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False):
        super(Sender, self).__init__(dest, port, filename, debug)
        self.seqno = 0
        self.msg = None
        self.next_msg = None
        self.msg_type = 'start'
        self.deliver_window = {}
        self.window_size = 5
        self.end = False

    # Main sending loop.
    def start(self):
        self.msg = self.infile.read(1400)
        packet1 = self.make_packet(self.msg_type, self.seqno, self.msg)
        self.send(packet1)
        self.deliver_window[self.seqno] = (self.msg_type, self.msg)
        self.msg_type = 'data'
        self.seqno += 1

        self.msg = self.infile.read(1400)
        for i in range(self.window_size - 1):
            self.next_msg = self.infile.read(1400)
            if self.next_msg == "":
                self.msg_type = 'end'
            packet2 = self.make_packet(self.msg_type, self.seqno, self.msg)
            self.send(packet2)
            self.deliver_window[self.seqno] = (self.msg_type, self.msg)
            self.msg = self.next_msg
            self.seqno += 1
            if self.msg_type == 'end':
                break
                
        while not self.end:
            response = self.receive(0.5)
            if response == None:
                self.handle_timeout()
            else:
                self.handle_new_ack(response)

        self.infile.close()



    def handle_timeout(self):
        for deliver_keys1 in self.deliver_window.keys():
            packet3 = self.make_packet(self.deliver_window[deliver_keys1][0], deliver_keys1, self.deliver_window[deliver_keys1][1])
            self.send(packet3)

    def handle_new_ack(self, ack):
        if Checksum.validate_checksum(ack):
            receive_type, receive_seqno, receive_data, receive_checksum = self.split_packet(ack)
            if int(receive_seqno) > self.deliver_window.keys()[0]:
                for delete_keys in self.deliver_window.keys():
                    if delete_keys < int(receive_seqno):
                        del self.deliver_window[delete_keys]
            if not self.msg_type == 'end':
                for j in range(self.window_size - len(self.deliver_window)):
                    self.next_msg = self.infile.read(1400)
                    if self.next_msg == "":
                        self.msg_type = 'end'
                    self.deliver_window[self.seqno] = (self.msg_type, self.msg)
                    self.msg = self.next_msg
                    self.seqno += 1
                    if self.msg_type == 'end':
                        break
            if len(self.deliver_window) == 0:
                self.end = True


    def handle_dup_ack(self, ack):
        pass

    def log(self, msg):
        if self.debug:
            print msg

'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:d", ["file=", "port=", "address=", "debug="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest,port,filename,debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
