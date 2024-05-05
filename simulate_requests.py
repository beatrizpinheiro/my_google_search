import asyncio, time

async def client_task(server_ip, server_port, num_clients, msg1=None, msg2=None, msg3=None):
    try:
        start_time = time.time()
        reader, writer = await asyncio.open_connection(server_ip, server_port)

        welcome_msg = await reader.read(4096)
        print(welcome_msg.decode("utf-8"))

        while True:
            if msg1 is None:
                msg = input("Enter message: ")
                writer.write(msg.encode("utf-8")[:1024])
                await writer.drain()
            else:
                writer.write(msg1.encode("utf-8")[:1024])
                await writer.drain()
                response = await reader.read(1024)
                print(response.decode("utf-8"))

            if msg2 is not None:
                writer.write(msg2.encode("utf-8")[:1024])
                await writer.drain()

                response = await reader.read(1024)
                print(response.decode("utf-8"))

            if msg3 is not None:
                writer.write(msg3.encode("utf-8")[:1024])
                await writer.drain()

                response = await reader.read(1024)
                print(response.decode("utf-8"))

                if response.lower() == "closed":
                    break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Connection to server closed")
        response_time = time.time() - start_time
        with open(f"response_times_{int(num_clients/60)}.txt", "a") as f:
            f.write(f"{response_time}\n")


async def run_clients(server_ip, server_port, num_clients, msg1=None, msg2=None, msg3=None):
    tasks = []
    for i in range(num_clients):
        if i%(num_clients/60) == 0:
            time.sleep(1)
        task = asyncio.create_task(client_task(server_ip, server_port, num_clients, msg1, msg2, msg3))
        tasks.append(task)
        await asyncio.sleep(1 / num_clients)  # Adjust timing for desired requests per second

    await asyncio.gather(*tasks)


async def main():
    server_ip = "127.0.0.1"
    server_port = 8000

    num_connections_per_second = 50
    num_clients = num_connections_per_second*60
    msg1 = "4"
    msg2 = "quantos"
    msg3 = "5"

    await run_clients(server_ip, server_port, num_clients, msg1, msg2, msg3)

if __name__ == "__main__":
    asyncio.run(main())