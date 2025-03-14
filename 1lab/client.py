import socket
import struct
import xml.etree.ElementTree as ET


def print_directory_tree(element, prefix=""):
    for sub_elem in element.findall('directoryItem'):
        path = sub_elem.get('path')
        print(prefix + " ├── " + path)

        inner_prefix = prefix + "│   "
        for dir_name in sub_elem.findall('directoryName'):
            print(inner_prefix + "├── " + dir_name.text)

        for file_name in sub_elem.findall('fileName'):
            print(inner_prefix + "└── " + file_name.text)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 45334))

    while True:
        command = input("Введите команду: cd + путь / dir_s / close ")

        if command.strip().lower() == "close":
            print('stopp')
            client_socket.close()
            exit()

        client_socket.send(command.encode())

        if command.upper() == "DIR_S":
            length_data = client_socket.recv(4)
            if not length_data:
                print('Ошибка получения длины файла.')
                break
            file_length = struct.unpack('!I', length_data)[0]

            data = b''
            while len(data) < file_length:
                part = client_socket.recv(4096)
                if not part:
                    break
                data += part

            with open('received_structure.xml', 'wb') as file:
                file.write(data)
            print('Структура директории получена и сохранена в received_structure.xml')

            tree = ET.parse('received_structure.xml')
            root = tree.getroot()
            print_directory_tree(root)

        else:
            response = client_socket.recv(1024).decode()
            print(response)

    client_socket.close()


if __name__ == "__main__":
    main()
