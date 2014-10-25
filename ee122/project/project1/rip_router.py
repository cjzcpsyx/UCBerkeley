from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''
class RIPRouter (Entity):
    def __init__(self):
    # Add your code here!
        self.distance_vector = {}
        self.forward_table = {}
        self.neighbour_port = {}

    def handle_rx (self, packet, port):
    # Add your code here!
        if (type(packet) is DiscoveryPacket):
            if (packet.is_link_up):
                self.forward_table[(packet.src, packet.src)] = 1
                self.neighbour_port[packet.src] = port
                self.distance_vector[packet.src] = (packet.src, 1)
                for neighbours in self.neighbour_port.keys():
                    new_packet1 = RoutingUpdate()
                    for inform in self.distance_vector.keys():
                        if (self.distance_vector[inform][0] != neighbours):
                            new_packet1.add_destination(inform, self.distance_vector[inform][1])
                    self.send(new_packet1, self.neighbour_port[neighbours], flood=False)
            else:
                del self.neighbour_port[packet.src]
                for unlink in self.forward_table.keys():
                    if (unlink[1] is packet.src):
                        del self.forward_table[unlink]
                        distances1 = set()
                        for update in self.forward_table.keys():
                            if (update[0] is unlink[0]):
                                distances1.add(self.forward_table[update])
                        if (len(distances1) == 0):
                            del self.distance_vector[unlink[0]]
                        else:
                            self.distance_vector[unlink[0]] = (self.get_distance_vector(unlink[0], min(distances1)), min(distances1))
                for neighbours in self.neighbour_port.keys():
                    new_packet1 = RoutingUpdate()
                    for inform in self.distance_vector.keys():
                        if (self.distance_vector[inform][0] != neighbours):
                            new_packet1.add_destination(inform, self.distance_vector[inform][1])
                    self.send(new_packet1, self.neighbour_port[neighbours], flood=False)
        elif (type(packet) is RoutingUpdate):
            updated = False
            for withdraw in self.forward_table.keys():
                if (withdraw[1] is packet.src and withdraw[0] not in (packet.all_dests()+[packet.src])):
                    del self.forward_table[withdraw]
                    distances2 = set()
                    for update2 in self.forward_table.keys():
                        if (update2[0] is withdraw[0]):
                            distances2.add(self.forward_table[update2])
                    if (len(distances2) == 0):
                        del self.distance_vector[withdraw[0]]
                        updated = True
                    else:
                        if (self.distance_vector[withdraw[0]][1] != min(distances2)):
                            self.distance_vector[withdraw[0]] = (self.get_distance_vector(withdraw[0], min(distances2)), min(distances2))
                            updated = True
                        elif (self.distance_vector[withdraw[0]][0] != self.get_distance_vector(withdraw[0], min(distances2))):
                            updated = True
                            self.distance_vector[withdraw[0]] = (self.get_distance_vector(withdraw[0], min(distances2)), min(distances2))
            for dest in packet.all_dests():
                if (dest != self):
                    self.forward_table[(dest, packet.src)] = 1 + packet.get_distance(dest)
                    distances1 = set()
                    for update in self.forward_table.keys():
                        if (update[0] is dest):
                            distances1.add(self.forward_table[update])
                    if (len(distances1) == 0):
                        if (dest in self.distance_vector.keys()):
                            updated = True
                            del distance_vector[dest]
                    else:
                        if (dest not in self.distance_vector.keys() or self.distance_vector[dest][1] != min(distances1)):
                            updated = True
                            self.distance_vector[dest] = (self.get_distance_vector(dest, min(distances1)), min(distances1))
                        elif (self.distance_vector[dest][0] != self.get_distance_vector(dest, min(distances1))):
                            updated = True
                            self.distance_vector[dest] = (self.get_distance_vector(dest, min(distances1)), min(distances1))
            if (updated):
                for neighbours in self.neighbour_port.keys():
                    new_packet1 = RoutingUpdate()
                    for inform in self.distance_vector.keys():
                        if (self.distance_vector[inform][0] != neighbours):
                            new_packet1.add_destination(inform, self.distance_vector[inform][1])
                    self.send(new_packet1, self.neighbour_port[neighbours], flood=False)
        else:
            if (packet.dst != self):
                if (packet.dst in self.distance_vector.keys()):
                    self.send(packet, self.neighbour_port[self.distance_vector[packet.dst][0]], flood=False)
    def get_distance_vector(self, dest, distance):
        ports = set()
        for route in self.forward_table.keys():
            if (route[0] is dest and self.forward_table[route] == distance):
                ports.add(self.neighbour_port[route[1]])
        for vector in self.neighbour_port.keys():
            if (self.neighbour_port[vector] == min(ports)):
                return vector






