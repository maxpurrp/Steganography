# Steganography
С помощью данной программы можно сохранить текст в тайне самого факта такого хранения используя метод SLB стеганографии. 
Доступно две функции : encodind и decoding.

## 1. Encoding
Функция шифрует текст методом замены двух последних битов в каждом байте. Последний бит в байте - указатель на то, зашифрован ли байт или нет (1 / 0). Предпоследний бит - значение ascii value символа из слова / предложения.
Для шифровки необходима картинка формата '.bmp' и на основе нее создается зашифрованная картинка такого же формата.
Входные данные: картинка и текстовый файл.
Для тестирования введите в консоль :
python3 D:\\directory\\steganography.py -image=test.bmp -text_path=text.txt -action=encoding

## 2. Decoding
Функция в цикле считывает байты и с каждого байта вычленяет бит, который несет в себе значение ascii. После чтения всех байт, функция обрабатывает ascii value, и выводит на консоль зашифрованный текст. Для декодирования необходима картинка  формата '.bmp'.
Для тестирования введите в консоль:
python3 D:\\directory\\steganography.py 
-image=update_pict.bmp -action=decoding
