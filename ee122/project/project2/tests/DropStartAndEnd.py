import random

from BasicTest import *

class DropStartAndEnd(BasicTest):

    def __init__(self, forwarder, input_file):
        super(DropStartAndEnd, self).__init__(forwarder, input_file)
        self.dropped_starts = 0
        self.dropped_ends = 0

    def handle_packet(self):
        for p in self.forwarder.in_queue:
            msg_type = p.msg_type
            if msg_type == 'start' and self.dropped_starts < 10:
                self.dropped_starts += 1
            elif msg_type == 'end' and self.dropped_ends < 10:
                self.dropped_ends += 1
            else:
                if random.choice([True, False]):
                    self.forwarder.out_queue.append(p)

        # empty out the in_queue
        self.forwarder.in_queue = []
