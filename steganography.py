import os
import argparse
def _byte_encoding(byte : int, ind : str) -> int:
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

def encoding(text_path : str, image_path : str):
    #Text-to-image encoding
    text_for_encoding = ''
    with open(text_path, 'r') as msg:
        for elem in msg.readlines():
            text_for_encoding += elem
    with open(image_path, 'rb') as start_pic:
        if (os.stat(image_path).st_size  - 54) < len(text_for_encoding) * 8: 
            print('text size is to big')
            exit()
        print(f'text size is {len(text_for_encoding)} out of {int((os.stat(image_path).st_size  - 54) / 8)} possible ')
        with open('update_pict.bmp', 'wb') as final_pic:
            pict_info = start_pic.read(54)
            #first 54 byte is info about picture in .bmp
            final_pic.write(pict_info)
            for elem in range(len(text_for_encoding)):
                cu_ascii_list = format(ord(text_for_encoding[elem]), '08b')
                for ind in range(len(cu_ascii_list)):
                    cur_byte = int.from_bytes(start_pic.read(1), byteorder='little')
                    cur_byte = _byte_encoding(cur_byte, cu_ascii_list[ind])
                    if elem == len(text_for_encoding) -1 and ind == len(cu_ascii_list) - 1:
                        cur_byte = cur_byte >> 1
                        cur_byte = cur_byte << 1
                    final_pic.write(cur_byte.to_bytes(1, byteorder='little'))
            final_pic.write(start_pic.read())
    print('Successfully')

def decoding(pict_for_decoding : str):
    #decoding str from picture 
    with open(pict_for_decoding, 'rb') as pict:
        symbol = ''
        output = ''
        pict_info = pict.read(54)
        byte = int.from_bytes(pict.read(1),byteorder='little')
        while bin(byte)[-1] != '0':
                symbol +=(format(byte, '#010b'))[-2]
                byte = int.from_bytes(pict.read(1),byteorder='little')
                if len(symbol) == 8:
                    output += ''.join(chr(int(symbol, 2)))
                    symbol = ''
        symbol +=(format(byte, '#010b'))[-2]
        output += ''.join(chr(int(symbol, 2)))
        print(f'output message is: {output}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pict', required = True, help ='name or path to file')
    parser.add_argument('-text', required = True, help ='name or path to file')
    parser.add_argument('-action', required = True, choices = ['encoding', 'decoding'], help = 'encoding text to image | decoding text from text')
    args = parser.parse_args()
    if args.action == 'encoding':
        encoding(args.text, args.pict)
    if args.action == 'decoding':
        decoding(args.pict)

if __name__ == '__main__':
    main()