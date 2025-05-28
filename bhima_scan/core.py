import os
import threading
from queue import Queue
import requests
import uuid

from .utils import random_headers, safe_sleep, color_status, extract_title, save_results

class BhimaScan:
    def __init__(
        self,
        target_url,
        wordlist,
        output_file,
        thread_count=5,
        proxy=None,
        valid_statuses=None,
        format_type="txt",
        bypass_403=False,
        session=None,
        oob_domain=None
    ):
        self.target_url = target_url.rstrip('/')
        self.wordlist = wordlist
        self.output_file = output_file
        self.thread_count = thread_count
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.valid_statuses = (
            [int(s.strip()) for s in valid_statuses.split(',')]
            if valid_statuses else [200, 301, 302]
        )
        self.format_type = format_type
        self.bypass_403 = bypass_403
        self.session = session or requests
        self.oob_domain = oob_domain

        self.queue = Queue()
        self.found_paths = []
        self.result_data = []
        self.lock = threading.Lock()

    def worker(self):
        while not self.queue.empty():
            word = self.queue.get()
            self.scan_path(word)
            self.queue.task_done()

    def scan_path(self, word):
        url = f"{self.target_url}/{word}"
        headers = random_headers()
        oob_token = None

        if self.oob_domain:
            token = uuid.uuid4().hex
            oob_token = f"{token}.{self.oob_domain}"
            headers["X-OOB-Callback"] = oob_token

        try:
            response = self.session.get(
                url,
                headers=headers,
                proxies=self.proxy,
                timeout=8,
                allow_redirects=True
            )
            code = response.status_code

            if code in self.valid_statuses:
                self._record_hit(url, response, bypass_header=None, oob_token=oob_token)

            elif code == 403 and self.bypass_403:
                self._attempt_bypass(url, headers, oob_token)

        except requests.RequestException as e:
            with self.lock:
                print(f"[!] Error reaching {url} - {e}", end="\r")

        finally:
            safe_sleep()

    def _attempt_bypass(self, url, headers, oob_token):
        bypass_headers_list = [
            {"X-Original-URL": url},
            {"X-Rewrite-URL": url},
            {"X-Forwarded-For": "127.0.0.1"},
            {"X-Host": "127.0.0.1"},
            {"X-Custom-IP-Authorization": "127.0.0.1"},
        ]
        for hdr in bypass_headers_list:
            combined = headers.copy()
            combined.update(hdr)
            r2 = self.session.get(
                url,
                headers=combined,
                proxies=self.proxy,
                timeout=8,
                allow_redirects=True
            )
            if r2.status_code in self.valid_statuses:
                header_name = next(iter(hdr))
                self._record_hit(url, r2, bypass_header=header_name, oob_token=oob_token)
                with self.lock:
                    print(f"[+] Bypass: {url} ({color_status(r2.status_code)}) via {header_name}")
                break

    def _record_hit(self, url, response, bypass_header=None, oob_token=None):
        title = extract_title(response.text)
        server = response.headers.get("Server", "Unknown")
        with self.lock:
            print(f"[+] Found: {url} ({color_status(response.status_code)})")
            self.found_paths.append(url)
            entry = {
                "url": url,
                "status": response.status_code,
                "title": title,
                "server": server,
                "bypass_header": bypass_header,
                "oob_token": oob_token
            }
            self.result_data.append(entry)

    def run(self):
        print(
            f"[+] Starting BhimaScan on {self.target_url} "
            f"with {len(self.wordlist)} paths using {self.thread_count} threads.\n"
        )
        out_dir = os.path.dirname(self.output_file)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)

        for word in self.wordlist:
            self.queue.put(word)

        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        save_results(self.result_data, self.output_file, self.format_type)
        print(f"\n[+] Scan complete. {len(self.found_paths)} paths found.")
        print(f"[+] Results saved to {self.output_file}")
