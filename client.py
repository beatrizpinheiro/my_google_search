import socket
import asyncio
import time

async def send_data(client, data):
    client.send(data)

async def run_client(msg1=None, msg2=None, msg3=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000

    client.connect((server_ip, server_port))

    try:
        welcome_msg = client.recv(4096).decode("utf-8")
        print(welcome_msg)

        while True:
            if msg1 is None:
                msg = input("Enter message: ")
                await send_data(client, msg.encode("utf-8")[:1024])
            else:
                await send_data(client, msg1.encode("utf-8")[:1024])
                response = await asyncio.to_thread(client.recv, 1024)
            

            if msg2 is not None:
                await send_data(client, msg2.encode("utf-8")[:1024])

            response = await asyncio.to_thread(client.recv, 1024)

            response = response.decode("utf-8")

            if response.lower() == "closed":
                break

            print(f"{response}")

            if msg3 is not None:
                await send_data(client, msg3.encode("utf-8")[:1024])
                response = await asyncio.to_thread(client.recv, 1024)
                response = response.decode("utf-8")
                if response.lower() == "closed":
                    break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")

if __name__ == "__main__":
    asyncio.run(run_client())