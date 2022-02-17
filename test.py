#!/usr/bin/env python3

import random
import string
from subprocess import Popen, PIPE

def rand_string(size, sep = ''):
    good_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return sep.join(random.choices(population=good_chars, k=size)).encode('utf-8')


def rand_spaces(size):
    return ''.join(random.choices(population=string.whitespace, k=size)).encode('utf-8')


def gen_input(stream, words_cnt, front_spaces, back_spaces):
    if front_spaces:
        stream.write(rand_spaces(random.randint(1, 10)))
    if words_cnt >= int(1e5):
        chunk_size = int(1e4)
        (chunks, delta) = divmod(words_cnt, chunk_size)
        big_chunk = rand_spaces(1) + rand_string(chunk_size, ' ')
        for _ in range(chunks):
            stream.write(big_chunk)
        for _ in range(delta):
            stream.write(rand_spaces(random.randint(1, 50)))
            stream.write(rand_string(random.randint(1, 50)))
    elif words_cnt >= 1:
        stream.write(rand_string(random.randint(1, 50)))
        for _ in range(words_cnt - 1):
            stream.write(rand_spaces(random.randint(1, 50)))
            stream.write(rand_string(random.randint(1, 50)))
    if back_spaces:
        stream.write(rand_spaces(random.randint(1, 10)))


def test(words_cnt, front_spaces, back_spaces):
    with Popen('./wordcount', shell=True, stdin=PIPE, stdout=PIPE, close_fds=True) as process:
        gen_input(process.stdin, words_cnt, front_spaces, back_spaces)

        process.stdin.close()
        if process.wait() != 0:
            print('Return code is not 0!')
            exit(1)

        real = process.stdout.read()
        if words_cnt != int(real):
            print(f'Expected {words_cnt} words, but counted {real}')
            exit(1)


def test_all_spaces(words_cnt):
    test(words_cnt, False, False)
    test(words_cnt, True, False)
    test(words_cnt, False, True)
    test(words_cnt, True, True)


random.seed(2517)
test_all_spaces(0)
for _ in range(100):
    cnt = random.randint(100, 5000)
    test_all_spaces(cnt)
for huge in map(int, [1e6, 1e7, 1e8, 1e9]):
    test_all_spaces(huge + 13)
test_all_spaces(2 ** 32 + 42)
