from horadrimSoftware import *

catalog_page_header_size = 2 + 2 + 4 # record_number + active_record_number + total_size
catalog_page_record_number = 8
catalog_record_header_size = 1 + 20 + 2 # valid_bit + table_name + primary_key
catalog_record_body_size = 12*(20+3) # number of fields*(field_size + type_size)
catalog_record_size = catalog_record_header_size + catalog_record_body_size
catalog_page_size = catalog_page_header_size \
                    + catalog_page_record_number*(catalog_record_header_size + catalog_record_body_size)

max_field_number = 12
max_field_name_length = 20
max_field_length = 20
max_table_name_length = 20

def add_new_page_to_information_schema(infor):
    infor.write((str(catalog_page_record_number).zfill(2) + "00" + catalog_page_size).encode("ascii"))
    for j in range(8):
        infor.write(("0" + (catalog_record_size-1)*'$').encode("ascii"))

def create_type(inp):
    table_name = inp[2]
    table_name_extended = extend_to(max_table_name_length, table_name)
    primary_key = inp[3]
    # add to information schema
    written = False
    infor = open(f"information_schema.txt", "rb+")
    while not written:
        data = infor.read(4)[-2:].decode("ascii")
        if data == '':
            add_new_page_to_information_schema(infor)
            continue
        no_empty = int(data)
        print("no empty:", no_empty)
        if no_empty != 0:
            infor.read(catalog_page_size - 4).decode("ascii")
        else:
            infor.read(4).decode("ascii")
            for i in range(catalog_page_record_number):
                valid = int(infor.read(1).decode("ascii"))
                if valid == 0:
                    infor.seek(infor.tell() - 1)
                    infor.write('1'.encode("ascii"))
                    infor.write(table_name_extended)
                    infor.write(primary_key.zfill(2))
                    for field in range(max_field_number):
                        field_name = ""
                        field_type_name = ""
                        if not 4 + 2 * field >= len(inp):
                            field_name = inp[4 + 2 * field]
                            field_type_name = inp[4 + 2 * field + 1]
                        field_name_extended = extend_to(max_field_name_length, field_name)

                        infor.write((field_name_extended + field_type_name).encode("ascii"))
                    written = True
                    break
                else:
                    infor.read(catalog_record_size-1).decode("ascii")
    infor.close()


def list_type(inp, output_file_name):
    infor = open("information_schema.txt", "rb+")
    out = open(output_file_name, "a")
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
                out.write(sub_ans + '\n')
    infor.close()


def delete_type(inp):
    name = inp[2]
    name_extended = extend_to(max_table_name_length, name)
    infor = open("information_schema.txt", "rb+")

    var = True
    while var:
        data = infor.read(catalog_page_size).decode("ascii")
        if len(data) == 0:
            break
        cursor = catalog_page_header_size
        for i in range(catalog_page_record_number):
            if data[cursor] == '1' and data[(cursor + 1): (cursor + 1 + max_table_name_length)] == name_extended:
                print("tell is:", infor.tell())
                infor.seek(infor.tell() - catalog_page_size
                           + catalog_page_header_size + i*catalog_record_size)
                infor.write("0".encode("ascii"))
                var = False
                break
            cursor += catalog_record_size
    infor.close()
