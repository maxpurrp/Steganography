import os
def _output_byte(byte, ind) -> bytes:
    if ind == '0':
        #if the bit being changed is 0
        if bin(byte)[-2] == '0':
            byte = byte | 0b00000001
        else:
            byte = byte & 0b11111101
            byte = byte | 0b00000001
    if ind == '1':
        #if the bit being changed is 1
        if bin(byte)[-2] == '1':
            byte = byte | 0b00000011
        else:
            byte = byte & 0b11111101
            byte = byte | 0b00000011
    return byte

def encoding(text):
    #Text-to-image encoding
    with open('test.bmp', 'rb') as start_pic:
        str = open('text.txt', 'w')
        str.write(text)
        if os.stat('text.txt').st_size > os.stat('test.bmp').st_size:
            print('text size is to big')
            exit()
        with open('update.bmp', 'wb') as final_pic:
            pict_info = start_pic.read(54)
            #first 54 byte is info about picture in .bmp
            final_pic.write(pict_info)
            for elem in text:
                cu_ascii_list = format(ord(elem), '08b')
                for ind in cu_ascii_list:
                    cur_byte = int.from_bytes(start_pic.read(1), byteorder='little')
                    cur_byte = _output_byte(cur_byte, ind)
                    final_pic.write(cur_byte.to_bytes(1, byteorder='little'))
            final_pic.write(start_pic.read())

def decoding():
    #decoding str from picture 
    with open('update.bmp', 'rb') as pict:
        symbol = ''
        pict_info = pict.read(54)
        byte = int.from_bytes(pict.read(1),byteorder='little')
        while bin(byte)[-1] == '1':
                symbol +=(bin(byte)[-2])
                byte = int.from_bytes(pict.read(1),byteorder='little')
    word = ''
    bin_ascii_list = []
    for elem in symbol:
        word += elem
        if len(word) == 8:
            bin_ascii_list.append(word)
            word = ''
            symbol = symbol[8:]
    output = ''
    for elem in bin_ascii_list:
        #chr() take 2 arguments - str and what number system is the number in
        symb = ''.join(chr(int(elem, 2)))
        output += symb
    print(f'output message is: {output}')

def main():
    choise = input('1 - encoding | 2 - decoding ')
    if choise == '1':
        text = input()
        encoding(text)
    if choise == '2':
        decoding()
    else:
        exit()
if __name__ == '__main__':
    main()