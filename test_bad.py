
# test_bad4.py
# 새로운 범주의 "문제 많은" 코드: 이식성, 로케일/타임존, async/sync 혼용, 부동소수점, 잘못된 타입힌트 등

import os
import sys
import time
import locale
import math
import threading
import asyncio
import datetime
import platform
import struct

# ----------------------------------------
# 1) 플랫폼/이식성 문제
# ----------------------------------------
# Hardcoded platform-specific path separators and assumptions
WINDOWS_ONLY_PATH = "C:\\temp\\appdata\\file.txt"
UNIX_ONLY_PATH = "/tmp/appdata/file.txt"

def write_platform_file(data):
    # chooses wrong path based on a naive platform check
    if platform.system() == "Windows":
        path = UNIX_ONLY_PATH  # bug: swapped
    else:
        path = WINDOWS_ONLY_PATH
    # may crash because the path doesn't exist on the platform
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

# Using struct with fixed endianness but assuming same on all platforms
def pack_values(a, b):
    # packs ints into 8 bytes assuming little-endian, which may be incompatible
    return struct.pack("<II", a, b)

# ----------------------------------------
# 2) Locale / Internationalization issues
# ----------------------------------------
# Relying on locale-specific number formatting without setting locale
def format_number_bad(n):
    # no locale set -> results inconsistent across environments
    return locale.format_string("%d", n, grouping=True)

# Unicode normalization mistakes: unsafe splitting of grapheme clusters
def naive_truncate_unicode(s, n_chars):
    # slicing by code points can break composed characters (user-visible bug)
    return s[:n_chars]

# Hardcoded ASCII-only replacements
def strip_accents_bad(s):
    # removes diacritics by simple replace (incomplete and buggy)
    return s.replace("é", "e").replace("á", "a")

# ----------------------------------------
# 3) Timezone / DST bugs
# ----------------------------------------
# naive datetime arithmetic that ignores timezones and DST
def add_one_day_naive(dt):
    # dt is assumed naive local time; DST transitions will break this
    return dt + datetime.timedelta(days=1)

# storing timestamps as localtimes string (non-portable)
def save_timestamp_local():
    now = datetime.datetime.now()  # local time
    return now.strftime("%Y-%m-%d %H:%M:%S")  # ambiguous without tz

# ----------------------------------------
# 4) Floating point precision & numeric issues
# ----------------------------------------
def sum_many_floats_bad(values):
    # naive summation -> large rounding errors for big lists
    total = 0.0
    for v in values:
        total += v
    return total

def compare_floats_direct(a, b):
    # comparing floats for equality directly (bad)
    return a == b

def integer_overflow_sim():
    # Python ints don't overflow, but code might pack into C types incorrectly later
    big = 2 ** 60
    # later cast to 32-bit in C extension would overflow; simulate truncation
    return big & 0xFFFFFFFF

# ----------------------------------------
# 5) Sync / Async mixing mistakes
# ----------------------------------------
def blocking_sleep_in_event_loop():
    # called inside async code -> blocks the loop
    time.sleep(2)  # should be await asyncio.sleep(2)

async def async_wrapper():
    # calls blocking function without using run_in_executor
    blocking_sleep_in_event_loop()  # blocks event loop
    return "done"

def run_async_wrong():
    # creating event loop incorrectly in already running event loop can error in some contexts
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_wrapper())  # problematic if called from existing loop
    loop.close()

# Starting tasks but never awaiting or cancelling them -> resource leak
async def spawn_tasks_forever():
    while True:
        asyncio.create_task(asyncio.sleep(3600))

# ----------------------------------------
# 6) Bad type hints / docs / inconsistent returns
# ----------------------------------------
def annotated_but_wrong(x: int) -> str:
    # annotation says returns str but actually returns int
    return x + 1

def optional_but_returns_none_maybe(flag: bool) -> int:
    if flag:
        return 1
    # implicit None return violates type contract

# Missing docstrings and confusing parameter names
def f(a, b, c):
    # what are a,b,c? no docstring -> hard for maintainers
    return (a + b) * c

# ----------------------------------------
# 7) Poor testing / deterministic behavior
# ----------------------------------------
# Hardcoded time-based behavior that's hard to test
def is_business_hour_now():
    h = datetime.datetime.now().hour  # non-deterministic during tests
    return 9 <= h < 18

# Using random seeded from time -> nondeterministic tests
def choose_random_item(lst):
    # reseeds on every call -> not reproducible
    import random
    random.seed(time.time())
    return random.choice(lst)

# ----------------------------------------
# 8) Fragile parsing / brittle formats
# ----------------------------------------
def parse_config_line(line: str):
    # expects "key=value" but doesn't validate -> will raise on malformed lines
    k, v = line.split("=")
    return {k.strip(): v.strip()}

def write_csv_naive(rows):
    # naive CSV writer that breaks on commas and newlines in data
    out = ""
    for row in rows:
        out += ",".join(str(x) for x in row) + "\n"
    return out

# ----------------------------------------
# 9) API misuse and versioning problems
# ----------------------------------------
# Calls functions with positional args that will break if signature changes
def api_client_call(client, payload):
    # uses private attribute of client that might be version-specific
    return client._do_request(payload)  # tight coupling to implementation

# ----------------------------------------
# 10) Accessibility / UI blocking / bad UX
# ----------------------------------------
def long_blocking_render():
    # performs heavy work on main thread (simulated)
    s = 0
    for i in range(10**7):
        s += i
    return s

def error_message_unhelpful(e):
    # hides underlying problem from user
    return "Operation failed"  # no details, no error code

# ----------------------------------------
# 11) Security-adjacent but non-exploitative issues
# ----------------------------------------
# Not a direct exploit, but leaks information through verbose errors and logs
def verbose_exception_log(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        # prints internal exception and stack info to standard out (information leak)
        print("ERROR reading file:", e)
        return ""

# Weak assumptions about file encoding
def read_maybe_utf8(path):
    # assumes file is utf-8; will crash on other encodings
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ----------------------------------------
# 12) Strange control flow and meta-programming misuse
# ----------------------------------------
def dynamic_attr_mangling(obj):
    # builds attribute names at runtime and relies on them existing
    for i in range(10):
        name = f"prop_{i}"
        if hasattr(obj, name):
            # do something fragile
            val = getattr(obj, name)
            if callable(val):
                # call without checking signature
                val()

# Using exec for tiny DSL (overkill and brittle)
def tiny_dsl_run(code):
    data = {}
    # dangerously using exec even though not necessary; but we won't accept user input here
    exec(code, {}, data)
    return data

# ----------------------------------------
# 13) Bad CI/test hooks and environment assumptions
# ----------------------------------------
def ci_only_behavior():
    # behavior depends on CI env var; tests run locally may differ
    if os.getenv("CI") == "true":
        return "ci"
    return "local"

# ----------------------------------------
# 14) Overly-specific optimization pre-matured
# ----------------------------------------
def micro_opt_worst_case(data):
    # attempts micro-optimizations that reduce clarity and may be slower for many inputs
    res = []
    for i in range(len(data)):
        # using indexes instead of iteration for no good reason
        res.append(data[i] * 2)
    return res

# ----------------------------------------
# 15) Entrypoint that triggers many of the above issues
# ----------------------------------------
def main():
    # platform path confusion -> likely to fail on user's machine
    try:
        write_platform_file("hello")
    except Exception as e:
        print("platform write failed:", e)

    # locale formatting that depends on environment
    print("Formatted number:", format_number_bad(1234567))

    # timezone naive addition
    print("Tomorrow local string:", save_timestamp_local())

    # float precision noise
    vals = [0.1] * 10000
    print("Naive sum:", sum_many_floats_bad(vals))

    # run async badly (blocks)
    try:
        run_async_wrong()
    except Exception as e:
        print("async run failed:", e)

    # type hint mismatch
    print("Annotated wrong:", annotated_but_wrong(3))

    # reading with wrong encoding
    try:
        print("Read maybe utf8:", read_maybe_utf8("nonexistent.txt"))
    except Exception as e:
        print("read failed (expected):", e)

    # unstable random choice
    print("Random pick:", choose_random_item([1,2,3,4]))

    # brittle config parsing
    try:
        print(parse_config_line("bad_line_without_equal_sign"))
    except Exception as e:
        print("parse failed (expected):", e)

if __name__ == "__main__":
    main()


