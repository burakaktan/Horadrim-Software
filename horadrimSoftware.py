# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import os
from ddl import *
from dml import *

def extend_to(l,s):
    return s + (l - len(s)) * '$'

def remove_dollar(s):
    ns = ""
    for ch in s:
        if ch != '$':
            ns += ch
    return ns

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    input_file = open(input_file_name, 'r')
    input_lines = input_file.readlines()
    #create information_schema table if not exist
    if not os.path.exists('information_schema.txt'):
        infor = open(f"information_schema.txt", "wb+")
        add_new_page_to_information_schema(infor)
        infor.close()

    for inp in input_lines:
        inp = inp.split()
        # if query is DDL
        if inp[1] == 'type':
            if inp[0] == 'create':
                create_type(inp)
            if inp[0] == 'delete':
                delete_type(inp)
            if inp[0] == 'list':
                list_type(inp, output_file_name)

        # if query is DML
        else :
            if inp[0] == 'create':
                create_record(inp)
            if inp[0] == 'delete':
                pass
            if inp[0] == 'list':
                pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
