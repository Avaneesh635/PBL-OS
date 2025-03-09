import streamlit as st
import matplotlib.pyplot as plt

st.title("OS Explorer - Simulation Tool")

# CPU Scheduling
def fcfs(burst_times):
    waiting_time = [0] * len(burst_times)
    for i in range(1, len(burst_times)):
        waiting_time[i] = waiting_time[i-1] + burst_times[i-1]
    return waiting_time

# Disk Scheduling
def fcfs_disk(requests, head):
    total_distance = sum(abs(head - req) for req in requests)
    return total_distance

# Memory Management
def first_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                allocation[i] = j
                blocks[j] -= processes[i]
                break
    return allocation

# File System
def file_allocation(num_files):
    return [f"File {i+1} allocated successfully" for i in range(num_files)]

# Graph Plotting
def plot_graph(processes, burst_times, waiting_times):
    fig, ax = plt.subplots()
    ax.bar(range(len(burst_times)), burst_times, label="Burst Time")
    ax.bar(range(len(waiting_times)), waiting_times, label="Waiting Time", bottom=burst_times)
    ax.set_xlabel("Processes")
    ax.set_ylabel("Time")
    ax.legend()
    st.pyplot(fig)

# GUI Interface
option = st.sidebar.selectbox("Choose Simulation", 
                              ["CPU Scheduling", "Disk Scheduling", "Memory Management", "File System"])

if option == "CPU Scheduling":
    burst_times = list(map(int, st.text_input("Enter Burst Times (space separated):").split()))
    if st.button("Simulate"):
        waiting_times = fcfs(burst_times)
        plot_graph(range(len(burst_times)), burst_times, waiting_times)
        st.success("Simulation Complete")

elif option == "Disk Scheduling":
    requests = list(map(int, st.text_input("Enter Disk Requests (space separated):").split()))
    head = int(st.text_input("Enter Initial Head Position:"))
    if st.button("Simulate"):
        total_distance = fcfs_disk(requests, head)
        st.write(f"Total Head Movement: {total_distance} cylinders")

elif option == "Memory Management":
    blocks = list(map(int, st.text_input("Enter Memory Block Sizes (space separated):").split()))
    processes = list(map(int, st.text_input("Enter Process Sizes (space separated):").split()))
    if st.button("Simulate"):
        allocation = first_fit(blocks, processes)
        for i, alloc in enumerate(allocation):
            if alloc != -1:
                st.write(f"Process {i+1} allocated to Block {alloc+1}")
            else:
                st.write(f"Process {i+1} not allocated")

elif option == "File System":
    num_files = int(st.text_input("Enter Number of Files:"))
    if st.button("Simulate"):
        result = file_allocation(num_files)
        for res in result:
            st.write(res)
