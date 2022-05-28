"""
TODO:
    - print the logs
    - look at the report
"""

from horadrimSoftware import *
from bplustree.tree import BPlusTree
from bplustree.serializer import StrSerializer
from ddl import *
import os

max_field_length = 20
max_field_number = 12
max_field_name_length = 20
max_table_name_length = 20

pages_per_file = 3
page_header_size = 8  # 2(number_of_records) + 2(number_of_active_records) + 4(total_size)
records_per_page = 9
record_header_size = 3  # 1(valid_bit) + 2(number_of_fields)
record_body_size = max_field_number * max_field_length
record_size = record_body_size + record_header_size
page_size = page_header_size + records_per_page * record_size


def extend_to(l, s):
    return s + (l - len(s)) * '$'


def remove_dollar(s):
    ns = ""
    for ch in s:
        if ch != '$':
            ns += ch
    return ns


def create_fill_file(filename):
    infor = open(filename, "w")
    infor.close()
    infor = open(filename, "rb+")
    for i in range(pages_per_file):
        infor.write((str(records_per_page).zfill(2)+"00"+str(page_size).zfill(4)).encode("ascii"))
        for j in range(records_per_page):
            infor.write(("0"+"00"+max_field_number*max_field_length*'$').encode("ascii"))
    infor.close()


def add_to_file(filename, inp):
    infor = open(filename, "rb+")
    to_return = -1
    for i in range(pages_per_file):
        if to_return != -1:
            break
        data = infor.read(page_size).decode("ascii")
        active_records = int(data[2:4])
        if active_records < records_per_page:
            cursor = page_header_size
            for j in range(records_per_page):
                if data[cursor] != '0':
                    cursor += record_size
                else:
                    number_of_fields = len(inp)-3
                    write = "1" + str(number_of_fields).zfill(2)
                    for k in range(number_of_fields):
                        write += extend_to(max_field_length, inp[3+k])
                    for k in range(12-number_of_fields):
                        write += max_field_length*'$'
                    infor.seek(infor.tell()-page_size+page_header_size+j*record_size)
                    to_return = infor.tell()
                    infor.write(write.encode("ascii"))
                    # change number of active records
                    infor.seek(i*page_size+2)
                    infor.write(str(active_records+1).zfill(2).encode("ascii"))
                    infor.close()
                    return to_return
    infor.close()
    return to_return


def getFileList(table_name):
    all_files = os.listdir(".")
    related_files = []
    for file in all_files:
        if ".txt" in file and file.find(table_name+"_") == 0:
            related_files.append(file)
    return related_files


# data is a byte array
def get_data_from_record(data):
    is_valid = int(data[0])
    number_of_fields = int(data[1:3])
    cursor = 3
    ans = ""
    for i in range(number_of_fields):
        ans += remove_dollar(data[cursor:cursor+max_field_length]) + " "
        cursor += max_field_length
    return ans


def check_empty(file_name):
    empty_records_in_file = 0
    infor = open(file_name,"rb+")
    for i in range(pages_per_file):
        empty_records_in_page = int(infor.read(page_size).decode("ascii")[2:4])
        empty_records_in_file += empty_records_in_page
    infor.close()
    if empty_records_in_file == pages_per_file*records_per_page:
        os.remove(file_name)


def create_record(inp):
    table_name = inp[2]
    table_name_extended = extend_to(20, table_name)
    mx = 1
    # file_name and byte where we added the record
    added_file = ""
    added_byte = 0
    related_files = getFileList(table_name)
    for file in related_files:
        num_as_str = ""
        for ch in file:
            if '9' >= ch >= '0':
                num_as_str += ch
        mx = max(mx, int(num_as_str))
    result = -1
    for file_name in related_files:
        result = add_to_file(file_name, inp)
        if result != -1:
            added_file = file_name
            added_byte = result
            break
    if result == -1:
        new_file_name = table_name+"_"+str(mx)+".txt"
        create_fill_file(new_file_name)
        result = add_to_file(new_file_name, inp)
        added_file = new_file_name
        added_byte = result
    tree = BPlusTree("./bp_"+table_name+".txt", key_size=20, serializer = StrSerializer(), order = 50)
    pk = inp[2+get_primary_key(table_name)]
    print("pk is:", pk)
    tree[pk] = ("1" + added_file + "," + str(added_byte)).encode("ascii")
    tree.close()


def list_record(inp, output_file_name):
    table_name = inp[2]
    table_name_extended = extend_to(20, table_name)
    outputs = []
    related_files = getFileList(table_name)
    pk = get_primary_key(table_name)
    for filename in related_files:
        infor = open(filename, "rb+")
        page_data = infor.read(page_size).decode("ascii")
        cursor = page_header_size
        for i in range(records_per_page):
            if page_data[cursor] == '1':
                sub_ans = get_data_from_record(page_data[cursor:cursor+record_size])
                sub_key = sub_ans.split(" ")[pk-1]
                print("sub key is: ",sub_key)
                outputs.append([sub_key,sub_ans])
            cursor += record_size
        infor.close()
    out = open(output_file_name, "a")
    outputs.sort()
    for o in outputs:
        out.write(o[1]+"\n")
    out.close()


def update_record(inp):
    table_name = inp[2]
    pk = inp[3]
    tree = BPlusTree("./bp_"+table_name+".txt", key_size=20, serializer=StrSerializer(),order = 50)
    storage = tree.get(str(pk)).decode("utf-8")[1:].split(",")
    infor = open(storage[0], "rb+")
    infor.seek(int(storage[1]) + record_header_size)
    for field in inp[4:]:
        infor.write(extend_to(20, field).encode("ascii"))
    infor.close()
    tree.close()


def search_record(inp, output_file_name):
    table_name = inp[2]
    pk = inp[3]
    tree = BPlusTree("./bp_"+table_name+".txt", key_size=20, serializer=StrSerializer(), order = 50)
    storage = tree.get(str(pk)).decode("utf-8")[1:].split(",")
    tree.close()

    infor = open(storage[0], "rb+")
    out = open(output_file_name, "a")
    infor.seek(int(storage[1]))
    data = infor.read(record_size).decode("ascii")
    infor.close()

    out.write(get_data_from_record(data) + "\n")
    out.close()


def filter_record(inp, output_file_name):
    table_name = inp[2]
    pk = inp[3]
    cond = inp[4]
    operand = inp[5]
    outputs = []

    pk_type = get_primary_key_type(table_name)
    print("pk type is: ", pk_type)
    tree = BPlusTree("./bp_"+table_name+".txt", key_size=20, serializer=StrSerializer(), order = 50)
    for key, value in tree.items():
        _key = key
        if pk_type == "int":
            operand = int(operand)
            _key = int(_key)
        holds = False
        if cond == '<' and _key < operand:
            holds = True
        if cond == '>' and _key > operand:
            holds = True
        if cond == '=' and _key == operand:
            holds = True
        if holds:
            _value = value[1:]
            storage = _value.decode("utf-8").split(",")
            infor = open(storage[0], "rb+")

            infor.seek(int(storage[1]))
            data = infor.read(record_size).decode("ascii")
            infor.close()
            outputs.append([_key, get_data_from_record(data)])
    tree.close()
    out = open(output_file_name, "a")
    outputs.sort()
    for i in range(len(outputs)):
        out.write(outputs[i][1] + "\n")
    out.close()

def delete_record(inp):
    table_name = inp[2]
    pk = inp[3]
    tree = BPlusTree("./bp_"+table_name+".txt", key_size=20, serializer=StrSerializer(), order = 50)
    is_alive = tree.get(pk)[0]
    storage = tree.get(pk).decode("utf-8")[1:].split(",")
    tree[pk] = "0".encode("ascii")
    tree.close()
    infor = open(storage[0], "rb+")
    infor.seek(int(storage[1]))
    infor.write("0".encode("ascii"))
    curr_page = int(storage[1])//page_size
    infor.seek(curr_page*page_size+2)
    no_active_records = int(infor.read(2).decode("ascii"))-1
    infor.seek(infor.tell()-2)
    infor.write(str(no_active_records).zfill(2).encode("ascii"))
    infor.close()
    check_empty(storage[0])
