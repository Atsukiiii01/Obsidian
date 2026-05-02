import re
import ipaddress
from pathlib import Path

def find_iocs(file_path, chunk_size=1048576):
    path = Path(file_path).expanduser().resolve()
    iocs = {"ipv4": set(), "urls": set(), "btc_wallets": set()}
    
    if not path.exists():
        return {"ipv4": [], "urls": [], "btc_wallets": []}

    ipv4_pattern = re.compile(rb'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    url_pattern = re.compile(rb'https?://[^\s<>"\']+|www\.[^\s<>"\']+')
    # Basic BTC pattern (P2PKH and P2SH)
    btc_pattern = re.compile(rb'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')

    try:
        with path.open("rb") as f:
            while chunk := f.read(chunk_size):
                # Extract and Validate IPv4
                for match in ipv4_pattern.finditer(chunk):
                    ip_str = match.group().decode('ascii', errors='ignore')
                    try:
                        ip_obj = ipaddress.IPv4Address(ip_str)
                        # Only keep Public, Routable IP addresses. Drop local/multicast noise.
                        if ip_obj.is_global and not ip_obj.is_multicast:
                            iocs["ipv4"].add(ip_str)
                    except ipaddress.AddressValueError:
                        pass # Not a real IP (e.g., 999.999.999.999 or version numbers)
                
                # Extract URLs
                for match in url_pattern.finditer(chunk):
                    url = match.group().decode('ascii', errors='ignore')
                    # Basic filter to drop local schemas
                    if not url.startswith("http://localhost") and not url.startswith("http://127."):
                        iocs["urls"].add(url)

                # Extract BTC Wallets
                for match in btc_pattern.finditer(chunk):
                    iocs["btc_wallets"].add(match.group().decode('ascii', errors='ignore'))
                    
        return {
            "ipv4": list(iocs["ipv4"]),
            "urls": list(iocs["urls"]),
            "btc_wallets": list(iocs["btc_wallets"])
        }
    except Exception:
        return {"ipv4": [], "urls": [], "btc_wallets": []}