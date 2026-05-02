#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

# Ensure the engine can find your src directory
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from Obsidian.core.engine import identify_file

# Terminal Colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print(" ██████╗ ██████╗ ███████╗██╗██████╗ ██╗ █████╗ ███╗   ██╗")
    print("██╔═══██╗██╔══██╗██╔════╝██║██╔══██╗██║██╔══██╗████╗  ██║")
    print("██║   ██║██████╔╝███████╗██║██║  ██║██║███████║██╔██╗ ██║")
    print("██║   ██║██╔══██╗╚════██║██║██║  ██║██║██╔══██║██║╚██╗██║")
    print("╚██████╔╝██████╔╝███████║██║██████╔╝██║██║  ██║██║ ╚████║")
    print(" ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝")
    print(f"                       Forensic Analysis Engine v1.0{Colors.ENDC}\n")

def format_output(result):
    print(f"{Colors.BOLD}TARGET:{Colors.ENDC}  {result['file']}")
    
    # Identity & Confidence
    conf_color = Colors.GREEN if result['confidence'] >= 0.8 else Colors.WARNING
    print(f"{Colors.BOLD}TYPE:{Colors.ENDC}    {result['type']} {conf_color}(Confidence: {result['confidence']}){Colors.ENDC}")
    
    # Entropy Status
    ent_color = Colors.FAIL if result['entropy'] > 7.5 or result['entropy'] < 6.0 else Colors.CYAN
    print(f"{Colors.BOLD}ENTROPY:{Colors.ENDC} {ent_color}{result['entropy']}{Colors.ENDC}")
    
    # Cryptographic Identity
    print(f"\n{Colors.BOLD}[+] CRYPTOGRAPHY{Colors.ENDC}")
    print(f"    MD5:     {result['hashes'].get('md5', 'N/A')}")
    print(f"    SHA-256: {result['hashes'].get('sha256', 'N/A')}")
    
    # Artifacts
    iocs = result.get('iocs', {})
    if any(iocs.values()):
        print(f"\n{Colors.BOLD}[+] ARTIFACTS{Colors.ENDC}")
        for ipv4 in iocs.get('ipv4', []):
            print(f"    IPv4: {Colors.CYAN}{ipv4}{Colors.ENDC}")
        for url in iocs.get('urls', []):
            print(f"    URL:  {Colors.CYAN}{url}{Colors.ENDC}")
        for btc in iocs.get('btc_wallets', []):
            print(f"    BTC:  {Colors.FAIL}{btc}{Colors.ENDC}")
    
    # Heuristics
    hints = result.get('hints', [])
    if hints:
        print(f"\n{Colors.BOLD}[!] HEURISTICS{Colors.ENDC}")
        for hint in hints:
            print(f"    {Colors.FAIL}-> {hint}{Colors.ENDC}")
    
    print("-" * 65)

def scan_target(target_path):
    path = Path(target_path).resolve()
    
    if not path.exists():
        print(f"{Colors.FAIL}[!] Target does not exist: {path}{Colors.ENDC}")
        return
        
    if path.is_file():
        format_output(identify_file(str(path)))
    elif path.is_dir():
        print(f"[*] Commencing recursive directory scan: {path}\n")
        # Ignore common noise directories
        ignore_dirs = {'.git', '__pycache__', 'node_modules', 'venv'}
        
        for file_path in path.rglob('*'):
            if file_path.is_file() and not any(part in ignore_dirs for part in file_path.parts):
                # Skip files larger than 100MB in bulk scans to save time
                if file_path.stat().st_size > 100 * 1024 * 1024:
                    print(f"{Colors.WARNING}[-] Skipping massive file: {file_path.name}{Colors.ENDC}\n" + "-"*65)
                    continue
                format_output(identify_file(str(file_path)))

def main():
    parser = argparse.ArgumentParser(description="Obsidian Forensic Analysis Engine")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--json", action="store_true", help="Output raw JSON for scripting pipelines")
    
    args = parser.parse_args()
    
    if args.json:
        path = Path(args.target).resolve()
        if path.is_file():
            print(json.dumps(identify_file(str(path)), indent=4))
        elif path.is_dir():
            results = [identify_file(str(f)) for f in path.rglob('*') if f.is_file()]
            print(json.dumps(results, indent=4))
    else:
        print_banner()
        scan_target(args.target)

if __name__ == "__main__":
    main()