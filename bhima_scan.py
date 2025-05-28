#!/usr/bin/env python3
"""
BhimaScan - Hidden Directory Discovery Tool
Main launcher with interactive, config-file, auth-session and OOB support.
"""

import sys
import os
import json
import requests

from bhima_scan.cli import parse_arguments
from bhima_scan.interactive import interactive_config, load_saved_profiles
from bhima_scan.core import BhimaScan

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            return [l.strip() for l in f if l.strip()]
    except Exception as e:
        print(f"[-] Error loading wordlist: {e}")
        sys.exit(1)

def load_config(name):
    """
    Load configuration from saved profiles or JSON/YAML file.
    """
    saved = load_saved_profiles()
    if name in saved:
        return saved[name]

    if os.path.exists(name):
        ext = os.path.splitext(name)[1].lower()
        try:
            with open(name) as f:
                if ext in ('.yaml', '.yml'):
                    import yaml
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
        except Exception as e:
            print(f"[-] Failed to parse config file '{name}': {e}")
            sys.exit(1)

    print(f"[-] Config '{name}' not found as profile or file.")
    sys.exit(1)

def main():
    args = parse_arguments()

    # CONFIG mode
    if args.config:
        cfg = load_config(args.config)
        args.url        = cfg.get('url')
        args.wordlist   = cfg.get('wordlist')
        args.output     = cfg.get('output')
        args.threads    = cfg.get('threads')
        args.status     = cfg.get('status')
        args.format     = cfg.get('format')
        args.proxy      = cfg.get('proxy')
        args.bypass_403 = cfg.get('bypass_403', False)
        args.login_url  = cfg.get('login_url')
        args.username   = cfg.get('username')
        args.password   = cfg.get('password')
        args.oob_domain = cfg.get('oob_domain')

    # INTERACTIVE mode (if no config)
    elif args.interactive:
        cfg = interactive_config()
        args.url        = cfg['url']
        args.wordlist   = cfg['wordlist']
        args.output     = cfg['output']
        args.threads    = cfg['threads']
        args.status     = cfg['status']
        args.format     = cfg['format']
        args.proxy      = cfg['proxy']
        args.bypass_403 = cfg.get('bypass_403', False)
        args.login_url  = cfg.get('login_url')
        args.username   = cfg.get('username')
        args.password   = cfg.get('password')
        args.oob_domain = cfg.get('oob_domain')

    # Ensure URL is provided
    if not args.url:
        print("[-] No URL provided. Use -u/--url, --interactive, or --config.")
        sys.exit(1)

    # Load wordlist
    words = load_wordlist(args.wordlist)

    # Authenticated session setup
    session = None
    if args.login_url and args.username and args.password:
        print(f"[+] Logging in at {args.login_url} as '{args.username}'...")
        session = requests.Session()
        try:
            login_data = {'username': args.username, 'password': args.password}
            resp = session.post(args.login_url, data=login_data, timeout=10)
            if resp.status_code not in (200, 302):
                print(f"[-] Login failed: HTTP {resp.status_code}")
                sys.exit(1)
            print(f"[+] Authenticated session established (status {resp.status_code})")
        except Exception as e:
            print(f"[-] Error during login: {e}")
            sys.exit(1)

    # Initialize and run scanner
    scanner = BhimaScan(
        target_url     = args.url,
        wordlist       = words,
        output_file    = args.output,
        thread_count   = args.threads,
        proxy          = args.proxy,
        valid_statuses = args.status,
        format_type    = args.format,
        bypass_403     = args.bypass_403,
        session        = session,
        oob_domain     = args.oob_domain
    )
    scanner.run()

if __name__ == '__main__':
    main()
