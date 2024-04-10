import time
import math
import random
import threading
import matplotlib.pyplot as plt


class Node:
    def __init__(self, node_id, send_rate, channel_id):
        self.node_id = node_id
        self.send_rate = send_rate
        self.packet_list = []
        self.channel_id = channel_id

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
                packets_sent += 1
                tdma.cumulative_packets_count(current_time, 1)
            else:
                tdma.cumulative_packets_count(current_time, 0)

            time.sleep(1 / self.send_rate)  # Simulate packet transmission time
            current_time = time.time()
        return packets_sent


class DTDMA:
    # TODO pass corresponding node id to here for each channel
    def __init__(self, num_nodes, node_ids, total_time, packet_send_rate, channel_id):
        self.num_nodes = num_nodes
        self.total_time = total_time
        self.packet_send_rate = packet_send_rate
        self.time_slot_duration = total_time / len(node_ids)
        # self.time_slot_duration = []
        self.nodes = [
            Node(node_id, packet_send_rate, channel_id) for node_id in node_ids
        ]
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
        self.channel_id = channel_id
        self.packet_send = 0

    def add_packet_to_node(self, node_id, packet):
        for node in self.nodes:
            if node.node_id == node_id:
                node.add_packet(packet)

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
        # print("total packets" + str(self.total_packets))

        for node in self.nodes:
            # A node has nothing to send
            if len(node.packet_list) == 0:
                self.nodes.remove(node)
                self.num_nodes -= 1
            else:
                # count how many packets in each node, and split time frame accrdingly
                self.packet_buffer.append((node, len(node.packet_list)))

        for node in self.nodes:

            duration = 0
            if self.total_packets != 0:
                duration = (len(node.packet_list) / self.total_packets) * total_time

            self.time_slot_durations.append(
                (
                    node,
                    duration,
                )
            )
        # print(self.nodes)

    def simulate(self):
        self.scheduler()
        slot_start_time = time.time()
        for slot in self.time_slot_durations:
            node = slot[0]
            duration = slot[1]

            slot_end_time = slot_start_time + duration
            # Get the node for the current time slot
            self.packet_send = node.send_packets(self, slot_end_time)
            self.current_slot += 1
            slot_start_time = slot_end_time


class Channel(threading.Thread):
    def __init__(
        self, num_nodes, node_id_per_channel, total_time, packet_send_rate, channel_id
    ):
        super().__init__()
        self.num_nodes = num_nodes
        self.nodes_id = node_id_per_channel
        self.total_time = total_time
        self.packet_send_rate = packet_send_rate
        self.channel_id = channel_id
        self.throughput = 0

    # TODO: something wrong with the node_id
    def run(self):
        # print("Channel Run")
        self.dtdma = DTDMA(
            self.num_nodes,
            self.nodes_id,
            self.total_time,
            self.packet_send_rate,
            self.channel_id,
        )
        # self.channel_id += 1
        for node_id in self.nodes_id:
            if node_id % 2 == 0:
                for i in range(random.randint(0, 1000)):
                    self.dtdma.add_packet_to_node(node_id, f"Packet {i}")
            # else:
            #     for i in range(1, 50):
            #         self.dtdma.add_packet_to_node(node_id, f"Packet {i}")

        self.dtdma.simulate()
        self.throughput = self.dtdma.packet_send


class FDMA:

    def __init__(self, num_nodes, num_channels, total_time, packet_send_rate):
        self.my_channels = []
        self.throughput = 0
        self.nodes_id = [node_id for node_id in range(num_nodes)]

        num_nodes_per_channel = int(num_nodes / num_channels)
        # print(self.nodes_id)
        channel_id = 0
        for _ in range(num_channels):
            node_ids_per_channel = []
            for i in range(num_nodes_per_channel):
                if len(self.nodes_id) < num_nodes_per_channel:
                    node_ids_per_channel = [id for id in self.nodes_id]
                    break
                node_ids_per_channel.append(self.nodes_id[i])
                self.nodes_id.remove(self.nodes_id[i])

            # TODO: pass a list of node id to Channel
            my_channel = Channel(
                num_nodes_per_channel,
                node_ids_per_channel,
                total_time,
                packet_send_rate,
                channel_id,
            )
            self.my_channels.append(my_channel)
            channel_id += 1

    def simulate(self):
        # print("FDMA simulate")
        for channel in self.my_channels:
            channel.start()
        for channel in self.my_channels:
            channel.join()

        x_category = []
        y_value = []
        for channel in self.my_channels:
            print(channel.throughput)
            self.throughput += channel.throughput
            x_category.append(channel.channel_id)
            y_value.append(channel.throughput)
        # print(x_category)
        # print(y_value)
        plt.bar(x_category, y_value)
        plt.xlabel("Channel ID")
        plt.ylabel("Number of Packets send")
        plt.title("Cumulative packets send by Channel")
        # plt.show()
        plt.savefig("ftdma.png")


if __name__ == "__main__":
    num_nodes = 1000
    total_time = 10  # seconds
    packet_send_rate = 200  # packets per second
    # dtdma_system = DTDMA(num_nodes, total_time, packet_send_rate)

    num_channels = int(num_nodes / 2)
    packet_send_raterate_per_channel = packet_send_rate / num_channels
    fdma_system = FDMA(
        num_nodes, num_channels, total_time, packet_send_raterate_per_channel
    )
    start = time.time()
    fdma_system.simulate()
    end = time.time()
    print(end - start)
    print(fdma_system.throughput)
