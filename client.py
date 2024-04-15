import socket, time, statistics

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  
    server_port = 8000 
    client.connect((server_ip, server_port))

    response_times = []  # Store response times

    try:
        welcome_msg = client.recv(4096).decode("utf-8")
        print(welcome_msg)

        while True:
            msg = input("Enter message: ")
            start_time = time.time()
            client.send(msg.encode("utf-8")[:1024])

            response = client.recv(1024)
            end_time = time.time()

            response_time = end_time - start_time
            response_times.append(response_time)

            response = response.decode("utf-8")

            if response.lower() == "closed":
                break

            print(f"{response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")

        # Calculate statistics
        response_times.sort()
        num_responses = len(response_times)
        lower_bound = int(num_responses * 0.05)
        upper_bound = num_responses - lower_bound
        trimmed_response_times = response_times[lower_bound:upper_bound]
        median = statistics.median(trimmed_response_times)
        std_dev = statistics.stdev(trimmed_response_times)
        print(f"Median response time: {median} seconds")
        print(f"Standard deviation of response times: {std_dev} seconds")

run_client()