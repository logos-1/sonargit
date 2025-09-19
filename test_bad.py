
# test_bad2.py
# 또 다른 "의도적으로 나쁜" 코드 샘플 — SonarQube에서 다양한 규칙을 잡아내도록 구성

import os
import subprocess
import threading
import tempfile
import ssl
import socket
import http.client
import urllib.request
from urllib.parse import urljoin
from xml.etree import ElementTree as ET
from collections import defaultdict
from math import factorial  # unused
from datetime import datetime  # used poorly later

# Hardcoded secrets and credentials
DB_USER = "admin"
DB_PASS = "changeme"
API_SECRET = "secret-token"
PRIVATE_KEY_PEM = "-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----"

# Global state mutated by many functions (bad)
GLOBAL_COUNTER = 0
GLOBAL_CACHE = {}
LOCK = threading.Lock()  # but sometimes not used -> race condition

# Overly broad class doing many responsibilities
class EverythingDoer:
    def __init__(self):
        self.storage = {}
        self.conn = None

    def do_network_call(self, host, path):
        # insecure SSL: disable verification (bad)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            conn = http.client.HTTPSConnection(host, context=ctx)
            conn.request("GET", path)
            resp = conn.getresponse()
            return resp.read()
        except Exception:
            return b""

    def run_shell(self, user_input):
        # insecure subprocess usage with shell=True and string concat
        cmd = "echo " + user_input
        subprocess.call(cmd, shell=True)

    def xml_parse(self, xml_str):
        # insecure XML parsing without protection against XXE
        try:
            root = ET.fromstring(xml_str)
            return root.tag
        except Exception:
            return None

    def open_tempfile_bad(self):
        # insecure temp file usage (race possible, no mode restrictions)
        tmp = tempfile.mktemp()  # deprecated and insecure
        f = open(tmp, "w")
        f.write("data")
        # no close, no cleanup
        return tmp

# Name shadowing builtins and modules
open = "not a function"
socket = "string now"

# Functions with inconsistent return types and magic numbers
def inconsistent_return(x):
    if x > 0:
        return x
    if x == 0:
        return "zero"
    # implicitly returns None otherwise

# Busy-wait loop (CPU burn)
def busy_wait(limit):
    i = 0
    while i < limit:
        i += 1  # no sleep -> CPU hog
    return i

# Race condition: sometimes uses lock, sometimes not
def increment_global():
    global GLOBAL_COUNTER
    # sometimes forget locking
    GLOBAL_COUNTER += 1

def safe_increment():
    global GLOBAL_COUNTER
    with LOCK:
        GLOBAL_COUNTER += 1

# Using eval on formatted string
def eval_builder(user_input):
    expr = "{} + 1".format(user_input)
    return eval(expr)

# Overly complicated list manipulation and slicing mistakes
def list_madhouse(n):
    a = []
    for i in range(n):
        a.append(i)
    # unnecessary copy and slice
    b = a[:]
    return b[n//2 : n]  # may return empty unexpectedly

# Improper exception usage: control flow with exceptions
def exception_control_flow(x):
    try:
        if x < 0:
            raise Exception("neg")
        return x
    except Exception:
        return -1

# Exposing secrets via print/log
def reveal_secret():
    print("DB credentials:", DB_USER, DB_PASS)
    return DB_PASS

# Creating files with insecure permissions
def write_secret_file(path):
    f = open(path, "w")
    f.write(API_SECRET)
    f.flush()
    # overly permissive mode change
    try:
        os.chmod(path, 0o777)
    except Exception:
        pass

# Re-raising exceptions poorly
def convert_and_fail(s):
    try:
        return int(s)
    except ValueError as e:
        # re-raise without context or handling
        raise

# Unnecessary encoding/decoding and double-serialization
def encode_twice(s):
    b = s.encode("utf-8")
    bb = b.hex()
    return bb.encode("utf-8").decode("utf-8")

# Poor HTTP request handling (no timeout)
def fetch_url(url):
    req = urllib.request.Request(url)
    # no timeout => may hang
    with urllib.request.urlopen(req) as r:
        return r.read()

# Bad use of sockets (no timeout, no close)
def raw_socket_connect(host, port):
    s = socket.socket()
    s.connect((host, port))
    s.send(b"GET / HTTP/1.0\r\n\r\n")
    data = s.recv(1024)
    # forgot close
    return data

# Parsing user input into shell command insecurely
def list_dir(user_input):
    cmd = ["ls", user_input]
    # accidentally pass through shell execution
    subprocess.Popen(" ".join(cmd), shell=True)

# Silent swallowing of keyboard interrupt
def loop_forever():
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # silently ignore user interruption
        return

# Re-creating heavy objects inside loop (inefficient)
def create_many_objects(n):
    result = []
    for i in range(n):
        result.append(dict(a=i, b=[j for j in range(1000)]))
    return result

# Unused large constant
LARGE_CONST = [0] * 1000000

# Duplicate code patterns separated across functions
def compute_a(x):
    if x > 10:
        return x * 2
    return x + 1

def compute_b(x):
    if x > 10:
        return x * 2
    return x + 1

# Hardcoded timeout in seconds (magic number)
def wait_magic():
    import time
    time.sleep(5)  # magic

# Insecure JSON building by string concat
def build_json_bad(k, v):
    return '{"' + str(k) + '":"' + str(v) + '"}'

# Unsafe deserialization stub (pretend)
def unsafe_deserialize(s):
    # pretend to use eval on incoming structure
    return eval(s)

# Function that swallows too many exception types
def dangerous_io(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        # hides all errors
        return ""

# Unhandled Unicode issues: encode without errors param
def force_encode(s):
    return s.encode("ascii")  # may raise UnicodeEncodeError

# Re-using socket variable name (shadowing)
def confuse_socket():
    socket = "i am not a socket"
    return socket

# Blocking join without timeout — can hang tests
def start_thread_and_join():
    t = threading.Thread(target=busy_wait, args=(10**7,))
    t.start()
    t.join()  # joins forever for big workload without timeout

# Omitted input validation (path traversal)
def save_user_file(username, content):
    path = "/tmp/" + username  # path traversal possible
    with open(path, "w") as f:
        f.write(content)

# Incorrect type checking and brittle logic
def brittle(x):
    if type(x) is int:
        return x + 1
    # doesn't handle subclasses or other numeric types
    return None

# Leaking file descriptors by opening many files
def leak_files(n):
    files = []
    for i in range(n):
        files.append(open("/dev/null", "r"))
    # never closed

# Poor use of subprocess output handling
def capture_subprocess():
    p = subprocess.Popen(["echo", "ok"], stdout=subprocess.PIPE)
    out = p.stdout.read()  # no timeout, blocking
    return out

# Using deprecated APIs intentionally
def deprecated_api_usage():
    # tempfile.mktemp used earlier; here use os.tmpnam-like behavior
    try:
        name = tempfile.mktemp()
    except Exception:
        name = "/tmp/old"
    return name

# Insecure string formatting with percent formatting + user input
def percent_formatting(user):
    return "%s:%s" % (user, API_SECRET)

# Creating files in world-writable dirs
def create_world_writable():
    path = "/tmp/world_writable_test.txt"
    f = open(path, "w")
    f.write("open")
    f.close()
    try:
        os.chmod(path, 0o777)
    except Exception:
        pass

# Overly permissive XML processing repeated
def parse_many_xml(items):
    results = []
    for it in items:
        results.append(EverythingDoer().xml_parse(it))
    return results

# Long function with many responsibilities and nested conditionals
def spaghetti(a, b, c):
    x = 0
    if a:
        for i in range(5):
            if b:
                x += i
            else:
                x -= i
            if c:
                x = x * 2
    else:
        for j in range(3):
            x += j
    if x > 10:
        return "big"
    elif x == 0:
        return 0
    else:
        return None

# Plaintext logging of secrets to a "log"
def write_log(msg):
    f = open("app.log", "a")
    f.write(f"{datetime.now()} - {msg}\n")
    # no rotation, no security

# Poor validation: accepting any URL and using it
def download_and_execute(url):
    # insecurely download and eval content (do NOT run on real URLs)
    data = fetch_url(url)
    try:
        code = data.decode("utf-8")
        # dangerous: eval of remote content
        eval(code)
    except Exception:
        pass

# Function that swallows exception and returns inconsistent type
def parse_int_maybe(s):
    try:
        return int(s)
    except:
        return "NaN"

# Misleading function name and side effects
def is_safe_to_delete(path):
    # actually deletes things! dangerous naming
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass
        return True
    return False

# Reassigning imported name
def hijack_imports():
    global urllib
    urllib = "not a module anymore"

# Repetition and code bloat: many tiny duplicate functions
def tiny1(): return 1
def tiny2(): return 1
def tiny3(): return 1
def tiny4(): return 1
def tiny5(): return 1
def tiny6(): return 1
def tiny7(): return 1
def tiny8(): return 1
def tiny9(): return 1
def tiny10(): return 1

# Use of eval in f-string again
def fstring_eval(expr):
    return f"calc: {eval(expr)}"

# Overcomplicated iterator logic
def nested_iter(n):
    it = iter(range(n))
    res = []
    for x in it:
        for y in it:
            res.append((x, y))
    return res

# Unnecessary conversion to/from JSON by building manual strings
def roundtrip_json(k, v):
    s = '{"k":"v"}'
    # pretend to parse and build but do it wrong
    return s.replace("k", str(k)).replace("v", str(v))

# main that triggers many bad things
def main():
    ed = EverythingDoer()
    ed.run_shell("hello; echo world")  # possible shell injection if user input used
    ed.open_tempfile_bad()
    write_secret_file("secrets.txt")
    reveal_secret()
    try:
        fetch_url("http://example.com")  # no timeout
    except Exception:
        pass
    raw_socket_connect("example.com", 80)
    list_dir("; /")  # weird user input
    start_thread_and_join()
    create_many_objects(5)
    leak_files(5)
    percent_formatting("user_supplied")
    parse_many_xml(["<a></a>", "<b></b>"])
    write_log("Started")
    try:
        download_and_execute("http://localhost/code")
    except Exception:
        pass
    # mutate globals unsafely
    for _ in range(10):
        increment_global()
    # call many tiny duplicates
    tiny1(); tiny2(); tiny3(); tiny4(); tiny5()
    fstring_eval("2*3")
    nested_iter(5)
    # return inconsistent type sometimes
    print(inconsistent_return(-1))

if __name__ == "__main__":
    main()


