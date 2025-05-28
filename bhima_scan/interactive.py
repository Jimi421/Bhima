import os
import json
from .cli import PROFILES
from colorama import Fore, Style, init

init(autoreset=True)

defaults = {
    'wordlist': 'wordlists/basic_wordlist.txt',
    'output': 'outputs/bhima_results.txt',
    'threads': 5,
    'status': '200,301,302',
    'format': 'txt',
    'proxy': None,
    'profile': None,
    'bypass_403': False,
    'login_url': None,
    'username': None,
    'password': None,
    'oob_domain': None
}

PROFILE_STORE = os.path.expanduser('~/.bhimascan_profiles.json')

def load_saved_profiles():
    if os.path.exists(PROFILE_STORE):
        try:
            with open(PROFILE_STORE, 'r') as f:
                return json.load(f) or {}
        except:
            pass
    return {}

def prompt_save_profile(summary):
    choice = input(Fore.WHITE + "Save this configuration as a named profile? [y/N]: " + Style.RESET_ALL).strip().lower()
    return choice in ('y', 'yes')

def save_profile_interactive(summary):
    name = input(Fore.WHITE + "Enter profile name (no spaces): " + Style.RESET_ALL).strip()
    if not name:
        print(Fore.YELLOW + "Profile save skipped: no name provided." + Style.RESET_ALL)
        return
    data = load_saved_profiles()
    data[name] = summary
    with open(PROFILE_STORE,"w") as f:
        json.dump(data,f,indent=2)
    print(Fore.GREEN + f"Profile '{name}' saved to {PROFILE_STORE}" + Style.RESET_ALL)

def interactive_config():
    print(Fore.CYAN + "\n🔍 BhimaScan Interactive Wizard 🔍\n" + Style.RESET_ALL)
    saved = load_saved_profiles()
    if saved:
        use_saved = input(Fore.WHITE + "Use a saved profile? [y/N]: " + Style.RESET_ALL).strip().lower()
        if use_saved in ('y', 'yes'):
            print(Fore.CYAN + "\nAvailable profiles:" + Style.RESET_ALL)
            for n in saved: print(" ",n)
            while True:
                choice = input("Enter profile name: ").strip()
                if choice in saved:
                    cfg = saved[choice]
                    print(Fore.CYAN + "\nLoaded profile configuration:" + Style.RESET_ALL)
                    for k,v in cfg.items():
                        print(" ",k,":",v,Fore.GREEN+" (loaded)"+Style.RESET_ALL)
                    input(Fore.CYAN+"\nPress Enter to start the scan..."+Style.RESET_ALL)
                    return cfg
                print(Fore.YELLOW+"Invalid profile name. Try again."+Style.RESET_ALL)
    url = input(Fore.WHITE + "Target URL [required]: " + Style.RESET_ALL).strip()
    while not url:
        url = input(Fore.YELLOW + "URL is required. Please enter a valid URL: " + Style.RESET_ALL).strip()
    quick = input(Fore.WHITE + "Run with defaults for all other settings? [Y/n]: " + Style.RESET_ALL).strip().lower()
    if quick in ('', 'y', 'yes'):
        summary = {'url': url}
        summary.update(defaults)
        print(Fore.CYAN+"\nUsing defaults for other settings:"+Style.RESET_ALL)
        for k,v in summary.items():
            flag = Fore.GREEN+" (default)"+Style.RESET_ALL if k!='url' else ""
            print(" ",k.ljust(10),":",v,flag)
        bp = input(Fore.WHITE + "Enable 403-bypass mode? [y/N]: " + Style.RESET_ALL).strip().lower()
        summary['bypass_403'] = bp in ('y','yes')
        lu = input(Fore.WHITE + f"Login URL [{defaults['login_url']}]: " + Style.RESET_ALL).strip() or defaults['login_url']
        summary['login_url'] = lu
        un = input(Fore.WHITE + f"Username [{defaults['username']}]: " + Style.RESET_ALL).strip() or defaults['username']
        summary['username'] = un
        pw = input(Fore.WHITE + f"Password [{defaults['password']}]: " + Style.RESET_ALL).strip() or defaults['password']
        summary['password'] = pw
        od = input(Fore.WHITE + f"OOB Domain [{defaults['oob_domain']}]: " + Style.RESET_ALL).strip() or defaults['oob_domain']
        summary['oob_domain'] = od
        if prompt_save_profile(summary): save_profile_interactive(summary)
        input(Fore.CYAN+"\nPress Enter to start the scan..."+Style.RESET_ALL)
        return summary
    wl = input(Fore.WHITE + f"Wordlist [{defaults['wordlist']}]: " + Style.RESET_ALL).strip() or defaults['wordlist']
    out = input(Fore.WHITE + f"Output file [{defaults['output']}]: " + Style.RESET_ALL).strip() or defaults['output']
    th = input(Fore.WHITE + f"Threads [{defaults['threads']}]: " + Style.RESET_ALL).strip()
    threads = int(th) if th.isdigit() else defaults['threads']
    st = input(Fore.WHITE + f"Status codes [{defaults['status']}]: " + Style.RESET_ALL).strip() or defaults['status']
    fmt = input(Fore.WHITE + f"Format (txt/json/csv) [{defaults['format']}]: " + Style.RESET_ALL).strip().lower() or defaults['format']
    px = input(Fore.WHITE + f"Proxy URL [{defaults['proxy']}]: " + Style.RESET_ALL).strip() or defaults['proxy']
    pr = input(Fore.WHITE + f"Profile [{defaults['profile']}]: " + Style.RESET_ALL).strip()
    profile = pr if pr in PROFILES else defaults['profile']
    bp = input(Fore.WHITE + "Enable 403-bypass mode? [y/N]: " + Style.RESET_ALL).strip().lower()
    bypass_403 = bp in ('y','yes')
    lu = input(Fore.WHITE + f"Login URL [{defaults['login_url']}]: " + Style.RESET_ALL).strip() or defaults['login_url']
    un = input(Fore.WHITE + f"Username [{defaults['username']}]: " + Style.RESET_ALL).strip() or defaults['username']
    pw = input(Fore.WHITE + f"Password [{defaults['password']}]: " + Style.RESET_ALL).strip() or defaults['password']
    od = input(Fore.WHITE + f"OOB Domain [{defaults['oob_domain']}]: " + Style.RESET_ALL).strip() or defaults['oob_domain']
    summary = {'url':url,'wordlist':wl,'output':out,'threads':threads,'status':st,'format':fmt,'proxy':px,'profile':profile,'bypass_403':bypass_403,'login_url':lu,'username':un,'password':pw,'oob_domain':od}
    print(Fore.CYAN+"\nConfiguration Summary:"+Style.RESET_ALL)
    for k,v in summary.items():
        flag = Fore.GREEN+" (default)"+Style.RESET_ALL if v==defaults.get(k) else ""
        print(" ",k.ljust(10),":",v,flag)
    if prompt_save_profile(summary): save_profile_interactive(summary)
    input(Fore.CYAN+"\nPress Enter to start the scan..."+Style.RESET_ALL)
    return summary