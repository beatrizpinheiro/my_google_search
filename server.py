import socket, threading
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


def handle_client(client_socket, addr):
    try:
        client_socket.send(WELCOME_MESSAGE.encode("utf-8"))
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "5":
                client_socket.send("closed".encode("utf-8"))
                break

            my_google_search = MyGoogleSearch()

            # upload file
            if request == "1":
                client_socket.send("Provide the path of the file to be uploaded".encode("utf-8"))
                path = client_socket.recv(1024).decode("utf-8")
                response = my_google_search.upload_file(path)
                response = "File uploaded successfully" if response == 0 else "Path not located"

            # remove file
            if request == "2":
                client_socket.send("Provide the title of the file to be removed".encode("utf-8"))
                title = client_socket.recv(1024).decode("utf-8")
                response = my_google_search.remove_file(title)
                response = "File removed successfully" if response == 0 else "File not found"
            
            # list files
            if request == "3":
                titles = str(my_google_search.list_files())
                formatted_titles = [f"{i+1}. {title}" for i, title in enumerate(titles.split("\n"))]
                response = "\n".join(formatted_titles)

            # search
            if request == "4":
                client_socket.send("Provide the search query".encode("utf-8"))
                search_query = client_socket.recv(1024).decode("utf-8")
                total_files, relevant_files = my_google_search.search(search_query)
                response = f"{total_files} files were found\n" if total_files != 1 else f"{total_files} file was found\n"
                if relevant_files:
                    response += f"{len(relevant_files)} first relevant files:\n"
                    for i, file in enumerate(relevant_files):
                        response += f"{i+1}. {file['title']}\n"

            client_socket.send(response.encode("utf-8"))


    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "127.0.0.1"
    port = 8000

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((server_ip, port))

        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()