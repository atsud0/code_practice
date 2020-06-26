"""
生成字符序列(模仿Metasploit中的pattern_create.rb脚本
但是并不能指定生成的字符
"""

import sys

ALL_CHARS_NUM = 20280


def get_pattern_chars():
    Char = 65
    char = 97
    c = ""
    for i in range(0, 26):
        for j in range(0, 26):
            for k in range(0, 10):
                c += chr(Char + i) + chr(char + j) + "{}".format(k)

    return c


def check_nums(num):
    check_num = num - ALL_CHARS_NUM
    i = 1
    while check_num > ALL_CHARS_NUM:
        check_num = check_num - 20280
        i += 1
    return i


def main():
    pattern_char = ""
    try:
        input_num = int(sys.argv[1])

        if input_num > ALL_CHARS_NUM:
            count = check_nums(input_num)
            for num in range(0, count + 1):
                pattern_char += get_pattern_chars()

        elif 0 < input_num < ALL_CHARS_NUM:
            pattern_char = get_pattern_chars()

        else:
            print("Usage:Python pattern.py [nums]")

        return pattern_char[0:input_num]

    except Exception as error:
        print(error,"\nUsage: python pattern [nums]")


if __name__ == '__main__':
    print(main())