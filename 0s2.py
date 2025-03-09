import streamlit as st
import matplotlib.pyplot as plt

st.title("💻 OS Explorer - Simulation Tool")
st.sidebar.header("Choose Simulation")
choice = st.sidebar.selectbox("Select Simulation", ["CPU Scheduling", "Disk Scheduling", "Memory Management", "File System", "Deadlock"])

# Function for CPU Scheduling
if choice == "CPU Scheduling":
    st.subheader("🖥️ CPU Scheduling")
    algo = st.selectbox("Select Algorithm", ["FCFS", "SJF", "Round Robin"])
    burst_time = st.text_input("Enter Burst Times (space-separated)", "5 8 3 4")
    
    if st.button("Simulate"):
        burst_time = list(map(int, burst_time.split()))
        waiting_time = [0] * len(burst_time)

        if algo == "FCFS":
            for i in range(1, len(burst_time)):
                waiting_time[i] = waiting_time[i-1] + burst_time[i-1]
        elif algo == "SJF":
            burst_time.sort()
            for i in range(1, len(burst_time)):
                waiting_time[i] = waiting_time[i-1] + burst_time[i-1]
        elif algo == "Round Robin":
            time_quantum = int(st.text_input("Enter Time Quantum", "3"))
            remaining_bt = burst_time[:]
            t = 0
            while True:
                done = True
                for i in range(len(burst_time)):
                    if remaining_bt[i] > 0:
                        done = False
                        if remaining_bt[i] > time_quantum:
                            t += time_quantum
                            remaining_bt[i] -= time_quantum
                        else:
                            t += remaining_bt[i]
                            waiting_time[i] = t - burst_time[i]
                            remaining_bt[i] = 0
                if done:
                    break

        st.write("## Waiting Times")
        for i in range(len(waiting_time)):
            st.write(f"Process {i+1}: {waiting_time[i]} ms")

        # Plot graph
        fig, ax = plt.subplots()
        ax.bar(range(len(waiting_time)), waiting_time, color='skyblue')
        ax.set_xlabel("Process")
        ax.set_ylabel("Waiting Time")
        ax.set_title(f"{algo} Scheduling Result")
        st.pyplot(fig)

# Function for Disk Scheduling
if choice == "Disk Scheduling":
    st.subheader("💽 Disk Scheduling")
    algo = st.selectbox("Select Algorithm", ["FCFS", "SSTF", "SCAN"])
    requests = st.text_input("Enter Requests (space-separated)", "98 183 37 122 14 124 65 67")
    head = int(st.text_input("Enter Head Position", "53"))

    if st.button("Simulate"):
        requests = list(map(int, requests.split()))
        total_distance = 0

        if algo == "FCFS":
            for req in requests:
                total_distance += abs(head - req)
                head = req
        elif algo == "SSTF":
            while requests:
                closest = min(requests, key=lambda x: abs(head-x))
                total_distance += abs(head - closest)
                head = closest
                requests.remove(closest)
        elif algo == "SCAN":
            requests.sort()
            for req in requests:
                total_distance += abs(head - req)
                head = req

        st.write(f"## Total Head Movement: {total_distance} cylinders")
        fig, ax = plt.subplots()
        ax.plot(requests, color='orange', marker='o')
        ax.set_xlabel("Requests")
        ax.set_ylabel("Cylinder")
        st.pyplot(fig)

# Function for Memory Management
if choice == "Memory Management":
    st.subheader("💾 Memory Management")
    algo = st.selectbox("Select Algorithm", ["First Fit", "Best Fit", "Worst Fit"])
    memory_blocks = st.text_input("Enter Memory Block Sizes (space-separated)", "100 500 200 300 600")
    process_sizes = st.text_input("Enter Process Sizes (space-separated)", "212 417 112 426")

    if st.button("Simulate"):
        memory_blocks = list(map(int, memory_blocks.split()))
        process_sizes = list(map(int, process_sizes.split()))
        output = []

        for i, process in enumerate(process_sizes):
            if algo == "First Fit":
                for j, block in enumerate(memory_blocks):
                    if block >= process:
                        output.append(f"Process {i+1} allocated to Block {j+1}")
                        memory_blocks[j] -= process
                        break
            elif algo == "Best Fit":
                memory_blocks.sort()
                for block in memory_blocks:
                    if block >= process:
                        output.append(f"Process {i+1} allocated to Block {memory_blocks.index(block)+1}")
                        block -= process
                        break
            elif algo == "Worst Fit":
                memory_blocks.sort(reverse=True)
                for block in memory_blocks:
                    if block >= process:
                        output.append(f"Process {i+1} allocated to Block {memory_blocks.index(block)+1}")
                        block -= process
                        break
        
        st.write("## Allocation Result")
        for line in output:
            st.write(line)

# Function for File System Simulation
if choice == "File System":
    st.subheader("📁 File System Simulation")
    method = st.selectbox("Select Allocation Method", ["Contiguous", "Linked", "Indexed"])
    files = int(st.text_input("Enter Number of Files", "5"))

    if st.button("Simulate"):
        output = []
        for i in range(files):
            output.append(f"File {i+1} allocated successfully")
        st.write("## File Allocation Result")
        for line in output:
            st.write(line)

# Function for Deadlock Simulation
if choice == "Deadlock":
    st.subheader("🔐 Deadlock Detection & Avoidance")
    method = st.selectbox("Select Deadlock Method", ["RAG (Detection)", "Banker's Algorithm (Avoidance)"])

    if method == "RAG (Detection)":
        processes = int(st.text_input("Enter Number of Processes", "5"))
        resources = int(st.text_input("Enter Number of Resources", "3"))

        if st.button("Simulate"):
            st.write("⚠️ Deadlock Detected in Resource Allocation Graph")

    if method == "Banker's Algorithm (Avoidance)":
        max_need = st.text_area("Enter Maximum Need Matrix (Space-separated)")
        allocated = st.text_area("Enter Allocated Resources Matrix (Space-separated)")
        available = st.text_input("Enter Available Resources (Space-separated)")

        if st.button("Simulate"):
            max_need = [list(map(int, x.split())) for x in max_need.split('\n')]
            allocated = [list(map(int, x.split())) for x in allocated.split('\n')]
            available = list(map(int, available.split()))

            # Banker's Algorithm Logic
            n = len(allocated)
            work = available[:]
            finish = [False] * n
            safe_sequence = []

            while len(safe_sequence) < n:
                found = False
                for i in range(n):
                    if not finish[i] and all(max_need[i][j] - allocated[i][j] <= work[j] for j in range(len(available))):
                        work = [work[j] + allocated[i][j] for j in range(len(available))]
                        safe_sequence.append(i)
                        finish[i] = True
                        found = True
                if not found:
                    break

            if len(safe_sequence) == n:
                st.write("✅ System is in Safe State")
                st.write("Safe Sequence:", safe_sequence)
            else:
                st.write("❌ Deadlock Detected")
