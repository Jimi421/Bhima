 # File: bhima_scan/cli.py

import argparse
import sys

# Built‐in profiles
PROFILES = {
    "basic":      {"threads": 5,  "status": "200,301",     "format": "txt"},
    "stealth":    {"threads": 3,  "status": "403",         "format": "json"},
    "aggressive": {"threads": 10, "status": "200,301,403", "format": "csv"},
}

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="BhimaScan 🛡️ - Hidden Directory Discovery Tool with Profiles & Config"
    )

    # Config / profile loading
    parser.add_argument(
        "--config", type=str,
        help="Load settings from a saved profile name or a JSON/YAML config file"
    )

    # Interactive wizard mode
    parser.add_argument(
        "--interactive", action="store_true",
        help="Launch interactive wizard mode"
    )

    # Target URL
    parser.add_argument(
        "-u", "--url",
        help="Target base URL (e.g., http://example.com)"
    )

    # Wordlist file
    parser.add_argument(
        "-w", "--wordlist",
        default="wordlists/basic_wordlist.txt",
        help="Path to wordlist file (default: wordlists/basic_wordlist.txt)"
    )

    # Output file
    parser.add_argument(
        "-o", "--output",
        default="outputs/bhima_results.txt",
        help="Output file path (default: outputs/bhima_results.txt)"
    )

    # Concurrency
    parser.add_argument(
        "--threads", type=int,
        help="Number of concurrent threads"
    )

    # Proxy URL
    parser.add_argument(
        "--proxy", type=str, default=None,
        help="Optional proxy URL (e.g., http://127.0.0.1:8080)"
    )

    # HTTP status codes to include
    parser.add_argument(
        "--status", type=str,
        help="Comma-separated list of status codes to include (e.g., 200,301,403)"
    )

    # Output format
    parser.add_argument(
        "--format", type=str, choices=["txt", "json", "csv"],
        help="Output format (txt, json, csv)"
    )

    # Built‐in profile selector
    parser.add_argument(
        "--profile", type=str, choices=PROFILES.keys(),
        help="Apply a built-in profile: basic, stealth, aggressive"
    )

    # WAF evasion
    parser.add_argument(
        "--bypass-403", action="store_true", dest="bypass_403",
        help="On HTTP 403, retry with common WAF-bypass headers"
    )

    # Authenticated session
    parser.add_argument(
        "--login-url", type=str,
        help="Login URL for authenticated session (POST credentials before scanning)"
    )
    parser.add_argument(
        "--username", type=str,
        help="Username for authenticated session"
    )
    parser.add_argument(
        "--password", type=str,
        help="Password for authenticated session"
    )

    # OOB callback
    parser.add_argument(
        "--oob-domain", type=str,
        help="OOB collaborator DNS/HTTP domain for blind callback detection"
    )

    args = parser.parse_args()

    # If no arguments at all, default to interactive wizard
    if len(sys.argv) == 1:
        args.interactive = True

    # Require URL when not using config or interactive
    if not args.config and not args.interactive and not args.url:
        parser.error(
            "the following arguments are required: -u/--url when not using --interactive or --config"
        )

    return args
