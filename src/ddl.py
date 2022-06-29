from horadrimSoftware import *
import os
from bplustree import BPlusTree
from bplustree import StrSerializer

max_field_number = 12
max_field_name_length = 20
max_field_length = 20
max_table_name_length = 20

catalog_page_header_size = 2 + 2 + 4 # record_number + active_record_number + total_size
catalog_page_record_number = 8
catalog_record_header_size = 1 + max_table_name_length + 2 # valid_bit + table_name + primary_key
catalog_record_body_size = max_field_number*(max_field_name_length+3) # number of fields*(field_size + type_size)
catalog_record_size = catalog_record_header_size + catalog_record_body_size
catalog_page_size = catalog_page_header_size \
                    + catalog_page_record_number*(catalog_record_header_size + catalog_record_body_size)

def extend_to(l,s):
    return s + (l - len(s)) * '$'


def remove_dollar(s):
    ns = ""
    for ch in s:
        if ch != '$':
            ns += ch
    return ns


def add_new_page_to_information_schema():
    infor = open(f"information_schema.txt", "ab+")
    infor.write((str(catalog_page_record_number).zfill(2) + "00" + str(catalog_page_size)).encode("ascii"))
    for j in range(8):
        infor.write(("0" + (catalog_record_size-1)*'$').encode("ascii"))
    infor.close()


def create_type(inp):
    try:
        table_name = inp[2]
        table_name_extended = extend_to(max_table_name_length, table_name)
        number_of_fields = inp[3]
        primary_key = inp[4]

        # create edilen her file icin B+ tree olusturuyoruz, eger B+ tree'si onceden varsa yeniden create etmiyoruz
        if os.path.exists("./bp_" + table_name + ".txt"):
            return False
        tree = BPlusTree("./bp_" + table_name + ".txt", key_size=20, serializer=StrSerializer(), order = 50)
        tree.close()
        # add to information schema
        written = False
        infor = open(f"information_schema.txt", "rb+")
        current_page = 0
        while not written:
            data = infor.read(4)[-2:].decode("ascii")
            if data == '':
                add_new_page_to_information_schema()
                continue
            no_filled = int(data)
            if no_filled == catalog_page_record_number:
                infor.read(catalog_page_size - 4).decode("ascii")
            else:
                infor.read(4).decode("ascii")
                for i in range(catalog_page_record_number):
                    is_filled = int(infor.read(1).decode("ascii"))
                    if is_filled == 0:
                        infor.seek(infor.tell() - 1)
                        infor.write('1'.encode("ascii"))
                        infor.write(table_name_extended.encode("ascii"))
                        infor.write(primary_key.zfill(2).encode("ascii"))
                        for field in range(max_field_number):
                            field_name = ""
                            field_type_name = ""
                            if not 5 + 2 * field >= len(inp):
                                field_name = inp[5 + 2 * field]
                                field_type_name = inp[5 + 2 * field + 1]
                            field_name_extended = extend_to(max_field_name_length, field_name)
                            infor.write((field_name_extended + field_type_name).encode("ascii"))
                        written = True
                        # edit number of filled entries
                        back_up = infor.tell()
                        infor.seek(catalog_page_size*current_page + 2)
                        infor.write(str(no_filled+1).zfill(2).encode("ascii"))
                        infor.seek(back_up)
                        break
                    else:
                        infor.read(catalog_record_size-1).decode("ascii")
                current_page += 1
        infor.close()
        return True
    except:
        return False

def list_type(inp, output_file_name):
    try:
        infor = open("information_schema.txt", "rb+")
        outputs = []
        while True:
            data = infor.read(catalog_page_size).decode("ascii")
            if len(data) == 0:
                break
            cursor = catalog_page_header_size
            for i in range(catalog_page_record_number):
                # if valid bit is 1ss
                if data[cursor] == '1':
                    sub_ans = remove_dollar(data[(cursor + 1): (cursor + 1 + max_table_name_length)])
                    cursor += catalog_record_size
                    outputs.append(sub_ans)
        infor.close()
        out = open(output_file_name, "a")
        outputs.sort()
        for o in outputs:
            out.write(o+"\n")
        out.close()
        return len(outputs) != 0
    except:
        return False


def delete_type(inp):
    try:
        name = inp[2]
        name_extended = extend_to(max_table_name_length, name)

        # first check whether table exists, if it's not, return False
        if not os.path.exists("bp_"+name+".txt"):
            return False
        infor = open("information_schema.txt", "rb+")
        var = True
        while var:
            data = infor.read(catalog_page_size).decode("ascii")
            if len(data) == 0:
                break
            cursor = catalog_page_header_size
            for i in range(catalog_page_record_number):
                if data[cursor] == '1' and data[(cursor + 1): (cursor + 1 + max_table_name_length)] == name_extended:
                    infor.seek(infor.tell() - catalog_page_size
                            + catalog_page_header_size + i*catalog_record_size)
                    infor.write("0".encode("ascii"))
                    var = False
                    break
                cursor += catalog_record_size
        infor.close()
        all_files = os.listdir(".")
        related_files = []
        for file in all_files:
            if ".txt" in file and file.find(name+"_") == 0:
                related_files.append(file)
            if file.find("bp_"+name+".txt") == 0:
                related_files.append(file)
        for filename in related_files:
            os.remove(filename)
        return True
    except:
        return False


def get_primary_key(table_name):
    infor = open("information_schema.txt", "rb+")
    while True:
        data = infor.read(catalog_page_size).decode("ascii")
        if len(data) == 0:
            break
        cursor = catalog_page_header_size
        for i in range(catalog_page_record_number):
            # if valid bit is 1 and table is the table we search
            if data[cursor] == '1' and table_name == remove_dollar(data[(cursor+1):(cursor+1+max_table_name_length)]):
                infor.close()
                return int(data[cursor+1+max_table_name_length:cursor+1+max_table_name_length+2])
            cursor += catalog_record_size
    infor.close()
    return -1

def get_primary_key_type(table_name):
    infor = open("information_schema.txt", "rb+")
    while True:
        data = infor.read(catalog_page_size).decode("ascii")
        if len(data) == 0:
            break
        cursor = catalog_page_header_size
        for i in range(catalog_page_record_number):
            # if valid bit is 1 and table is the table we search
            if data[cursor] == '1' and table_name == remove_dollar(data[(cursor+1):(cursor+1+max_table_name_length)]):
                infor.close()
                cursor += 21
                place = int(data[cursor:cursor+2]) - 1
                cursor += 2
                cursor += 23*place+20
                return data[cursor:cursor+3]
            cursor += catalog_record_size
    infor.close()
    return -1
