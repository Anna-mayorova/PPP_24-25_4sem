import os
import socket
import xml.etree.ElementTree as ET
import struct


def build_directory_structure(root_path):
    root_element = ET.Element("directory")
    for path, dirs, files in os.walk(root_path):
        dir_elem = ET.SubElement(root_element, "directoryItem", path=path)
        for dir_name in dirs:
            ET.SubElement(dir_elem, "directoryName").text = dir_name
        for file_name in files:
            ET.SubElement(dir_elem, "fileName").text = file_name
    return root_element


def save_to_xml(structure, file_name='directory_structure.xml'):
    tree = ET.ElementTree(structure)
    tree.write(file_name, xml_declaration=True, encoding='utf-8')


def process_client_request(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break

        if command.startswith('cd '):
            new_directory = command.split(" ")[1]
            if os.path.isdir(new_directory):
                dir_structure = build_directory_structure(new_directory)
                save_to_xml(dir_structure)
                response_message = f'Установлена новая корневая директория: {new_directory}'
            else:
                response_message = f'Ошибка: директория "{new_directory}" не найдена.'

        elif command == 'dir_s':
            file_name = 'directory_structure.xml'
            with open(file_name, 'rb') as file:
                data = file.read()
                client_socket.send(struct.pack('!I', len(data)))
                client_socket.send(data)
            print(f'Файл "{file_name}" отправлен клиенту.')
            continue
        else:
            response_message = 'Неверная команда'

        client_socket.send(response_message.encode('utf-8'))


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 45334))
    server_socket.listen(5)
    print('Сервер запущен')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Клиент: {client_address}')
        process_client_request(client_socket)
        client_socket.close()


def start():
    current_directory = os.getcwd()
    initial_structure = build_directory_structure(current_directory)
    save_to_xml(initial_structure)
    run_server()


if __name__ == "__main__":
    start()
