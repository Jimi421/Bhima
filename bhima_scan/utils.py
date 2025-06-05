import random
import time
import json
import csv
import os
import re
import socket
import threading
from queue import Queue
from colorama import Fore, Style, init

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

DEFAULT_DELAY_MIN = 0.5
DEFAULT_DELAY_MAX = 2.0

def random_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def safe_sleep(min_delay=DEFAULT_DELAY_MIN, max_delay=DEFAULT_DELAY_MAX):
    time.sleep(random.uniform(min_delay, max_delay))

def color_status(code):
    if code == 200:
        return Fore.GREEN + str(code) + Style.RESET_ALL
    elif code in (301, 302):
        return Fore.YELLOW + str(code) + Style.RESET_ALL
    elif code == 403:
        return Fore.RED + str(code) + Style.RESET_ALL
    return Fore.LIGHTBLACK_EX + str(code) + Style.RESET_ALL

def extract_title(html):
    try:
        match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else None
    except Exception:
        return None

def save_results(data, output_file, format_type="txt"):
    out_dir = os.path.dirname(output_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if format_type == "txt":
        with open(output_file, "w") as f:
            for entry in data:
                f.write(entry.get("url", "") + "\n")
    elif format_type == "json":
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
    elif format_type == "csv":
        with open(output_file, "w", newline="") as f:
            fieldnames = [
                "url",
                "status",
                "title",
                "server",
                "bypass_header",
                "oob_token"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    "url": entry.get("url", ""),
                    "status": entry.get("status", ""),
                    "title": entry.get("title", ""),
                    "server": entry.get("server", ""),
                    "bypass_header": entry.get("bypass_header", ""),
                    "oob_token": entry.get("oob_token", "")
                })

def host_is_alive(host, ports=(80, 443), timeout=0.5):
    """Return True if any given TCP port on host is open."""
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((str(host), int(port))) == 0:
                    return True
        except Exception:
            continue
    return False

def filter_live_hosts(hosts, ports=(80, 443), threads=50):
    """Return a subset of hosts that respond on any of the given ports."""
    live_hosts = []
    q = Queue()
    for h in hosts:
        q.put(h)

    def worker():
        while True:
            try:
                host = q.get_nowait()
            except Exception:
                break
            if host_is_alive(host, ports):
                live_hosts.append(host)
            q.task_done()

    thread_count = min(threads, len(hosts)) or 1
    threads_list = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads_list.append(t)

    q.join()
    return live_hosts
