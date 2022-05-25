# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    input_file = open(input_file_name, 'r')
    input_lines = input_file.readlines()
    for inp in input_lines:
        inp = inp.split()
        # if query is DDL
        if inp[1] == 'type':
            if inp[0] == 'create':
                table_name = inp[2]
                f = open(f"{table_name}_1.txt", "wb")
                # 3 pages per file
                for i in range(3):
                    #page header
                    # 09 --> number of records in this page
                    # 00 --> number of active records (initially 0)
                    # 2195 --> number of bytes in the page
                    f.write("09002195")
                    # 9 records per page
                    for j in range(9):
                        # 0 --> this record is initially inactive
                        # 12 --> there are 12 fields in each record.
                        # 240*$ --> all records are filled with an exceptional character
                        f.write("012" + 240*'$')
            if inp[0] == 'delete':
            if inp[0] == 'list':
        # if query is DML
        else :

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
