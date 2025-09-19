

# test_bad.py
# 의도적으로 소나큐브 이슈를 많이 발생시키는 "나쁜 코드" 예제 파일

# unused imports (사용하지 않는 import)
import os
import sys
import math
import json
import pickle  # insecure when used with untrusted data
from random import *  # wildcard import (bad practice)
import hashlib  # insecure algorithm usage later
import time

# global mutable
BAD_GLOBAL = {}
PASSWORD = "P@ssw0rd123"  # hardcoded credential (security issue)
_api_key = "apikey-12345"  # hardcoded secret

# shadowing builtin
list = [1, 2, 3]

def too_many_params(a, b, c, d, e, f, g, h, i, j):
    # maintainability: too many parameters, some unused
    result = a + b
    unused_local = c  # unused var
    # unreachable code pattern (after return)
    return result
    print("this is unreachable")

def mutable_default(arg=[]):
    # mutable default argument (state shared across calls)
    arg.append("bad")
    return arg

def insecure_random_choice(seq):
    # using random module from wildcard import
    return choice(seq)  # nondeterministic and could be insecure usage

def duplicate_code_one(x):
    if x > 0:
        return x * 2
    else:
        return -x

def duplicate_code_two(x):
    if x > 0:
        return x * 2
    else:
        return -x

def complex_function(a):
    # very complex nesting and cyclomatic complexity
    total = 0
    for i in range(5):
        if i % 2 == 0:
            for j in range(5):
                for k in range(3):
                    if (i + j + k) % 3 == 0:
                        total += i * j - k
                    else:
                        total += i + j + k
        else:
            for j in range(4):
                if j == 2:
                    total *= 2
                else:
                    total += j
    try:
        # deliberate division by zero to be caught by broad except
        x = 1 / 0
    except Exception:
        # broad except (bad)
        total = -1
    return total

def dangerous_eval(user_input):
    # security hotspot: eval on user input
    return eval(user_input)

def dangerous_exec(code_str):
    # exec usage (dangerous)
    env = {}
    exec(code_str, env)
    return env

# insecure file handling (not using with -> resource leak)
def write_file_no_close(path, content):
    f = open(path, "w")
    f.write(content)
    # forgot to close the file -> resource leak

# insecure file handling (open in read but not exist handling)
def read_file_no_check(path):
    f = open(path, "r")
    data = f.read()
    return data  # file descriptor leaked

# file operations with potential path injection
def create_user_file(username, content):
    # building path by concatenation (path traversal possibility)
    path = "/tmp/" + username + ".txt"
    f = open(path, "w")
    f.write(content)
    # no close again

# insecure SQL string construction (SQL injection)
def build_query(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "' AND pwd = '" + PASSWORD + "'"
    print("Running query:", query)
    return query

# using pickle on untrusted data (RCE potential)
def load_data(raw_bytes):
    return pickle.loads(raw_bytes)

# weak cryptography usage
def simple_hash(value):
    # using md5 is insecure
    m = hashlib.md5()
    m.update(value.encode("utf-8"))
    return m.hexdigest()

# reassign builtin name
def reassign_builtin():
    global max
    max = 5  # shadowing builtin function

# deeply nested functions (hard to read)
def outer(a):
    def inner(b):
        def inner2(c):
            if c > 0:
                return c * b * a
            else:
                return c - b - a
        return inner2
    return inner(2)

# sleeping in code path (bad for responsiveness)
def slow_sleep():
    time.sleep(2)
    return "slept"

# dead code (never used)
def unused_function_one():
    return "I am not used"

def unused_function_two():
    return "Also unused"

# ignoring returned value
def ignore_return():
    os.system("echo 'run something'")  # using shell calls without sanitization

# large function doing too many things
def god_function(x, y, z, w):
    # does too many responsibilities
    res = 0
    for i in range(100):
        for j in range(20):
            res += i * j
            if i % 7 == 0:
                res -= j
    # duplicate logic
    if x > y:
        res += x - y
    else:
        res += y - x
    # repeat earlier operation (duplicate)
    if x > y:
        res += x - y
    else:
        res += y - x
    # mixing I/O with logic
    f = open("god.log", "a")
    f.write("res: " + str(res))
    # forgot to close
    return res

# recursion with missing or shallow base case
def bad_recursion(n):
    if n <= 0:
        return 0
    # no tail recursion handling and potential deep recursion
    return bad_recursion(n - 1) + 1

# naughty use of globals
def modify_global():
    global BAD_GLOBAL
    BAD_GLOBAL['count'] = BAD_GLOBAL.get('count', 0) + 1

# OS command injection vulnerability example
def run_command(user_input):
    # insecure concatenation into shell command
    cmd = "ls " + user_input
    os.system(cmd)

# regex with catastrophic backtracking example (naive)
import re
def catastrophic_regex(s):
    pattern = re.compile(r"(a+)+b")
    return bool(pattern.search(s))

# unused import variable demonstration (json imported above not used)
def use_none():
    pass

# mixing exceptions badly
def multi_except(x):
    try:
        if x == 0:
            raise ValueError("zero")
        if x == 1:
            raise KeyError("one")
        return x
    except (ValueError, KeyError) as e:
        # do nothing useful
        print("error occurred")
    except:
        # bare except (very bad)
        print("unexpected error")

# silent failures
def silent_fail():
    try:
        1 / 0
    except ZeroDivisionError:
        # swallow the exception silently
        pass

# variable shadowing in nested scopes
var = 10
def shadowing():
    var = 20  # shadows outer var
    def inner():
        nonlocal_var = 30
        return nonlocal_var
    return var

# creating large list in memory unnecessarily
def build_huge_list():
    # memory waste - could use generator
    huge = [i for i in range(100000)]
    return huge[:10]

# poor logging practice (using print)
def log_stuff():
    print("Important:", PASSWORD)  # printing secret

# copy-paste badness: many repetitive small functions
def bad_a(): return 1
def bad_b(): return 1
def bad_c(): return 1
def bad_d(): return 1
def bad_e(): return 1
def bad_f(): return 1

# function naming inconsistency and magic numbers
def compute_magic(x):
    return x * 42 + 7  # magic numbers

# using index access without checks
def first_element(seq):
    return seq[0]  # IndexError if empty

# implicit type conversions and duck-typing abuse
def add_any(a, b):
    return a + b  # may raise TypeError

# catching too broad exception and using it for control flow
def control_with_exception(x):
    try:
        if x < 0:
            raise Exception("neg")
        return x
    except Exception:
        return 0

# open network socket without handling or timeouts (pseudo-example)
def fake_network_call():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # no timeout set, no close, no error handling
    try:
        s.connect(("example.com", 80))
        s.send(b"GET / HTTP/1.0\r\n\r\n")
        data = s.recv(1024)
    except Exception:
        data = b""
    return data

# bad resource caching in global scope
CACHE = {}
def cache_result(key, value):
    CACHE[key] = value  # never expires

# reusing variables for different types
def reuse_var():
    x = 1
    x = "string now"
    x = [1, 2, 3]
    return x

# if/else branches that are identical (redundant)
def redundant_branch(flag):
    if flag:
        do = 1 + 1
    else:
        do = 1 + 1
    return do

# large multiline string build with concatenation (inefficient)
def build_string():
    s = ""
    s += "a"
    s += "b"
    s += "c"
    s += "d"
    return s

# multiple return points (harder to maintain)
def multiple_returns(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    return x

# leftover commented code (noisy)
# def old_function():
#     pass

# calling functions but ignoring exceptions entirely
def call_many_things():
    try:
        bad_a()
        bad_b()
    except:
        pass

# another insecure pattern: eval inside f-string
def eval_in_fstring(expr):
    return f"result: {eval(expr)}"

# constructing JSON insecurely by string concatenation
def build_json_insecure(k, v):
    return "{" + '"' + str(k) + '":"' + str(v) + '"' + "}"

# purposely long chain of attribute access (fragile)
class A:
    def __init__(self):
        self.b = None

class B:
    def __init__(self):
        self.c = None

def fragile_chain(obj):
    # will throw if any part is None
    return obj.b.c.d

# infinite loop example
def infinite_loop():
    i = 0
    while True:
        i += 1
        if i > 1000000000:
            break
    return i

# final main that ties many bad things together
def main():
    # call many bad patterns to ensure SonarQube picks them up
    mutable_default()
    insecure_random_choice([1,2,3])
    duplicate_code_one(5)
    duplicate_code_two(5)
    complex_function(1)
    try:
        dangerous_eval("2+2")
    except Exception:
        pass
    try:
        dangerous_exec("a=5")
    except Exception:
        pass
    write_file_no_close("tmp.txt", "hello")
    read_file_no_check("tmp.txt")
    create_user_file("user; rm -rf /", "data")
    build_query("admin' OR '1'='1")
    try:
        load_data(b"not a pickle")
    except Exception:
        pass
    simple_hash("secret")
    reassign_builtin()
    outer(3)
    slow_sleep()
    modify_global()
    run_command("; echo hacked")
    catastrophic_regex("aaaaa" * 10 + "b")
    multi_except(0)
    silent_fail()
    shadowing()
    build_huge_list()
    log_stuff()
    god_function(1,2,3,4)
    bad_recursion(5)
    fake_network_call()
    cache_result("k", "v")
    rebuild = build_string()
    eval_in_fstring("3*7")
    build_json_insecure("k", "v")
    try:
        fragile_chain(A())
    except Exception:
        pass

if __name__ == "__main__":
    main()


