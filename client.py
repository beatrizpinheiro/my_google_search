import socket, time

def run_client(num_connections = 0, msg1 = None, msg2 = None, msg3 = None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    start_time = time.time()
    server_ip = "127.0.0.1"  
    server_port = 8000 
    client.connect((server_ip, server_port))

    try:
        welcome_msg = client.recv(4096).decode("utf-8")
        print(welcome_msg)

        while True:
            if msg1 is None:
                msg = input("Enter message: ")
                client.send(msg.encode("utf-8")[:1024])
            else:
                client.send(msg1.encode("utf-8")[:1024])
                
            if msg2 is not None:
                client.send(msg2.encode("utf-8")[:1024])

            response = client.recv(1024)
            end_time = time.time()

            response_time = end_time - start_time

            response = response.decode("utf-8")

            if response.lower() == "closed":
                break

            print(f"{response}")
            
            if msg3 is not None:
                client.send(msg3.encode("utf-8")[:1024])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")

        # Save time
        with open(f"response_times_{num_connections}.txt", "a") as f:
            f.write(f"{response_time}\n")


if __name__ == "__main__":
    run_client()