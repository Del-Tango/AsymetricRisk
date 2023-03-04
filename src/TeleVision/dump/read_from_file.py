#!/bin/python3

import os

def read_from_file(file_path, **kwargs):
    if not os.path.exists(file_path):
        print('File not found')
        return 1
    lines = []
    with open(file_path, mode='r', encoding='utf-8', errors='ignore') as active_file:
        lines = active_file.readlines()
    print('Content was read')
    if kwargs.get('cleanup'):
        with open(file_path, mode='w', encoding='utf-8', errors='ignore') as active_file:
            active_file.write('')
        print('File cleaned up')
    return lines

file_path = 'test_file.txt'
print(read_from_file(file_path))
input('Press any key to continue')
print(read_from_file(file_path))
input('Press any key to continue')
print(read_from_file(file_path, cleanup=True))
input('Press any key to continue')
