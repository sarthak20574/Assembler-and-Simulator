import matplotlib.pyplot as plt

cycle = 0
mem_acc = []
cyc = []


mem_addr = {}
PC_dict = {}
PC = 0
halt_occured = False

reg_dict = {"000": 0,
            "001": 0,
            "010": 0,
            "011": 0,
            "100": 0,
            "101": 0,
            "110": 0,
            "111": 0}


def main():
    while True:
        try:
            line = input()
            if line != "":
                global PC
                PC_dict[PC] = line
                PC += 1
        except EOFError:
            break


def execute():
    global PC
    instruction = PC_dict[PC]  # Xor or And ADD SUB  MUL  mnemonic reg reg reg
    global halt_occured

    if instruction[0:5] == "00000":  # +
        reg_dict[instruction[7:10]] = reg_dict[instruction[10:13]] + reg_dict[instruction[13:len(instruction)]]
        reg_dict["111"] = 0

        if reg_dict[instruction[7:10]] > 2 ** 16 - 1:
            reg_dict["111"] = 8

        a = f'{reg_dict[instruction[7:10]]:016b}'
        b = a[len(a) - 16:]
        reg_dict[instruction[7:10]] = int(b, 2)

    elif instruction[0:5] == "00001":  # -
        reg_dict["111"] = 0
        if reg_dict[instruction[10:13]] < reg_dict[instruction[13:len(instruction)]]:
            # overflow

            reg_dict[instruction[7:10]] = 0
            reg_dict["111"] = 8

        else:
            reg_dict[instruction[7:10]] = reg_dict[instruction[10:13]] - reg_dict[instruction[13:len(instruction)]]

    elif instruction[0:5] == "00110":  # *
        reg_dict["111"] = 0
        reg_dict[instruction[7:10]] = reg_dict[instruction[10:13]] * reg_dict[instruction[13:len(instruction)]]
        if reg_dict[instruction[7:10]] > 2 ** 16 - 1:
            reg_dict["111"] = 8

        a = f'{reg_dict[instruction[7:10]]:016b}'
        b = a[len(a) - 16:]
        reg_dict[instruction[7:10]] = int(b, 2)

    elif instruction[0:5] == "00111":  # /
        reg_dict[instruction["000"]] = reg_dict[instruction[10:13]] // reg_dict[instruction[13:len(instruction)]]
        reg_dict[instruction["001"]] = reg_dict[instruction[10:13]] % reg_dict[instruction[13:len(instruction)]]

    elif instruction[0:5] == "01100":  # and
        reg_dict[instruction[7:10]] = reg_dict[instruction[10:13]] & reg_dict[instruction[13:len(instruction)]]

    elif instruction[0:5] == "01011":  # or
        reg_dict[instruction[7:10]] = reg_dict[instruction[10:13]] | reg_dict[instruction[13:len(instruction)]]

    elif instruction[0:5] == "01010":  # xor
        reg_dict[instruction[7:10]] = reg_dict[instruction[10:13]] ^ reg_dict[instruction[13:len(instruction)]]

    elif instruction[0:5] == "01101":  # not
        ans = ""
        for i in f'{reg_dict[instruction[13:len(instruction)]]:016b}':
            if i == "0":
                ans += "1"
            else:
                ans += "0"
            reg_dict[instruction[10:13]] = int(ans, 2)

    elif instruction[0:5] == "01000":  # rs
        reg_dict[instruction[5:8]] = instruction[8:] >> 1

    elif instruction[0:5] == "01001":  # ls
        reg_dict[instruction[5:8]]= instruction[8:] << 1

    elif instruction[0:5] == "00010":  # move immediate
        reg_dict[instruction[5:8]] = int(instruction[8:], 2)

    elif instruction[0:5] == "00011":  # move reg
        reg_dict[instruction[10:13]] = reg_dict[instruction[13:]]
        if instruction[13:] == "111":
            reg_dict["111"]=0


    elif instruction[0:5] == "01110":  # cmp
        if reg_dict[instruction[10:13]] == reg_dict[instruction[13:]]:
            reg_dict["111"] = 1
        elif reg_dict[instruction[10:13]] > reg_dict[instruction[13:]]:
            reg_dict["111"] = 2
        else:
            reg_dict["111"] = 4



    elif instruction[0:5] == "00101":  # str
        mem_addr[instruction[8:]] = reg_dict[instruction[5:8]]

    elif instruction[0:5] == "00100":  # ld
        try:
            reg_dict[instruction[5:8]] = mem_addr[instruction[8:]]
        except:
            reg_dict[instruction[5:8]] = 0
    elif instruction[0:5] == "01111":  # jmp
        PC = (int(instruction[8:], 2)) - 1

    elif instruction[0:5] == "10000":  # jlt
        if reg_dict["111"] == 4:
            PC = (int(instruction[8:], 2)) - 1
        reg_dict["111"]=0

    elif instruction[0:5] == "10001":  # jgt
        if reg_dict["111"] == 2:
            PC = (int(instruction[8:], 2)) - 1
        reg_dict["111"] = 0

    elif instruction[0:5] == "10010":  # je
        if reg_dict["111"] == 1:
            PC = (int(instruction[8:], 2)) - 1
        reg_dict["111"] = 0

    elif instruction[0:5] == "10011":  # hlt
        halt_occured = True


def print_reg():
    for i in reg_dict:
        print(f'{reg_dict[i]:016b}', end=" ")
    print()


def update_PC():
    global PC
    PC += 1

def mem_dump():
    count = 1
    for i in PC_dict:
        print(PC_dict[i])
        count += 1

    for i in mem_addr:
        print(f'{mem_addr[i]:016b}')
        count += 1

    while count <= 256:
        print("0"*16)
        count += 1


def graph():
    plt.plot(mem_acc, cyc)

    plt.xlabel('Cycle')

    plt.ylabel('Address')

    plt.title('MemoryAccess vs Cycle')

    plt.show()

    plt.savefig('graph1.png')

def process():
    global PC
    global halt_occured
    global cycle

    while not halt_occured:
        execute()
        print(f'{PC:08b}', end=" ")

        print_reg()

        mem_acc.append(PC)
        update_PC()

        cyc.append(cycle)
        cycle += 1

    mem_dump()
    graph()


main()
PC = 0
process()
