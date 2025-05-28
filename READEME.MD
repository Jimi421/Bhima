# 🔱 BhimaScan

**BhimaScan** is a modular, stealthy, and powerful hidden directory and endpoint discovery tool built for elite Red Teams.  
Designed with precision, BhimaScan balances stealth, configurability, and aggressive capability — perfect for professional operators and cybersecurity analysts.

---

## ⚙️ Features

- 🧠 **Interactive Mode** with smart defaults for ease of use
- 🏹 **CLI Mode** for automation and scripting
- 🔍 Multiple scan profiles:
  - **Quick Scan** (short wordlist, light delay)
  - **Stealth Scan** (medium list, randomized delay, proxy support)
  - **Brute Force Scan** (aggressive with large wordlists)
- 🛡️ Proxy support with rotation
- 🎯 Status code filtering + colorized terminal output
- 📁 Automatic saving of results to `.json` and `.txt` files
- 💾 Reusable config profiles
- 🧙 WAF/EDR bypass engine (experimental phase)
- 🧩 Modular structure for future upgrades

---

## 🖥️ Interactive Mode – Example

```bash
python3 bhima_scan.py
Example prompt:

mathematica
Copy
Edit
[+] Welcome to BhimaScan Interactive Mode
-------------------------------------------
Enter target URL: http://targetsite.com

Select scan profile:
  [1] Quick Scan (short wordlist, light delay)
  [2] Stealth Scan (medium wordlist, randomized delay, proxy rotation)
  [3] Bruteforce Scan (large wordlist, aggressive settings)
  [4] Load custom config

Enter your choice [1-4]: 2

Proxy mode? (y/n): y
Use default proxy list or custom? [d/c]: d

Saving config for future use? (y/n): y
Enter name for your profile: stealth_v1

[+] Starting scan with profile 'stealth_v1'...
Results will be saved in the outputs/ directory as both .txt and .json.

🚀 CLI Mode – Flags Example
bash
Copy
Edit
python3 bhima_scan.py -u http://targetsite.com -w wordlists/common.txt --profile stealth --proxy --output outputs/scan_results.txt
Use --help to view all options:

bash
Copy
Edit
python3 bhima_scan.py --help
🧰 Modular Layout
bash
Copy
Edit
BhimaScan/
├── bhima_scan.py          # Main launcher
├── cli.py                 # Interactive + CLI handler
├── core.py                # Scan engine
├── utils.py               # Wordlists, proxies, helpers
├── config/                # Saved profiles
├── outputs/               # Saved results
├── wordlists/             # Wordlists
├── README.md
💬 Contribute
Got a WAF bypass idea? Want to contribute modules or bypass lists?
Pull requests welcome. Stay stealthy.

✍️ Author
Jimi421
Cybersecurity Explorer | Red Team Apprentice | 🛡️ Dharma-Focused Coder

⚡ Fun Fact
🎨 I love art and music — because even in code, beauty matters.

yaml
Copy
Edit
