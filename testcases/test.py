#!/usr/bin/env python3

from subprocess import Popen, PIPE
import re
import os.path
from glob import glob

REGEX_TOKEN = "REGEX{"
REPEAT_TOKEN = "REPEAT{"
TOKEN_END = "}"


def run_test(test_name):
    in_data = open(test_name + "_in", "rb").read()
    expected = open(test_name + "_out", "r").read().split("\n")
    params_filename = test_name + "_params"

    cmd = ['python3', '../main.py']
    if os.path.isfile(params_filename):

        cmd += [a.strip()
                for a in open(params_filename, "r").read().split(" ")]

    stdoutdata, stderrdata = Popen(
        cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(input=in_data)

    try:
        stdoutdata = stdoutdata.decode('utf-8')
    except:
        return False, "Output contains non-UTF-8-characters"

    lines = stdoutdata.split("\n")
    idx = 0

    def next_line():
        nonlocal idx, lines
        line = None
        try:
            while not line:
                line = lines[idx].strip()
                idx += 1
            return line
        except Exception as e:
            return ""

    for i, e in enumerate(expected):
        # expected
        e = e.strip()
        if not e:
            continue

        line = next_line()

        if e.startswith(REPEAT_TOKEN):
            reg = re.compile(e[len(REPEAT_TOKEN):-len(TOKEN_END)])
            while reg.match(line):
                line = next_line()
            idx -= 1
            continue

        if REGEX_TOKEN in e:
            regex_begin = e.index(REGEX_TOKEN)
            reg = re.compile(e[regex_begin+len(REGEX_TOKEN):-len(TOKEN_END)])
            if reg.match(line[regex_begin:]):
                if e[:regex_begin] == line[:regex_begin]:
                    continue
        elif e == line:
            continue

        return False, "expected '{}'\nbut got  '{}'\n".format(e, line)

    if stderrdata:
        return False, "process printed to stderr: " + stderrdata.decode('utf-8')

    return True, "pass"


def try_test(test):
    try:
        return run_test(test)
    except Exception as e:
        return False, "Test failed: {}".format(e)


def main():
    for test_in in sorted(glob("*_in")):
        test = test_in[:-3]
        sucess, msg = try_test(test)
        print(test, end=": ")
        if sucess:
            print("success")
        else:
            print("failed!")
            print(msg)


if __name__ == '__main__':
    main()
