import time
import numpy as np
from client import run_client
import multiprocessing

def client_handler(num_connections, msg, msg2, msg3):
    run_client(num_connections, msg, msg2, msg3)

def simulate_connections(num_connections, duration):
    start_time = time.time()
    end_time = start_time + duration
    
    while time.time() < end_time:
        threads = []
        for i in range(num_connections):
            thread = multiprocessing.Process(target=client_handler, args=(num_connections, "4", 'teste', "5"))             # make a search
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        remaining_time = end_time - time.time()
        if remaining_time < 0:
            break
        
        time.sleep(1)
    
    with open(f"response_times_{num_connections_per_second}.txt", "r") as file:
        times = []
        for line in file:
            line = line.strip()
            if line:
                times.append(float(line))

    times = np.array(times)

    num_to_discard = int(len(times) * 0.05)

    times_sorted = np.sort(times)

    trimmed_times = times_sorted[num_to_discard:-num_to_discard]

    average_time = np.mean(trimmed_times)
    median_time = np.median(trimmed_times)
    std_deviation = np.std(trimmed_times)

    print("Average Time:", average_time)
    print("Median Time:", median_time)
    print("Standard Deviation:", std_deviation)

if __name__ == "__main__":
    num_connections_per_second = 50
    duration = 60
    
    simulate_connections(num_connections_per_second, duration)
