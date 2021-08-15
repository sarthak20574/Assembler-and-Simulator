addr = 0
string_list = []
var_dict = {}
label_dict = {}
line_number=1
halt_occured=False

def process():
    for i in string_list:
        arr = i.split()
        checking(arr)


reg_dict = {"R0": "000",
            "R1": "001",
            "R2": "010",
            "R3": "011",
            "R4": "100",
            "R5": "101",
            "R6": "110",
            "FLAGS": "111"}
inst_dict = {"add": "00000",
             "sub": "00001",
             "movI": "00010",
             "movR": "00011",
             "ld": "00100",
             "st": "00101",
             "mul": "00110",
             "div": "00111",
             "rs": "01000",
             "ls": "01001",
             "xor": "01010",
             "or": "01011",
             "and": "01100",
             "not": "01101",
             "cmp": "01110",
             "jmp": "01111",
             "jlt": "10000",
             "jgt": "10001",
             "je": "10010",
             "hlt": "10011"}


def checking(arr):
    global halt_occured
    if halt_occured:
        print("Halt has occured can't take anymore statements")
        exit()

    result = ""
   
    global line_number


    if arr[0][-1] == ":":
        arr = arr[1:]

    length = len(arr)


    if length == 2:
        if arr[0] in inst_dict:  # Type E
            result += inst_dict[arr[0]] + "0"*3 + f'{label_dict[arr[1]]:08b}'
        else:
            print("This is not a type E statement but is 2 letters long, error at line number: "+str(line_number+len(var_dict)))
            exit()
    elif length == 3:
        if arr[0] == "mov" and arr[2][0] == "$" and arr[1] in reg_dict:  # Type B
            result += "00010" + reg_dict[arr[1]] + f'{int(arr[2][1:]):08b}'

        elif arr[0] in inst_dict and arr[2][0] == "$" and arr[1] in reg_dict:  # Type B rs and ls
            result += inst_dict[arr[0]] + reg_dict[arr[1]] + f'{int(arr[2][1:]):08b}'

        elif arr[0] == "mov" and arr[2] in reg_dict and arr[1] in reg_dict:  # Type C -->
            result += "00011" + "00000" + reg_dict[arr[1]] + reg_dict[arr[2]]

        elif arr[0] in inst_dict and arr[2] in reg_dict and arr[1] in reg_dict:  # Type C -->
            result += inst_dict[arr[0]] + "00000" + reg_dict[arr[1]] + reg_dict[arr[2]]

        elif arr[0] in inst_dict and arr[1] in reg_dict and arr[2] in var_dict:
            result += inst_dict[arr[0]] + reg_dict[arr[1]] + f'{var_dict[arr[2]]:08b}'
        else:
            print("This is not a type B or C statement but is 3 letters long, error at line number: "+str(line_number+len(var_dict)))
            exit()

    elif length == 4:
        if arr[0] in inst_dict and arr[1] in reg_dict and arr[2] in reg_dict:  # Type A
            result += inst_dict[arr[0]] + "00" + reg_dict[arr[1]] + reg_dict[arr[2]] + reg_dict[arr[3]]
        else:
            print("This is not a type A statement but is 3 letters long, error at line number: "+str(line_number+len(var_dict)))
            exit()

    elif length == 1:
        if arr[0] in inst_dict:
            result += inst_dict[arr[0]] + "0" * 11
            halt_occured=True
    else:
        print("syntax error at line number: "+str(line_number+len(var_dict)))
        exit()
    line_number+=1
    print(result)


def main():
    while True:
        try:
            line = input()
            if line != "":
                ln = line.strip()
                if not ln[0:3] == "var":
                    string_list.append(ln)
                global line_number


                Ln = ln.split()
                if Ln[0] == "var":
                    try:
                        var_dict[Ln[1]] = 0
                    except:
                        print("Pass the variable name at line number "+ str(line_number))
                        exit()
                    

                    # label:
                else:
                    global addr
                    if Ln[0][-1] == ":":
                        label_dict[Ln[0][0:-1]] = addr
                    addr += 1

        except EOFError:
            break


def substituting_var_address():
    c = 0
    for i in var_dict:
        var_dict[i] = addr + c
        c += 1


if __name__ == "__main__":
    
    main()
    substituting_var_address()
    process()  # perform some operation(s) on given string
