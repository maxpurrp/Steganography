import os
import argparse
def _output_byte(byte : int, ind : str) -> int:
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

def encoding(text : str, pict : str):
    #Text-to-image encoding
    text_for_encoding = ''
    with open(text, 'r') as msg:
        ign = msg.readlines()
        for elem in ign:
            text_for_encoding += elem
    with open(pict, 'rb') as start_pic:
        if (os.stat(pict).st_size  - 54) < len(text_for_encoding) * 8:
            print('text size is to big')
            exit()
        with open('update_pict.bmp', 'wb') as final_pic:
            pict_info = start_pic.read(54)
            #first 54 byte is info about picture in .bmp
            final_pic.write(pict_info)
            for elem in text_for_encoding:
                cu_ascii_list = format(ord(elem), '08b')
                for ind in cu_ascii_list:
                    cur_byte = int.from_bytes(start_pic.read(1), byteorder='little')
                    cur_byte = _output_byte(cur_byte, ind)
                    final_pic.write(cur_byte.to_bytes(1, byteorder='little'))
            final_pic.write(start_pic.read())

def decoding(pict_for_decoding : str):
    #decoding str from picture 
    with open(pict_for_decoding, 'rb') as pict:
        symbol = ''
        pict_info = pict.read(54)
        byte = int.from_bytes(pict.read(1),byteorder='little')
        while bin(byte)[-1] == '1':
                symbol +=(format(byte, '#010b'))[-2]
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-pict', required= True)
    parser.add_argument('-text', required= True)
    parser.add_argument('-action', required= True, choices= ['encoding', 'decoding'])
    args = parser.parse_args()
    if args.action == 'encoding':
        encoding(args.text, args.pict)
    if args.action == 'decoding':
        decoding(args.pict)

if __name__ == '__main__':
    main()