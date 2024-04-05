import time

import matplotlib.pyplot as plt


class Node:
    def __init__(self, node_id, send_rate):
        self.node_id = node_id
        self.send_rate = send_rate
        self.packet_list = []

    def __str__(self):
        return str(self.node_id)

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
                # tdma.total_packets -= 1
            else:
                print("Idle")
                tdma.cumulative_packets_count(current_time, 0)

            time.sleep(1 / self.send_rate)  # Simulate packet transmission time
            current_time = time.time()
        return packets_sent


class DTDMA:
    def __init__(self, num_nodes, total_time, packet_send_rate):
        self.num_nodes = num_nodes
        self.total_time = total_time
        self.packet_send_rate = packet_send_rate
        self.time_slot_duration = total_time / num_nodes
        # self.time_slot_duration = []
        self.nodes = [Node(node_id, packet_send_rate) for node_id in range(num_nodes)]
        self.total_packets = 0
        self.current_slot = 0
        self.start_time = 0
        self.end_time = 0
        self.cumulative_packets = 0
        self.cumulative_packet_send = []
        self.elapsed_time = []
        self.time_zero = time.time()
        self.packet_buffer = []  # for counting how many packets in each node
        self.time_slot_durations = []

    def add_packet_to_node(self, node_id, packet):
        self.nodes[node_id].add_packet(packet)

    def cumulative_packets_count(self, time, amount_packet_send):
        self.cumulative_packets += amount_packet_send
        self.cumulative_packet_send.append(self.cumulative_packets)
        self.elapsed_time.append(time - self.time_zero)

    def draw(self):

        plt.plot(self.elapsed_time, self.cumulative_packet_send)
        plt.xlabel("Elapsed Time")
        plt.ylabel("Amount Of Packets")
        plt.title("TDMA Cumulative Packets Send")
        plt.show()

    def scheduler(self):
        self.total_packets = sum(len(node.packet_list) for node in self.nodes)
        print("total packets" + str(self.total_packets))

        for node in self.nodes:
            # A node has nothing to send
            if len(node.packet_list) == 0:
                self.nodes.remove(node)
                self.num_nodes -= 1
            else:
                # count how many packets in each node, and split time frame accrdingly
                self.packet_buffer.append((node, len(node.packet_list)))

        for node in self.nodes:
            self.time_slot_durations.append(
                (
                    node,
                    min(
                        (len(node.packet_list) / self.total_packets) * total_time,
                        self.packet_send_rate * len(node.packet_list),
                    ),
                )
            )
        print(self.time_slot_durations)

    def simulate(self):

        self.scheduler()
        slot_start_time = time.time()
        for slot in self.time_slot_durations:
            node = slot[0]
            duration = slot[1]

            slot_end_time = slot_start_time + duration
            print(f"Time Slot {self.current_slot} duration is: {duration}")
            print(slot_end_time)
            # Get the node for the current time slot
            packets_sent = node.send_packets(self, slot_end_time)
            print(f"Node {node.node_id} sent {packets_sent} packet(s) in this slot.")
            self.current_slot += 1
            slot_start_time = slot_end_time


if __name__ == "__main__":
    num_nodes = 10
    total_time = 10  # seconds
    packet_send_rate = 2  # packets per second
    dtdma_system = DTDMA(num_nodes, total_time, packet_send_rate)

    # Add packets to nodes
    for node_id in range(num_nodes):
        if node_id % 2 == 0:
            for i in range(1, 11):
                dtdma_system.add_packet_to_node(node_id, f"Packet {i}")
        # else:
        #     for i in range(1, 3):
        #         tdma_system.add_packet_to_node(node_id, f"Packet {i}")

    # Simulate TDMA

    # while tdma_system.total_packets >= 0:
    dtdma_system.simulate()
    for node in dtdma_system.nodes:
        print(node.node_id, node.packet_list)
    print(dtdma_system.total_packets)
    efficiency = dtdma_system.total_packets / total_time
    dtdma_system.draw()
