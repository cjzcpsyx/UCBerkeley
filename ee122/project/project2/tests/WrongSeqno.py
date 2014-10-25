import random

from BasicTest import *

class WrongSeqno(BasicTest):

    def __init__(self, forwarder, input_file):
        super(WrongSeqno, self).__init__(forwarder, input_file)

    def handle_packet(self):
        for p in self.forwarder.in_queue:
            p.seqno = p.seqno + random.randint(0, 1)
            self.forwarder.out_queue.append(p)

        # empty out the in_queue
        self.forwarder.in_queue = []
