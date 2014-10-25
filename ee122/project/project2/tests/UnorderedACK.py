import random

from BasicTest import *

class UnorderedACK(BasicTest):

    def __init__(self, forwarder, input_file):
        super(UnorderedACK, self).__init__(forwarder, input_file)

    def handle_packet(self):
        for p in self.forwarder.in_queue:
            index = random.randint(0, len(self.forwarder.out_queue)) 
            self.forwarder.out_queue.insert(index, p)

        # empty out the in_queue
        self.forwarder.in_queue = []
