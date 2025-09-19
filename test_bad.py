# test_bad3.py
# 더 많은 의도적인 안티패턴과 취약성을 포함한 테스트용 "쓰레기 코드"

import os
import sys
import time
import threading
import queue
import pickle
import subprocess
import urllib.request
import re
import json
import random
from collections import deque

# Hardcoded secrets / credentials (security issue)
ADMIN_PASS = "admin1234"
TOKEN = "token-abcdef-123456"

# Mutable global state used in unsafe ways
GLOBAL_QUEUE = queue.Queue()
GLOBAL_LIST = []
GLOBAL_FLAG = False

# Shadowing builtins and modules (bad)
str = 123
json = "not json"

# Bad regex (catastrophic backtracking risk)
BAD_REGEX = re.compile(r"(a+)+b")

def regex_test(s):
    # this may hang on crafted inputs
    return bool(BAD_REGEX.search(s))

# Busy infinite loop used as a thread (wastes CPU)
def cpu_hog():
    while True:
        pass  # never yields

# Deadlock example: two locks acquired in opposite order
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_deadlock_a():
    with lock_a:
        time.sleep(0.1)
        with lock_b:
            return "done A"

def thread_deadlock_b():
    with lock_b:
        time.sleep(0.1)
        with lock_a:
            return "done B"

# Poor thread usage: daemon threads that do too much work
def start_daemon_threads(n):
    for i in range(n):
        t = threading.Thread(target=cpu_hog)
        t.daemon = True
        t.start()

# Race condition: checking then acting (TOCTOU)
def check_and_write(path, content):
    if not os.path.exists(path):
        f = open(path, "w")
        f.write(content)
        # forgot to close -> resource leak

# Unsafe temp file usage
def insecure_temp_write(data):
    tmp = "/tmp/tmpfile-" + str(random.randint(0, 1000000))
    f = open(tmp, "w")
    f.write(data)
    # no mode/permission control, no cleanup
    return tmp

# Insecure deserialization using pickle
def load_pickle(data):
    # may execute arbitrary code when data is attacker-controlled
    return pickle.loads(data)

# Exec/eval usage
def run_dynamic(code_str):
    local_env = {}
    exec(code_str, {}, local_env)
    return local_env

def eval_input(expr):
    return eval(expr)

# Insecure subprocess injection pattern
def run_cmd_bad(user_input):
    cmd = "ls " + user_input  # simple concatenation
    subprocess.call(cmd, shell=True)

# Slow I/O blocking operation called on main thread
def slow_io_read(path):
    with open(path, "r") as f:
        # simulate long processing per-line
        res = []
        for line in f:
            time.sleep(0.01)
            res.append(line)
    return "".join(res)

# Inconsistent return types and poor error signaling
def find_in_list(lst, x):
    try:
        return lst.index(x)
    except ValueError:
        return -1
    except:
        return None  # inconsistent

# Memory leak: keep growing structure without bounds
def leak_memory(n):
    for i in range(n):
        GLOBAL_LIST.append("x" * 1024 * 10)  # append 10KB repeatedly

# Poor API: function modifies argument unexpectedly
def mutate_arg(arg):
    # modifies caller's list unexpectedly
    arg.append("mutated")
    return arg

# Ignoring exceptions silently
def ignore_exceptions():
    try:
        1 / 0
    except:
        pass  # swallow everything

# Unsafe network request: no timeout, no validation
def fetch_remote(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.read()

# Hardcoded file permissions and unsafe file creation
def create_insecure_file(path, content):
    f = open(path, "w")
    f.write(content)
    try:
        os.chmod(path, 0o666)  # too permissive
    except Exception:
        pass

# Using eval inside f-string
def fstring_eval(expr):
    return f"calc:{eval(expr)}"

# Reassigning builtins or imported names at runtime
def hijack_builtins():
    global open
    open = lambda *a, **k: None  # breaks everything

# Insecure JSON building via concatenation (injection risk)
def build_json_bad(k, v):
    return '{"' + str(k) + '":"' + str(v) + '"}'

# Long, very nested logic increasing complexity
def nested_logic(x, y, z):
    res = 0
    for i in range(10):
        if i % 2 == 0:
            for j in range(5):
                if j == 3:
                    for k in range(4):
                        res += i * j * k
                else:
                    res -= j
        else:
            for j in range(3):
                res += x + y + z
    return res

# Duplicate blocks sprinkled across functions
def dup_a(n):
    s = 0
    for i in range(n):
        s += i * 2
    return s

def dup_b(n):
    s = 0
    for i in range(n):
        s += i * 2
    return s

# Unsafe file path concatenation (path traversal)
def write_user_file(username, content):
    path = "/tmp/" + username  # no sanitization
    with open(path, "w") as f:
        f.write(content)

# Blocking network call in loop without backoff
def poll_forever(urls):
    while True:
        for u in urls:
            try:
                fetch_remote(u)
            except:
                pass
        time.sleep(0.1)  # small sleep -> tight loop

# Horrible error handling: catch Exception and continue
def process_items(items):
    results = []
    for it in items:
        try:
            results.append(int(it))
        except Exception:
            results.append(None)
    return results

# Inefficient algorithm: O(n^2) where O(n) possible
def find_duplicates(arr):
    dups = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                dups.append(arr[i])
    return dups

# Mixing concerns: I/O inside compute function
def compute_and_log(n):
    total = 0
    for i in range(n):
        total += i
        with open("compute.log", "a") as f:
            f.write(str(total) + "\n")
    return total

# Bad usage of floating point equality
def compare_floats(a, b):
    return a == b  # precision issues ignored

# Re-creating heavy objects in tight loops (inefficient)
def make_many_dicts(n):
    out = []
    for i in range(n):
        out.append({"i": i, "data": [j for j in range(1000)]})
    return out

# Using mutable default parameter that persists across calls
def config_builder(entry, conf={}):
    conf[entry] = conf.get(entry, 0) + 1
    return conf

# Side effects in property-like functions
def get_config_value(k):
    # writes to disk for read
    with open("cfg.tmp", "w") as f:
        f.write(k)
    return k

# Overly permissive logging of secrets
def log_secret():
    print("SECRET:", TOKEN)

# Mixing blocking and non-blocking concurrency poorly
def mix_concurrency():
    t = threading.Thread(target=busy_worker, args=(1000000,))
    t.start()
    # do heavy synchronous work
    leak_memory(1000)
    t.join()

def busy_worker(n):
    s = 0
    for i in range(n):
        s += i
    return s

# Function that returns inconsistent types depending on input
def maybe_string(n):
    if n == 0:
        return ""
    if n == 1:
        return 1
    return None

# Using eval on potentially user-controllable string after formatting
def build_and_eval(user_input):
    expr = "{} * 2".format(user_input)
    return eval(expr)

# Using deprecated APIs intentionally
def use_deprecated():
    # pretend to use older unstable API
    return os.tmpname() if hasattr(os, "tmpname") else "/tmp/oldtmp"

# Non-atomic file writes (partial writes possible)
def write_partial(path, data):
    f = open(path, "w")
    f.write(data[:len(data)//2])
    # program crash before finishing -> corrupt file

# Insecure cookie construction (no signing, no validation)
def build_cookie(user):
    return "user=" + user + "; token=" + TOKEN

# Overly permissive file reads (no path checks)
def read_any(path):
    with open(path, "r") as f:
        return f.read()

# Poorly implemented retry logic causing infinite retries
def retry_forever():
    while True:
        try:
            fetch_remote("http://example.com")
            break
        except:
            continue  # no backoff, no max attempts

# Creating many threads without limit -> resource exhaustion
def spawn_threads(n):
    threads = []
    for i in range(n):
        t = threading.Thread(target=time.sleep, args=(1000,))
        t.start()
        threads.append(t)
    return threads

# Mixing binary/text incorrectly
def bad_encoding(s):
    return s.encode("utf-8").decode("latin1")

# Overly permissive JSON loads with string concatenation earlier
def unsafe_json_load(s):
    # pretend we sanitize but actually we just eval
    return eval(s)

# Function with side-effect and surprising return
def write_and_return(path, val):
    with open(path, "w") as f:
        f.write(str(val))
    return True if val else 0  # inconsistent return meaning

# Long main that triggers many bad patterns
def main():
    # start some problematic threads
    start_daemon_threads(2)
    # spawn many blocking threads (resource exhaustion)
    spawn_threads(5)
    # create race and deadlock
    ta = threading.Thread(target=thread_deadlock_a)
    tb = threading.Thread(target=thread_deadlock_b)
    ta.start(); tb.start()
    # unsafe network
    try:
        fetch_remote("http://example.com")
    except:
        pass
    # write insecure file
    create_insecure_file("/tmp/insecure.txt", "data")
    # insecure temp file
    insecure_temp_write("tempdata")
    # leak memory a bit
    leak_memory(10)
    # do unsafe eval
    try:
        build_and_eval("2+2")
    except:
        pass
    # run insecure shell command (do not pass real input)
    try:
        run_cmd_bad("; echo hello")  # caution: may run shell
    except:
        pass
    # poor exception hiding
    ignore_exceptions()
    # open many files (leak)
    leak_files(3)
    # mutate config default
    config_builder("x")
    # print secrets
    log_secret()
    # inconsistent returns
    print(maybe_string(2))
    # regex that might hang on crafted input
    try:
        regex_test("a" * 1000 + "b")
    except:
        pass

# helper used above (intentionally placed later)
def leak_files(n):
    fds = []
    for i in range(n):
        fds.append(open("/dev/null", "r"))
    # never closed

if __name__ == "__main__":
    main()

