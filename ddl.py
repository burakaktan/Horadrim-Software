from main import *

def create_type(inp):
    table_name = inp[2]
    f = open(f"{table_name}_1.txt", "wb+")
    table_name_extended = extend_to(20, table_name).encode("ascii")
    # 3 pages per file
    for i in range(3):
        # page header
        f.write("09002195".encode("ascii"))
        # 9 records per page
        for j in range(9):
            f.write(("012" + 240 * '$').encode("ascii"))
    # add to information schema
    written = False
    infor = open(f"information_schema.txt", "rb+")
    while not written:
        print("severim haa")
        data = infor.read(4)[-2:].decode("ascii")
        if data == '':
            add_new_page_to_information_schema(infor)
            continue
        no_empty = int(data)
        print("no empty:", no_empty)
        if no_empty != 0:
            infor.read(2384 - 4).decode("ascii")
        else:
            infor.read(4).decode("ascii")
            for i in range(8):
                valid = int(infor.read(1).decode("ascii"))
                if valid == 0:
                    infor.seek(infor.tell() - 1)
                    infor.write('1'.encode("ascii"))
                    infor.write(table_name_extended)
                    for field in range(12):
                        field_name = ""
                        field_type_name = ""
                        if not 3 + 2 * field >= len(inp):
                            field_name = inp[3 + 2 * field]
                            field_type_name = inp[3 + 2 * field + 1]
                        field_name_extended = extend_to(20, field_name)

                        infor.write((field_name_extended + field_type_name).encode("ascii"))
                    written = True
                    break
                else:
                    infor.read(296).decode("ascii")
    infor.close()


def list_type(inp, output_file_name):
    infor = open("information_schema.txt", "rb+")
    data = "a"
    out = open(output_file_name, "a")
    while True:
        data = infor.read(2384).decode("ascii")
        if len(data) == 0:
            break
        cursor = 8
        for i in range(8):
            if data[cursor] == '1':
                sub_ans = remove_dollar(data[cursor + 1:cursor + 21])
                cursor += 297
                out.write(sub_ans + '\n')
    infor.close()

def delete_type(inp):
    name = inp[2]
    name_extended = extend_to(20, name)
    infor = open("information_schema.txt", "rb+")

    var = True
    while var:
        data = infor.read(2384).decode("ascii")
        if len(data) == 0:
            break
        cursor = 8
        for i in range(8):
            if data[cursor] == '1' and data[cursor+1:cursor+21] == name_extended:
                print("tell is:",infor.tell())
                infor.seek(infor.tell()-2384 + 8 + i*297)
                infor.write("0".encode("ascii"))
                var = False
                break
            cursor += 297
    infor.close()