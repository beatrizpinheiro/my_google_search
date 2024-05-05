import asyncio, socket
from my_google_search import MyGoogleSearch

WELCOME_MESSAGE = """
        Welcome to the MyGoogle Search server!

        Please choose one of the options below by typing the corresponding number:

        1. Upload files to be indexed for future searches;
        2. Remove a file from the system;
        3. List all inserted files;
        4. Perform a keyword search;
        5. Exit.

        Enter the number of the desired option and press Enter:
        """

async def handle_client(client_socket, addr, search_engine):
    try:
        client_socket.send(WELCOME_MESSAGE.encode("utf-8"))
        while True:
            request = await asyncio.to_thread(client_socket.recv, 1024)
            request = request.decode("utf-8")

            if request.lower() == "5":
                client_socket.send("closed".encode("utf-8"))
                break

            if request == "1":
                client_socket.send("Provide the path of the file to be uploaded".encode("utf-8"))
                path = await asyncio.to_thread(client_socket.recv, 1024)
                path = path.decode("utf-8")
                response = await search_engine.upload_file(path)

            elif request == "2":
                client_socket.send("Provide the title of the file to be removed".encode("utf-8"))
                title = await asyncio.to_thread(client_socket.recv, 1024)
                title = title.decode("utf-8")
                response = await search_engine.remove_file(title)            

            elif request == "3":
                titles = str(await search_engine.list_files())
                formatted_titles = [f"{i+1}. {title}" for i, title in enumerate(titles.split("\n"))]
                response = "\n".join(formatted_titles)
                
            elif request == "4":
                client_socket.send("Provide the search query".encode("utf-8"))
                search_query = await asyncio.to_thread(client_socket.recv, 1024)
                search_query = search_query.decode("utf-8")
                total_files, relevant_files = await search_engine.search(search_query)
                response = f"{total_files} files were found\n" if total_files != 1 else f"{total_files} file was found\n"
                if relevant_files:
                    response += '\n'.join([f"{i+1}. {file['title']}" for i, file in enumerate(relevant_files)])
  
            client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


async def run_server():
    server_ip = "127.0.0.1"
    port = 8000

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        search_engine = MyGoogleSearch()
        await search_engine.load_data()

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            await asyncio.create_task(handle_client(client_socket, addr, search_engine))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    asyncio.run(run_server())