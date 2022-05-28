# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from src.ddl import *
from src.dml import *
from bplustree.tree import BPlusTree
from bplustree.serializer import StrSerializer
import os
import sys
import time

from src.dml import filter_record

def get_ocurrence():
    return int(time.time())


def extend_to(l, s):
    return s + (l - len(s)) * '$'


def log(_inp, result):
    if _inp[-1] == '\n':
        _inp = _inp[:-1]
    infor = open("horadrimLog.csv", "a")
    status = "success"
    if not result:
        status = "failure"
    infor.write(str(get_ocurrence()) + "," + _inp + "," + status + "\n")
    infor.close()


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

    # open/close output file to cleaning
    infor = open(output_file_name, "w")
    infor.close()

    input_file = open(input_file_name, 'r')
    input_lines = input_file.readlines()
    # create information_schema table if not exist
    if not os.path.exists('information_schema.txt'):
        infor = open(f"information_schema.txt", "wb+")
        add_new_page_to_information_schema(infor)
        infor.close()

    for _inp in input_lines:
        print("executing:", _inp)
        inp = _inp.split()
        # if query is DDL
        if inp[1] == 'type':
            if inp[0] == 'create':
                log(_inp, create_type(inp))
            if inp[0] == 'delete':
                log(_inp, delete_type(inp))
            if inp[0] == 'list':
                log(_inp, list_type(inp, output_file_name))

        # if query is DML
        else :
            if inp[0] == 'create':
                log(_inp, create_record(inp))
            if inp[0] == 'list':
                log(_inp, list_record(inp, output_file_name))
            if inp[0] == 'update':
                log(_inp, update_record(inp))
            if inp[0] == 'search':
                log(_inp, search_record(inp, output_file_name))
            if inp[0] == 'filter':
                new_inp = []
                for i in range(len(inp)):
                    if "<" in inp[i] or ">" in inp[i] or "=" in inp[i]:
                        yeni = ""
                        for ch in inp[i]:
                            if ch in "<>=":
                                new_inp.append(yeni)
                                new_inp.append(ch)
                                yeni = ""
                            else:
                                yeni += ch
                        new_inp.append(yeni)
                    else:
                        new_inp.append(inp[i])
                log(_inp, filter_record(new_inp, output_file_name))
            if inp[0] == 'delete':
                log(_inp, delete_record(inp))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
