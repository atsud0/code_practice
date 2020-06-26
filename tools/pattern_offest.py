"""
模仿msf pattern_offest
计算偏移量

用法: python pattern_offest.py pattern hex
Usage: python pattern_offest.py pattern hex

python pattern_offest.py 600 35724134
python pattern_offest.py 2700 39694438
"""

import pattern
import sys


def get_offest(offest, pattern_char):
    offest_list = []
    for i in range(len(offest)):
        if i % 2 == 0:
            offest_list.append("0x" + offest[i:i + 2])
    offest_list = offest_list[::-1]  # 反转
    offest_char = ""
    for i in offest_list:
        offest_char += chr(int(i, 16))
    offest = pattern_char.find(offest_char)
    return offest


def main():
    try:
        return get_offest(sys.argv[2], pattern.main())
    except Exception:
        print("Usage: python pattern_offest.py pattern hex\nlike:  python pattern_offest.py 2700 39694438")


if __name__ == "__main__":
    print(main())
