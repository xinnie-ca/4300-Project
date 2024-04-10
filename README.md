# 4300 Project - Dynamic Time and Frequency Division Mulitple Access Method
This repository contains a Python program that simulates the hybrid version of the TDMA and FDMA methods.
## Features
`tdma.py`: This program is a simulation of the TDMA (Time Division Multiple Access) method, designed to mitigate collisions within a communication channel. It calculates the length of each time slot by dividing the total length of the time frame by the number of nodes present on the network.

`dtdma.py`: This program is a simulation of the dynamic TDMA (Time Division Multiple Access) method. Similar to traditional TDMA, it divides the time frame into slots for each node. However, it includes an additional scheduler component that continuously monitors the load of each node and dynamically adjusts time slot allocations accordingly.

'ftdma.py`: This simulation represents a hybrid approach combining TDMA and FDMA. It segments the bandwidth into multiple frequency channels and incorporates a dynamic TDMA method within each of these channels.

## How to Run
`git clone` https://github.com/xinnie-ca/4300-Project.git

In the IDE, you can simply click the run button. 

Or in the terminal

`python3 tdma.py` to run the TDMA simulation and obtain the graph
 
`python3 dynamic_tdma.py` to run the dynamic TDMA simulation and obtain the graph
 
`python3 ftdma.py` to run the hybrid version of the simulation and obtain the graph

## Additional information
This program uses random modules and matplotlib, please install these libraries before running the program.

## Sample output
### TDMA
![tdma_1000_zoom](https://github.com/xinnie-ca/4300-Project/assets/108996769/bdb8acfc-e8fd-4125-bc79-fe9c3b18d0b1)

### TDMA with a low number of loads to show the idle during the transmission
![tdma_low_node](https://github.com/xinnie-ca/4300-Project/assets/108996769/35a3ec6b-87d8-471c-91cb-05ff96cf01f7)

### Dynamic TDMA
![dtdma](https://github.com/xinnie-ca/4300-Project/assets/108996769/f7276b1e-cd95-4f39-b37c-4560d09e6658)

### DTFDMA packets send by each channel
![ftdma](https://github.com/xinnie-ca/4300-Project/assets/108996769/1cedf358-f421-4fc0-90d7-935ee8a93124)

### DTFDMA performance degraded situation
![ftdma_low_performance](https://github.com/xinnie-ca/4300-Project/assets/108996769/f7f9657a-ea67-429b-80c0-d1bab7dcd644)




