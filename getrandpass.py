from random import choice

'''
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789!@#$%&()<>?[]'
    length = len(chars)
    for i in range(randomlength):
       str += choice(chars)
    return str
'''


def random_str(randomlength=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789!@#$%&()<>?[]'
    return ''.join(choice(chars) for i in range(randomlength))


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        passlen = 8 if len(sys.argv) == 1 else int(sys.argv[1])
        print(random_str(passlen))
    else:
        for i in range(int(sys.argv[2])):
            print(random_str(int(sys.argv[1])))
