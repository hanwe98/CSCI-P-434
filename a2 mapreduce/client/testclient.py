import xmlrpc.client

option = 0

filename = "book.txt"
with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
    proxy.init_cluster(2, 10)
    handle = open(filename, "rb")
    binary_data = xmlrpc.client.Binary(handle.read())
    proxy.server_receive_file(binary_data)
    



# while (option != 'q'): 
#     option = input("Type 1 to perform word count. Type 2 to perform inverted index. Type q to quit: ")
#     if option == '1':
#         filename = input("Please enter the filename with file extension (for e.g. book.txt): ")
#         with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
#             handle = open(filename, "rb")
#             binary_data = xmlrpc.client.Binary(handle.read())
#             proxy.server_receive_file(binary_data)
#     elif option == '2':
#         # inverted index will be implemented here.
#         print("inverted index will be implemented here.")
#     elif option == 'q':
#         print("Connection closed.")
#     else:
#         print("This functionality is not supported yet")
