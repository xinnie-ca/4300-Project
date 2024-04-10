import time
import random
import matplotlib.pyplot as plt


class Node:
    def __init__(self, node_id, send_rate):
        self.node_id = node_id
        self.send_rate = send_rate
        self.packet_list = []

    def add_packet(self, packet):
        self.packet_list.append(packet)

    def send_packets(self, tdma, slot_end_time):
        packets_sent = 0
        current_time = time.time()
        while current_time < slot_end_time:
            if len(self.packet_list) != 0:
                packet = self.packet_list.pop(0)  # Send the first packet in the list
                print(f"Node {self.node_id} sent packet: {packet}")
                packets_sent += 1
                tdma.cumulative_packets_count(current_time, 1)
            else:
                print("Idle")
                tdma.cumulative_packets_count(current_time, 0)

            time.sleep(1 / self.send_rate)  # Simulate packet transmission time
            current_time = time.time()
        return packets_sent


class TDMA:
    def __init__(self, num_nodes, total_time, packet_send_rate):
        self.num_nodes = num_nodes
        self.total_time = total_time
        self.packet_send_rate = packet_send_rate
        self.time_slot_duration = total_time / num_nodes
        self.nodes = [Node(node_id, packet_send_rate) for node_id in range(num_nodes)]
        self.current_slot = 0
        self.start_time = 0
        self.end_time = 0
        self.cumulative_packets = 0
        self.cumulative_packet_send = []
        self.elapsed_time = []
        self.time_zero = time.time()

    def add_packet_to_node(self, node_id, packet):
        self.nodes[node_id].add_packet(packet)

    def cumulative_packets_count(self, time, packets):
        self.cumulative_packets += packets
        self.cumulative_packet_send.append(self.cumulative_packets)
        self.elapsed_time.append(time - self.time_zero)

    def draw(self):

        plt.plot(self.elapsed_time, self.cumulative_packet_send)
        plt.xlabel("Elapsed Time")
        plt.ylabel("Amount Of Packets")
        plt.title("TDMA Cumulative Packets Send")
        # plt.show()
        plt.savefig("tdma.png")

    def simulate(self):
        self.total_packets = sum(len(node.packet_list) for node in self.nodes)
        self.start_time = time.time()
        while self.current_slot < self.num_nodes:
            slot_start_time = (
                self.start_time + self.current_slot * self.time_slot_duration
            )
            slot_end_time = slot_start_time + self.time_slot_duration
            print(f"Time Slot {self.current_slot}:")
            # Get the node for the current time slot
            node_id = self.current_slot % self.num_nodes
            packets_sent = self.nodes[node_id].send_packets(self, slot_end_time)
            print(f"Node {node_id} sent {packets_sent} packet(s) in this slot.")
            self.current_slot += 1


if __name__ == "__main__":
    num_nodes = 1000
    total_time = 10  # seconds
    packet_send_rate = 200  # packets per second
    tdma_system = TDMA(num_nodes, total_time, packet_send_rate)

    # Add packets to nodes
    for node_id in range(num_nodes):
        if node_id % 2 == 0:
            for i in range(random.randint(0, 1000)):
                tdma_system.add_packet_to_node(node_id, f"Packet {i}")
        # else:
        #     for i in range(1, 3):
        #         tdma_system.add_packet_to_node(node_id, f"Packet {i}")

    # Simulate TDMA
    tdma_system.simulate()

    efficiency = tdma_system.total_packets / total_time
    tdma_system.draw()
    print(
        tdma_system.cumulative_packet_send[len(tdma_system.cumulative_packet_send) - 1]
    )
